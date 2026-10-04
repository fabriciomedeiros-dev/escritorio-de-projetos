"""Bloqueios/dependências/aceite humano, via HTTP em base temporária."""
import base64
import copy
import hashlib
import uuid
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import patch


def run(call, post, p, service, clients, validator):
    def ok(command, data):
        (status, result), pedido = post(command, data)
        assert status == 200, (command, status, result)
        validator.validate(result)
        return result, pedido
    def task(name, owner=True, criterion=True):
        data={'tipo':'tarefa','titulo':name}
        if owner:data['responsavel_total']=clients['executor']['pessoa']
        if criterion:data['criterio_conclusao']='Entrega integrada e teste documentado'
        result,_=ok('criar_registro',data)
        return result['registros'][0]['id']
    def read(id_):return call(p+'/registros?id='+id_)[1]['itens'][0]
    def version(id_):return read(id_)['versao']
    content=b'Evidencia sintetica de configuracao, integracao e teste.'
    artifact,_=ok('preparar_artefato',{'nome':'evidencia-bloqueio.txt','tipo_midia':'text/plain','bytes_esperados':len(content),'sha256_esperado':hashlib.sha256(content).hexdigest(),'origem':{'canal':'teste sintético'}})
    evidence=artifact['resultado']['artefato']['id']
    ok('enviar_artefato',{'artefato_id':evidence,'conteudo_base64':base64.b64encode(content).decode()})
    target=task('Bloqueio sintético: autenticação')
    provider=task('Provedor sintético: configurar e-mail')
    def dep(id_, blocked=False, **extra):
        data={'registro_id':id_,'versao_esperada':version(id_),'terceiro':'Infraestrutura sintética','motivo':'Configuração necessária','responsavel_acao':clients['gestor']['pessoa'],'proxima_acao':'Configurar e testar','acompanhar_em':'2020-01-01','criterio_resolucao':'Código enviado e recebido no teste','impede_avanco':blocked}
        if 'provedor_id' in extra:data.pop('terceiro')
        return {**data,**extra}
    def resolve(id_, depid):
        return {'registro_id':id_,'versao_esperada':version(id_),'dependencia_id':depid,'evidencia_id':evidence,'criterio_atendido':True,'justificativa':'Teste revisado pelo gestor satisfaz o critério registrado'}
    def complete(id_):
        return {'registro_id':id_,'versao_esperada':version(id_),'modo':'aceite_humano','criterio_atendido':True,'parecer':'Critério da entrega verificado pelo gestor no teste documentado','artefatos':[evidence]}

    invalid=dep(target);invalid.pop('acompanhar_em')
    assert post('registrar_dependencia',invalid)[0][0]==400
    assert post('registrar_dependencia',{**dep(target),'motivo':'  '})[0][0]==400
    assert post('registrar_dependencia',{**dep(target),'provedor_id':provider})[0][0]==400
    assert post('registrar_dependencia',dep(target),profile='executor')[0][0]==403
    assert post('registrar_dependencia',dep(target),profile='consulta')[0][0]==403
    assert post('registrar_dependencia',{**dep(target),'responsavel_acao':clients['outro']['pessoa']})[0][0]==403
    assert post('registrar_dependencia',dep(target,provedor_id=target))[0][0]==422
    assert post('registrar_dependencia',dep(target,provedor_id='DEMO_OUTRO-TAR-AUSENTE'))[0][0]==404
    internal,_=ok('registrar_dependencia',dep(target,provedor_id=provider))
    internal_id=internal['resultado']['dependencia']['id']
    assert internal['resultado']['registro']['estado']=='capturada'
    assert internal['resultado']['registro']['impedimentos']=={'dependencias_pendentes':1,'bloqueios_de_avanco':0,'acompanhamentos_vencidos':1}
    assert post('registrar_dependencia',dep(target,provedor_id=provider))[0][0]==409
    # A dependência pode passar a impedir avanço e depois permitir trabalho parcial.
    for blocking in (True,False):
        ok('atualizar_dependencia',{'registro_id':target,'versao_esperada':version(target),'dependencia_id':internal_id,'motivo':'Gestor revisou possibilidade de trabalho em paralelo','alteracoes':{'impede_avanco':blocking}})
        assert read(target)['estado']==('bloqueada' if blocking else 'capturada')
        assert read(target)['dependencias'][0]['estado']=='pendente'

    assert post('validar_conclusao',complete(target))[0][0]==422
    assert post('resolver_dependencia',resolve(target,internal_id))[0][0]==422
    assert post('registrar_dependencia',dep(provider,provedor_id=target))[0][0]==422
    first,block_request=ok('registrar_dependencia',dep(target,True,criterio_resolucao='Serviço externo A liberado'))
    first_id=first['resultado']['dependencia']['id']
    assert read(target)['estado']=='bloqueada' and read(target)['estado_antes_bloqueio']=='capturada'
    assert call(p+'/operacoes',body=block_request,key=block_request['operacao_id'])[1]==first
    second,_=ok('registrar_dependencia',dep(target,True,terceiro='Fornecedor B',criterio_resolucao='Serviço externo B liberado'))
    second_id=second['resultado']['dependencia']['id']
    assert read(target)['impedimentos']['bloqueios_de_avanco']==2
    original_owner=read(target)['responsavel_total']
    update={'registro_id':target,'versao_esperada':version(target),'dependencia_id':first_id,'motivo':'Nova data de acompanhamento definida pelo gestor','alteracoes':{'responsavel_acao':clients['executor']['pessoa'],'proxima_acao':'Cobrar fornecedor e anexar retorno','acompanhar_em':'2099-01-01'}}
    updated,_=ok('atualizar_dependencia',update)
    assert updated['resultado']['registro']['responsavel_total']==original_owner
    assert next(d for d in read(target)['dependencias'] if d['id']==first_id)['acompanhamento']=='agendado'
    assert post('atualizar_dependencia',update)[0][0]==409
    assert post('resolver_dependencia',resolve(provider,first_id))[0][0]==404
    assert post('resolver_dependencia',{**resolve(target,first_id),'criterio_atendido':False})[0][0]==400
    assert post('resolver_dependencia',{**resolve(target,first_id),'evidencia_id':str(uuid.uuid4())})[0][0]==404
    object_path=service.objetos.path('demo_escritorio',evidence)
    object_path.write_bytes(b'Corrompido')
    assert post('resolver_dependencia',resolve(target,first_id))[0][0]==422
    assert next(d for d in read(target)['dependencias'] if d['id']==first_id)['estado']=='pendente'
    object_path.write_bytes(content)
    ok('resolver_dependencia',resolve(target,first_id))
    assert read(target)['estado']=='bloqueada'
    ok('resolver_dependencia',resolve(target,second_id))
    assert read(target)['estado']=='capturada' and read(target)['estado_antes_bloqueio'] is None
    assert read(target)['impedimentos']['dependencias_pendentes']==1
    assert post('validar_conclusao',complete(target))[0][0]==422
    # Código entregue pelo executor não conclui provedor nem resolve dependência.
    ok('registrar_relato',{'registro_id':provider,'versao_esperada':version(provider),'entregue':'Codificação concluída','restante':'Teste final'},)
    assert read(provider)['estado']=='capturada'
    assert post('resolver_dependencia',resolve(target,internal_id))[0][0]==422
    assert post('validar_conclusao',complete(provider),profile='executor')[0][0]==403
    assert post('validar_conclusao',{**complete(provider),'modo':'verificacao'})[0][0]==422
    assert post('validar_conclusao',{**complete(provider),'criterio_atendido':False})[0][0]==400
    assert post('validar_conclusao',complete(task('Sem critério',criterion=False)))[0][0]==422
    assert post('validar_conclusao',complete(task('Sem responsável',owner=False)))[0][0]==422
    done,_=ok('validar_conclusao',complete(provider))
    assert done['resultado']['registro']['estado']=='concluida'
    assert done['resultado']['validacao']['modo']=='aceite_humano'
    assert read(provider)['validacoes'][0]['modo']=='aceite_humano'
    assert read(provider)['validacoes'][0]['versao_registro']==version(provider)
    ok('resolver_dependencia',resolve(target,internal_id))
    assert read(target)['estado']=='capturada'
    assert read(target)['impedimentos']['dependencias_pendentes']==0
    # Aceite é explícito e recuperável após perda de confirmação.
    from nucleo import Falha
    with patch.object(service,'get_operation',side_effect=Falha(503,'SERVICO_INDISPONIVEL','Falha simulada')):
        (status,_),lost=post('validar_conclusao',complete(target))
    assert status==503
    recovered=call(p+'/operacoes/'+lost['operacao_id'])
    assert recovered[0]==200 and recovered[1]['resultado']['registro']['estado']=='concluida'
    assert call(p+'/operacoes',body=lost,key=lost['operacao_id'])==recovered
    assert post('registrar_dependencia',dep(target))[0][0]==422
    assert post('validar_conclusao',complete(target))[0][0]==422

    # Subtarefas necessárias e dependências formam a mesma cadeia de entrega.
    parent=task('Entrega total sintética');child=task('Subtarefa necessária sintética')
    with service.connect() as conn:
        conn.execute("INSERT INTO vinculos_registros(portfolio,origem,destino,relacao) VALUES('demo_escritorio',%s,%s,'parte_de')",(child,parent))
    assert post('registrar_dependencia',dep(child,provedor_id=parent))[0][0]==422
    assert post('validar_conclusao',complete(parent))[0][0]==422
    ok('validar_conclusao',complete(child))
    ok('validar_conclusao',complete(parent))

    # Duas propostas opostas concorrentes não podem criar um ciclo.
    a,b=task('Ciclo concorrente A'),task('Ciclo concorrente B')
    requests=[{'operacao_id':str(uuid.uuid4()),'comando':'registrar_dependencia','dados':dep(a,provedor_id=b)}, {'operacao_id':str(uuid.uuid4()),'comando':'registrar_dependencia','dados':dep(b,provedor_id=a)}]
    with ThreadPoolExecutor(max_workers=2) as pool:
        outcomes=list(pool.map(lambda body:call(p+'/operacoes',body=body,key=body['operacao_id']),requests))
    assert sorted(x[0] for x in outcomes)==[200,422],outcomes
    rejected=next(x for x in outcomes if x[0]==422)
    assert rejected[1]['codigo']=='DEPENDENCIA_CICLICA'
    # Conflito de versão na resolução impede sobrescrever outro acompanhamento.
    c=task('Resolução concorrente')
    blocking,_=ok('registrar_dependencia',dep(c,True))
    data=resolve(c,blocking['resultado']['dependencia']['id'])
    bodies=[{'operacao_id':str(uuid.uuid4()),'comando':'resolver_dependencia','dados':data} for _ in range(2)]
    with ThreadPoolExecutor(max_workers=2) as pool:
        outcomes=list(pool.map(lambda body:call(p+'/operacoes',body=body,key=body['operacao_id']),bodies))
    assert sorted(x[0] for x in outcomes)==[200,409]
    assert read(c)['estado']=='capturada'
    print('PASSOU: dependência sem bloquear avanço, múltiplos bloqueios, retomada, acompanhamento, autoria, evidência íntegra, provedor parcial, ciclos concorrentes e aceite humano recuperável.')
