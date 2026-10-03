"""Teste HTTP → serviço → PostgreSQL com identidades sintéticas em base temporária."""
import copy
import json
from pathlib import Path
import sys
import threading
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
    admin.execute(sql.SQL('CREATE DATABASE {} TEMPLATE escritorio_test').format(sql.Identifier(database)))
    service=Servico(config,database)
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
            with urlopen(request,timeout=10) as response:return response.status,json.loads(response.read())
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
        assert post('registrar_relato',{'registro_id':id_,'versao_esperada':2,'entregue':'Sem anexo persistido','artefatos':[str(uuid.uuid4())]})[0][0]==422
        assert post('criar_registro',{'tipo':'projeto','titulo':'Promoção indevida'})[0][0]==422
        assert post('capturar_entrada',{'artefato_id':str(uuid.uuid4()),'origem':{}})[0][0]==422
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
        with psycopg.connect(host=env['PGHOST'],port=env['PGPORT'],dbname=database,user='escritorio_api_local',password=config['senha_banco']) as conn:
            row=conn.execute('SELECT rolsuper,rolcreatedb FROM pg_roles WHERE rolname=current_user').fetchone()
            assert row==(False,False)
            assert conn.execute('SELECT count(*) FROM escritorio.historico WHERE portfolio=%s AND registro=%s',('demo_escritorio',id_)).fetchone()[0]==2
            assert conn.execute('SELECT count(*) FROM escritorio.operacoes WHERE id=%s',(concurrent['operacao_id'],)).fetchone()[0]==1
            assert conn.execute("SELECT has_schema_privilege(current_user,'escritorio','CREATE')").fetchone()[0] is False
        print('PASSOU: HTTP → serviço → PostgreSQL; captura, criação, relato e leitura após commit.')
        print('PASSOU: tokens, perfis, portfólios, executor atribuído, conflito de versão, SQL parametrizado,')
        print('repetição concorrente, paginação assinada, rejeição de anexos/promoção indisponíveis e histórico.')
        print('PASSOU: recuperação por ID após falha simulada de confirmação pós-commit, sem duplicação.')
        print('Respostas validadas contra JSON Schema; testes em base temporária, sem dados reais.')
    finally:
        http.shutdown();http.server_close();thread.join(timeout=5)
        admin.execute(sql.SQL('DROP DATABASE {}').format(sql.Identifier(database)))
        admin.close()


if __name__=='__main__':main()
