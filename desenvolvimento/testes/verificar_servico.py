"""Teste HTTP → serviço → PostgreSQL com identidades sintéticas em base temporária."""
import copy
import base64
import hashlib
import json
from pathlib import Path
import sys
import threading
import tempfile
import subprocess
import uuid
from concurrent.futures import ThreadPoolExecutor
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request,urlopen
import psycopg
from unittest.mock import patch
from psycopg import sql
from jsonschema import Draft202012Validator,FormatChecker
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'servico'))
from nucleo import Servico,CONFIG,API,ambiente,Falha
from http_local import server


def main():
    if not ambiente.running(): raise RuntimeError('Inicie o PostgreSQL local e prepare a demo.')
    config=json.loads(CONFIG.read_text())
    clients=json.loads((CONFIG.parent/'clientes.local.json').read_text())['identidades']
    env=ambiente.connection()
    database='ep_test_'+uuid.uuid4().hex[:12]
    admin=psycopg.connect(host=env['PGHOST'],port=env['PGPORT'],dbname='postgres',user=env['PGUSER'],password=env['PGPASSWORD'],autocommit=True)
    # pg_dump fornece snapshot consistente mesmo com DBeaver conectado à demo.
    with tempfile.TemporaryDirectory(prefix='ep-servico-test-') as directory:
        dump=str(Path(directory)/'demo.dump')
        ambiente.execute([ambiente.binary('pg_dump'),'-Fc','-f',dump],env)
        admin.execute(sql.SQL('CREATE DATABASE {}').format(sql.Identifier(database)))
        try:
            ambiente.execute([ambiente.binary('pg_restore'),'--exit-on-error','-d',database,dump],env)
        except Exception:
            admin.execute(sql.SQL('DROP DATABASE {}').format(sql.Identifier(database)))
            admin.close()
            raise
    objects=tempfile.TemporaryDirectory(prefix='ep-objetos-test-')
    service=Servico(config,database,objetos=objects.name)
    http=server(service,0)
    thread=threading.Thread(target=http.serve_forever,daemon=True);thread.start()
    base='http://127.0.0.1:'+str(http.server_port)
    p='/v1/portfolios/demo_escritorio'
    validator=Draft202012Validator(API['components']['schemas']['Resultado'],format_checker=FormatChecker())
    def call(path,profile='gestor',body=None,key=None,token=None):
        headers={'Authorization':'Bearer '+(token or clients[profile]['token'])}
        if body is not None: headers['Content-Type']='application/json'
        if key: headers['Idempotency-Key']=key
        request=Request(base+path,data=None if body is None else json.dumps(body).encode(),headers=headers)
        try:
            with urlopen(request,timeout=10) as response:
                raw=response.read()
                return response.status,raw if response.headers.get_content_type()=='application/octet-stream' else json.loads(raw)
        except HTTPError as error:return error.code,json.loads(error.read())
    def post(command,data,profile='gestor',id_=None,key=None):
        pedido={'operacao_id':id_ or str(uuid.uuid4()),'comando':command,'dados':data}
        return call(p+'/operacoes',profile,pedido,key or pedido['operacao_id']),pedido
    try:
        assert call(p+'/registros',token='invalido')[0]==401
        assert call(p+'/registros',profile='outro')[0]==403
        assert post('criar_registro',{'tipo':'tarefa','titulo':'Proibido'},profile='consulta')[0][0]==403
        (status,entrada),pedido=post('capturar_entrada',{'texto':'Relatório trimestral sintético','origem':{'canal':'teste'}})
        assert status==200 and entrada['estado']=='verificada' and entrada['protecao']=='pendente'
        validator.validate(entrada)
        assert entrada['resultado']['entrada']['texto']==pedido['dados']['texto']
        assert call(p+'/operacoes',body=pedido,key=pedido['operacao_id'])==(status,entrada)
        conflict=copy.deepcopy(pedido);conflict['dados']['texto']='Conteúdo divergente'
        assert call(p+'/operacoes',body=conflict,key=pedido['operacao_id'])[0]==409
        injected=copy.deepcopy(pedido);injected['ator']=clients['outro']['pessoa']
        assert call(p+'/operacoes',body=injected,key=str(uuid.uuid4()))[0]==400
        (status,task),_=post('criar_registro',{'tipo':'tarefa','titulo':'Inventário sintético','origem_entrada_id':entrada['resultado']['entrada_id'],'responsavel_total':clients['executor']['pessoa'],'criterio_conclusao':'Inventário completo e validado'})
        assert status==200;validator.validate(task)
        id_=task['registros'][0]['id']
        (status,update),_=post('registrar_relato',{'registro_id':id_,'versao_esperada':1,'entregue':'Codificação concluída','restante':'Integração pendente','esforco_restante':3,'prazo_proposto':'2026-10-09'},profile='executor')
        assert status==200;validator.validate(update)
        assert update['resultado']['registro']['estado']=='capturada'
        assert update['resultado']['registro']['prazo_aceito'] is None
        assert update['registros'][0]['versao']==2
        assert post('registrar_relato',{'registro_id':id_,'versao_esperada':1,'entregue':'Reenvio obsoleto'},profile='executor')[0][0]==409
        assert post('registrar_relato',{'registro_id':id_,'versao_esperada':2,'entregue':'Sem autorização'},profile='consulta')[0][0]==403
        assert post('registrar_relato',{'registro_id':id_,'versao_esperada':2,'entregue':'Sem anexo persistido','artefatos':[str(uuid.uuid4())]})[0][0]==404
        assert post('criar_registro',{'tipo':'projeto','titulo':'Promoção indevida'})[0][0]==422
        assert post('capturar_entrada',{'artefato_id':str(uuid.uuid4()),'origem':{}})[0][0]==404
        assert call(p+'/operacoes/'+update['operacao_id'],profile='executor')[0]==200
        assert call(p+'/registros?'+urlencode({'assunto':"' OR TRUE --"}))[1]['itens']==[]
        assert call(p+'/registros?limite=0')[0]==400
        assert call(p+'/registros?cursor=invalido')[0]==400
        for i in range(2): assert post('criar_registro',{'tipo':'tarefa','titulo':f'Tarefa sem executor {i}'})[0][0]==200
        status,page=call(p+'/registros?limite=1');assert status==200 and page['proximo_cursor']
        next_page=call(p+'/registros?'+urlencode({'limite':1,'cursor':page['proximo_cursor']}))[1]
        assert next_page['itens'][0]['id']!=page['itens'][0]['id']
        assert call(p+'/registros?'+urlencode({'limite':1,'assunto':'alterado','cursor':page['proximo_cursor']}))[0]==400
        assert len(call(p+'/registros',profile='executor')[1]['itens'])==1
        hidden=post('criar_registro',{'tipo':'tarefa','titulo':'Privada'})[0][1]['registros'][0]['id']
        assert post('registrar_relato',{'registro_id':hidden,'versao_esperada':1,'entregue':'Invasão'},profile='executor')[0][0]==404
        # Consolidar complemento sem criar outro registro ou perder o original.
        (status,idea),_=post('criar_registro',{'tipo':'ideia','titulo':'Ideia sintética de intranet','resultado_esperado':'App de demandas'})
        assert status==200
        idea_id=idea['registros'][0]['id']
        (status,source),_=post('capturar_entrada',{'texto':'Será evolução do SuperSync','origem':{'canal':'teste','registro_id':idea_id}})
        assert status==200
        source_id=source['resultado']['entrada_id']
        data={'registro_id':idea_id,'versao_esperada':1,'motivo':'Definição do proponente','entrada_id':source_id,'alteracoes':{'resultado_esperado':'App de demandas como evolução do SuperSync'}}
        (status,changed),change_request=post('atualizar_registro',data)
        assert status==200;validator.validate(changed)
        assert changed['registros'][0]['versao']==2
        assert changed['resultado']['registro']['entradas'][0]['conteudo']=='Será evolução do SuperSync'
        assert changed['resultado']['registro']['entradas'][0]['estado']=='vinculada'
        assert changed['resultado']['registro']['estado']=='capturada'
        assert changed['resultado']['registro']['responsavel_total'] is None
        assert call(p+'/operacoes',body=change_request,key=change_request['operacao_id'])==(status,changed)
        assert post('atualizar_registro',data)[0][0]==409
        fresh={**data,'versao_esperada':2}
        assert post('atualizar_registro',fresh,profile='executor')[0][0]==403
        assert post('atualizar_registro',fresh,profile='consulta')[0][0]==403
        assert post('atualizar_registro',{**fresh,'alteracoes':{'estado':'promovida'}})[0][0]==400
        assert post('atualizar_registro',{**fresh,'alteracoes':{}})[0][0]==400
        assert post('atualizar_registro',{**fresh,'alteracoes':{'titulo':'   '}})[0][0]==400
        other_id=post('criar_registro',{'tipo':'ideia','titulo':'Outra ideia'})[0][1]['registros'][0]['id']
        assert post('atualizar_registro',{**data,'registro_id':other_id})[0][0]==409
        assert post('criar_registro',{'tipo':'ideia','titulo':'Duplicação da entrada','origem_entrada_id':source_id})[0][0]==409
        wrong=post('capturar_entrada',{'texto':'Outro assunto','origem':{'registro_id':other_id}})[0][1]['resultado']['entrada_id']
        assert post('atualizar_registro',{**fresh,'entrada_id':wrong})[0][0]==409
        foreign_path='/v1/portfolios/demo_outro/operacoes'
        foreign_request={'operacao_id':str(uuid.uuid4()),'comando':'capturar_entrada','dados':{'texto':'Outro portfólio','origem':{}}}
        foreign=call(foreign_path,profile='outro',body=foreign_request,key=foreign_request['operacao_id'])
        assert foreign[0]==200
        assert post('atualizar_registro',{**fresh,'entrada_id':foreign[1]['resultado']['entrada_id']})[0][0]==404
        assert post('atualizar_registro',{'registro_id':id_,'versao_esperada':2,'motivo':'Tipo não disponível','alteracoes':{'titulo':'Tarefa'}})[0][0]==422
        found=call(p+'/registros?'+urlencode({'assunto':'SuperSync'}))[1]['itens']
        recovered=next(x for x in found if x['id']==idea_id)
        assert recovered['versao']==2 and recovered['entradas'][0]['id']==source_id
        # Falha antes do histórico reverte texto, vínculo e operação juntos.
        rollback_source=post('capturar_entrada',{'texto':'Complemento que deve permanecer pendente','origem':{}})[0][1]['resultado']['entrada_id']
        rollback_request={'operacao_id':str(uuid.uuid4()),'comando':'atualizar_registro','dados':{'registro_id':idea_id,'versao_esperada':2,'motivo':'Falha sintética','entrada_id':rollback_source,'alteracoes':{'titulo':'Não persistir'}}}
        original_snapshot=service.snapshot
        def fail_after_update(conn,portfolio,record_id,actor,role):
            result=original_snapshot(conn,portfolio,record_id,actor,role)
            if record_id==idea_id and result['versao']==3:
                raise Falha(503,'SERVICO_INDISPONIVEL','Falha sintética pré-commit')
            return result
        with patch.object(service,'snapshot',side_effect=fail_after_update):
            assert call(p+'/operacoes',body=rollback_request,key=rollback_request['operacao_id'])[0]==503
        assert call(p+'/registros?'+urlencode({'id':idea_id}))[1]['itens'][0]['versao']==2
        with service.connect() as conn:
            assert conn.execute('SELECT estado FROM entradas WHERE portfolio=%s AND id=%s',('demo_escritorio',rollback_source)).fetchone()['estado']=='triagem_pendente'
            histories=conn.execute('SELECT antes,depois,motivo FROM historico WHERE portfolio=%s AND registro=%s AND acao=%s',('demo_escritorio',idea_id,'atualizar_registro')).fetchall()
            assert len(histories)==1 and histories[0]['antes']['versao']==1 and histories[0]['depois']['versao']==2
            assert histories[0]['motivo']=='Definição do proponente'
        # Dois pedidos diferentes na mesma versão não sobrescrevem um ao outro.
        competing=[{'operacao_id':str(uuid.uuid4()),'comando':'atualizar_registro','dados':{'registro_id':idea_id,'versao_esperada':2,'motivo':'Concorrência de conteúdo','alteracoes':{'titulo':f'Proposta concorrente {i}'}}} for i in range(2)]
        with ThreadPoolExecutor(max_workers=2) as pool:
            outcomes=list(pool.map(lambda request:call(p+'/operacoes',body=request,key=request['operacao_id']),competing))
        assert sorted(status for status,_ in outcomes)==[200,409]
        request_id=post('criar_registro',{'tipo':'solicitacao','titulo':'Relatório pontual'})[0][1]['registros'][0]['id']
        assert post('atualizar_registro',{'registro_id':request_id,'versao_esperada':1,'motivo':'Detalhamento explícito','alteracoes':{'resultado_esperado':'Relatório trimestral recuperável'}})[0][0]==200
        content=b'Relatorio sintetico\nEntrega parcial: API pendente.\n'
        artifact_data={'nome':'relatorio.txt','tipo_midia':'text/plain','bytes_esperados':len(content),'sha256_esperado':hashlib.sha256(content).hexdigest(),'origem':{'canal':'ensaio'}}
        assert post('preparar_artefato',artifact_data,profile='consulta')[0][0]==403
        assert post('preparar_artefato',artifact_data,profile='executor')[0][0]==403
        assert post('preparar_artefato',{**artifact_data,'bytes_esperados':524289})[0][0]==400
        (status,prepared),prepare_request=post('preparar_artefato',artifact_data)
        assert status==200;validator.validate(prepared)
        artifact_id=prepared['resultado']['artefato']['id']
        assert prepared['resultado']['artefato']['estado']=='preparado' and prepared['lacunas']
        assert 'chave_objeto' not in prepared['resultado']['artefato']
        assert call(p+'/operacoes',body=prepare_request,key=prepare_request['operacao_id'])[1]==prepared
        assert call(p+'/artefatos/'+artifact_id)[0]==422
        assert post('verificar_artefato',{'artefato_id':artifact_id})[0][0]==422
        link={'registro_id':id_,'versao_esperada':2,'artefato_id':artifact_id,'finalidade':'evidencia','motivo':'Evidência de avanço parcial'}
        assert post('vincular_artefato',link)[0][0]==422
        assert post('enviar_artefato',{'artefato_id':artifact_id,'conteudo_base64':'invalido!'})[0][0]==400
        assert post('enviar_artefato',{'artefato_id':artifact_id,'conteudo_base64':base64.b64encode(b'divergente').decode()})[0][0]==422
        upload={'artefato_id':artifact_id,'conteudo_base64':base64.b64encode(content).decode()}
        # Arquivo durável com falha pré-commit: retry reconcilia o mesmo objeto.
        upload_request={'operacao_id':str(uuid.uuid4()),'comando':'enviar_artefato','dados':upload}
        original_save=service.objetos.save
        def interrupted_save(*args):
            original_save(*args)
            raise OSError('Falha sintética após persistir arquivo')
        with patch.object(service.objetos,'save',side_effect=interrupted_save):
            assert call(p+'/operacoes',body=upload_request,key=upload_request['operacao_id'])[0]==503
        with service.connect() as conn:
            assert conn.execute('SELECT estado FROM artefatos WHERE portfolio=%s AND id=%s',('demo_escritorio',artifact_id)).fetchone()['estado']=='preparado'
        status,uploaded=call(p+'/operacoes',body=upload_request,key=upload_request['operacao_id'])
        assert status==200 and uploaded['resultado']['artefato']['estado']=='verificado'
        validator.validate(uploaded)
        assert call(p+'/artefatos/'+artifact_id)==(200,content)
        assert call(p+'/artefatos/'+artifact_id,profile='executor')[0]==404
        assert call(p+'/artefatos/'+artifact_id,profile='consulta')[0]==404
        assert call('/v1/portfolios/demo_outro/artefatos/'+artifact_id,profile='outro')[0]==404
        assert post('verificar_artefato',{'artefato_id':artifact_id})[0][0]==200
        # Nome do cliente é metadado; nunca vira caminho no servidor.
        unsafe=post('preparar_artefato',{**artifact_data,'nome':'../../fora.txt'})[0][1]['resultado']['artefato']['id']
        assert service.objetos.path('demo_escritorio',unsafe).parent==Path(objects.name)
        (status,linked),link_request=post('vincular_artefato',link)
        assert status==200 and linked['registros'][0]['versao']==3
        assert linked['resultado']['registro']['fontes'][0]['integridade']=='verificada'
        assert linked['resultado']['registro']['estado']=='capturada'
        assert call(p+'/operacoes',body=link_request,key=link_request['operacao_id'])[1]==linked
        assert post('vincular_artefato',link)[0][0]==409
        assert call(p+'/artefatos/'+artifact_id,profile='executor')==(200,content)
        assert call(p+'/artefatos/'+artifact_id,profile='consulta')==(200,content)
        assert post('registrar_relato',{'registro_id':id_,'versao_esperada':3,'entregue':'Relatório parcial','artefatos':[artifact_id]},profile='executor')[0][0]==200
        captured_artifact=post('capturar_entrada',{'artefato_id':artifact_id,'origem':{'canal':'reunião sintética'}})[0][1]['resultado']['entrada_id']
        from_original=post('criar_registro',{'tipo':'solicitacao','titulo':'Demanda com original','origem_entrada_id':captured_artifact})[0][1]
        assert from_original['resultado']['registro']['fontes'][0]['finalidade']=='origem'
        # Cliente portável prepara/envia/vincula e retoma sem duplicar as etapas.
        fixture=Path(objects.name)/'fixture.txt';fixture.write_bytes(b'Anexo pelo cliente de referencia')
        cli_task=post('criar_registro',{'tipo':'tarefa','titulo':'Teste de cliente'})[0][1]['registros'][0]['id']
        client=[sys.executable,str(Path(__file__).resolve().parents[1]/'servico/cliente.py')]
        upload_cli=client+['anexar','--porta',str(http.server_port),'--id',str(uuid.uuid4()),'--chave','fixture-cli-'+uuid.uuid4().hex,'--arquivo',str(fixture),'--registro',cli_task,'--versao','1','--finalidade','evidencia']
        first=subprocess.run(upload_cli,capture_output=True,text=True,check=True)
        assert '"estado": "verificada"' in first.stdout
        second=subprocess.run(upload_cli,capture_output=True,text=True,check=True)
        assert first.stdout==second.stdout
        cli_record=call(p+'/registros?'+urlencode({'id':cli_task}))[1]['itens'][0]
        assert cli_record['versao']==2 and len(cli_record['fontes'])==1
        downloaded=Path(objects.name)/'download.txt'
        subprocess.run(client+['baixar','--porta',str(http.server_port),'--id',cli_record['fontes'][0]['artefato'],'--arquivo',str(downloaded)],capture_output=True,text=True,check=True)
        assert downloaded.read_bytes()==fixture.read_bytes()
        assert subprocess.run(client+['baixar','--porta',str(http.server_port),'--id',cli_record['fontes'][0]['artefato'],'--arquivo',str(downloaded)],capture_output=True,text=True).returncode!=0
        # Corrupção externa é detectada na consulta, download e recuperação da operação.
        path=service.objetos.path('demo_escritorio',artifact_id)
        path.write_bytes(b'Corrompido')
        assert call(p+'/artefatos/'+artifact_id)[0]==422
        assert call(p+'/operacoes/'+uploaded['operacao_id'])[0]==422
        assert call(p+'/registros?'+urlencode({'id':id_}))[1]['itens'][0]['fontes'][0]['integridade']=='indisponivel_ou_divergente'
        assert post('verificar_artefato',{'artefato_id':artifact_id})[0][0]==422
        assert post('enviar_artefato',upload)[0][0]==422
        path.write_bytes(content)  # Restaurar fixture sintética, não rotina produtiva.
        # Um objeto substituído por symlink não é seguido pelo servidor.
        path.unlink();path.symlink_to(fixture)
        assert call(p+'/artefatos/'+artifact_id)[0]==422
        path.unlink();path.write_bytes(content)
        # Simular perda da confirmação após commit: retomar por ID sem repetir efeitos.
        recovery={'operacao_id':str(uuid.uuid4()),'comando':'criar_registro','dados':{'tipo':'tarefa','titulo':'Recuperação após commit'}}
        with patch.object(service,'get_operation',side_effect=Falha(503,'SERVICO_INDISPONIVEL','Falha simulada após commit')):
            assert call(p+'/operacoes',body=recovery,key=recovery['operacao_id'])[0]==503
        status,reconciled=call(p+'/operacoes/'+recovery['operacao_id'])
        assert status==200 and reconciled['estado']=='verificada'
        assert call(p+'/operacoes',body=recovery,key=recovery['operacao_id'])==(status,reconciled)
        # Duas requisições simultâneas idênticas produzem o mesmo resultado.
        concurrent={'operacao_id':str(uuid.uuid4()),'comando':'criar_registro','dados':{'tipo':'tarefa','titulo':'Concorrência sintética'}}
        with ThreadPoolExecutor(max_workers=2) as pool:
            results=list(pool.map(lambda _:call(p+'/operacoes',body=concurrent,key=concurrent['operacao_id']),range(2)))
        assert results[0]==results[1] and results[0][0]==200
        from cenarios_reunioes import run as verificar_reunioes
        verificar_reunioes(call,post,p,service,clients,validator,client,http.server_port,Path(objects.name))
        with psycopg.connect(host=env['PGHOST'],port=env['PGPORT'],dbname=database,user='escritorio_api_local',password=config['senha_banco']) as conn:
            row=conn.execute('SELECT rolsuper,rolcreatedb FROM pg_roles WHERE rolname=current_user').fetchone()
            assert row==(False,False)
            assert conn.execute('SELECT count(*) FROM escritorio.historico WHERE portfolio=%s AND registro=%s',('demo_escritorio',id_)).fetchone()[0]==4
            assert conn.execute('SELECT count(*) FROM escritorio.operacoes WHERE id=%s',(concurrent['operacao_id'],)).fetchone()[0]==1
            assert conn.execute("SELECT has_schema_privilege(current_user,'escritorio','CREATE')").fetchone()[0] is False
        print('PASSOU: HTTP → serviço → PostgreSQL; captura, criação, relato e leitura após commit.')
        print('PASSOU: tokens, perfis, portfólios, executor atribuído, conflito de versão, SQL parametrizado,')
        print('repetição concorrente, paginação assinada, rejeição de promoção indisponível e histórico.')
        print('PASSOU: recuperação por ID após falha simulada de confirmação pós-commit, sem duplicação.')
        print('PASSOU: atualização de ideias, vínculo de originais, busca pelo conteúdo, isolamento, histórico e rollback atômico.')
        print('PASSOU: anexos imutáveis, checksum/tamanho, download autenticado, evidência parcial, corrupção e recuperação de envio interrompido.')
        print('Respostas validadas contra JSON Schema; testes em base temporária, sem dados reais.')
    finally:
        http.shutdown();http.server_close();thread.join(timeout=5)
        admin.execute(sql.SQL('DROP DATABASE {}').format(sql.Identifier(database)))
        admin.close()
        objects.cleanup()


if __name__=='__main__':main()
