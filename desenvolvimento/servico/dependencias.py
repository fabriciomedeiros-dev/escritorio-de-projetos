"""Dependências, impedimentos e aceite humano no piloto local, sem produção."""
import uuid
from psycopg.types.json import Jsonb
from psycopg import sql

COMANDOS = {'registrar_dependencia', 'atualizar_dependencia', 'resolver_dependencia', 'validar_conclusao'}


def error(status, code, message):
    from nucleo import Falha
    raise Falha(status, code, message)


def dependency(conn, p, id_, record):
    row = conn.execute('SELECT to_jsonb(d) AS item FROM dependencias d WHERE portfolio=%s AND id=%s AND entrega=%s', (p, id_, record)).fetchone()
    if not row:
        error(404, 'NAO_ENCONTRADO', 'Dependência não encontrada na entrega e portfólio informados.')
    return row['item']


def active_member(service, conn, p, person):
    service.member(conn, p, person)


def cycle(conn, p, target, provider):
    # Entrega depende de provedor; pai depende de suas subtarefas necessárias.
    return conn.execute('''WITH RECURSIVE arestas(entrega,provedor) AS (
      SELECT entrega,provedor FROM dependencias WHERE portfolio=%s AND estado='pendente' AND provedor IS NOT NULL
      UNION SELECT v.destino,v.origem FROM vinculos_registros v JOIN registros r ON (r.portfolio,r.id)=(v.portfolio,v.origem)
        WHERE v.portfolio=%s AND v.relacao='parte_de' AND r.tipo='tarefa' AND r.estado<>'cancelada'
    ), alcance(id) AS (
      SELECT %s::text UNION SELECT a.provedor FROM arestas a JOIN alcance x ON a.entrega=x.id
    ) SELECT 1 FROM alcance WHERE id=%s LIMIT 1''', (p, p, provider, target)).fetchone() is not None


def apply(service, conn, p, actor, role, op, command, d, result):
    id_ = d['registro_id']
    before = service.snapshot(conn, p, id_, actor, role)
    if before['tipo'] != 'tarefa' or before['estado'] in ('concluida', 'cancelada'):
        error(422, 'PEDIDO_INVALIDO', 'Este incremento exige tarefa aberta; não altera fase de projeto.')
    if before['versao'] != d['versao_esperada']:
        error(409, 'VERSAO_DIVERGENTE', 'Entrega mudou; consultar a versão atual antes de registrar.')
    state, resume = before['estado'], before['estado_antes_bloqueio']
    prior_dependency = None
    dep = None
    evidence = None
    if command == 'registrar_dependencia':
        active_member(service, conn, p, d['responsavel_acao'])
        if d.get('provedor_id'):
            provider = service.record(conn, p, d['provedor_id'], actor, role)
            if provider['tipo'] != 'tarefa' or provider['estado'] == 'cancelada':
                error(422, 'PEDIDO_INVALIDO', 'Provedor interno deve ser tarefa não cancelada.')
            if cycle(conn, p, id_, provider['id']):
                error(422, 'DEPENDENCIA_CICLICA', 'Dependência criaria um ciclo de entregas.')
        duplicate = conn.execute("SELECT 1 FROM dependencias WHERE portfolio=%s AND entrega=%s AND estado='pendente' AND provedor IS NOT DISTINCT FROM %s AND terceiro IS NOT DISTINCT FROM %s AND criterio_resolucao=%s", (p, id_, d.get('provedor_id'), d.get('terceiro'), d['criterio_resolucao'])).fetchone()
        if duplicate:
            error(409, 'REPETICAO_DIVERGENTE', 'Dependência equivalente já aberta; consultar e atualizar o acompanhamento.')
        dep_id = str(uuid.uuid4())
        conn.execute("INSERT INTO dependencias(portfolio,id,entrega,provedor,terceiro,motivo,responsavel_acao,proxima_acao,acompanhar_em,criterio_resolucao,estado,impede_avanco) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'pendente',%s)", (p, dep_id, id_, d.get('provedor_id'), d.get('terceiro'), d['motivo'], d['responsavel_acao'], d['proxima_acao'], d['acompanhar_em'], d['criterio_resolucao'], d['impede_avanco']))
        if d['impede_avanco'] and state != 'bloqueada':
            resume, state = state, 'bloqueada'
        dep = dependency(conn, p, dep_id, id_)
    elif command in ('resolver_dependencia', 'atualizar_dependencia'):
        prior_dependency = dependency(conn, p, d['dependencia_id'], id_)
        if prior_dependency['estado'] != 'pendente':
            error(409, 'VERSAO_DIVERGENTE', 'Dependência já resolvida; não substituir a decisão anterior.')
        if command == 'atualizar_dependencia':
            changes = d['alteracoes']
            if 'responsavel_acao' in changes:
                active_member(service, conn, p, changes['responsavel_acao'])
            query = sql.SQL('UPDATE dependencias SET {} WHERE portfolio=%s AND id=%s').format(sql.SQL(',').join(sql.SQL('{}=%s').format(sql.Identifier(field)) for field in changes))
            conn.execute(query, (*changes.values(), p, d['dependencia_id']))
            if changes.get('impede_avanco') and state != 'bloqueada':
                resume, state = state, 'bloqueada'
            elif changes.get('impede_avanco') is False and state == 'bloqueada' and not conn.execute("SELECT 1 FROM dependencias WHERE portfolio=%s AND entrega=%s AND estado='pendente' AND impede_avanco", (p, id_)).fetchone():
                if resume is None:
                    error(409, 'VERSAO_DIVERGENTE', 'Estado anterior ao bloqueio desconhecido; não presumir retomada.')
                state, resume = resume, None
        else:
            evidence = service.artifact(conn, p, d['evidencia_id'], actor, role, verified=True)
            if prior_dependency['provedor']:
                provider = service.record(conn, p, prior_dependency['provedor'], actor, role)
                if provider['estado'] != 'concluida':
                    error(422, 'DEPENDENCIA_PENDENTE', 'Provedor interno não concluído; relato parcial não resolve a dependência.')
                # Evidências do provedor também devem permanecer recuperáveis.
                for source in service.snapshot(conn, p, provider['id'], actor, role)['fontes']:
                    if source['finalidade'] == 'evidencia':
                        service.artifact(conn, p, source['artefato'], actor, role, verified=True)
            conn.execute("UPDATE dependencias SET estado='resolvida' WHERE portfolio=%s AND id=%s", (p, d['dependencia_id']))
            conn.execute("INSERT INTO fontes(portfolio,registro,artefato,finalidade,localizacao) VALUES(%s,%s,%s,'evidencia',%s) ON CONFLICT DO NOTHING", (p, id_, evidence['id'], Jsonb({'dependencia_id': d['dependencia_id'], 'operacao_id': op})))
            if state == 'bloqueada' and not conn.execute("SELECT 1 FROM dependencias WHERE portfolio=%s AND entrega=%s AND estado='pendente' AND impede_avanco", (p, id_)).fetchone():
                if resume is None:
                    error(409, 'VERSAO_DIVERGENTE', 'Estado anterior ao bloqueio desconhecido; não presumir retomada.')
                state, resume = resume, None
        dep = dependency(conn, p, d['dependencia_id'], id_)
    elif command == 'validar_conclusao':
        if d['modo'] != 'aceite_humano':
            error(422, 'PEDIDO_INVALIDO', 'Validação automática não implementada; usar aceite humano explícito do gestor.')
        if not before['responsavel_total'] or not (before['criterio_conclusao'] or '').strip():
            error(422, 'EVIDENCIA_INSUFICIENTE', 'Conclusão exige responsável total e critério de conclusão definido.')
        active_member(service, conn, p, before['responsavel_total'])
        if before['estado'] == 'bloqueada' or any(x['estado'] == 'pendente' for x in before['dependencias']):
            error(422, 'DEPENDENCIA_PENDENTE', 'Entrega ainda tem bloqueio ou dependência necessária pendente.')
        child = conn.execute("SELECT 1 FROM vinculos_registros v JOIN registros r ON (r.portfolio,r.id)=(v.portfolio,v.origem) WHERE v.portfolio=%s AND v.destino=%s AND v.relacao='parte_de' AND r.tipo='tarefa' AND r.estado NOT IN ('concluida','cancelada') LIMIT 1", (p, id_)).fetchone()
        if child:
            error(422, 'DEPENDENCIA_PENDENTE', 'Subtarefa necessária ainda não concluída.')
        for artifact_id in d['artefatos']:
            evidence = service.artifact(conn, p, artifact_id, actor, role, verified=True)
            conn.execute("INSERT INTO fontes(portfolio,registro,artefato,finalidade) VALUES(%s,%s,%s,'evidencia') ON CONFLICT DO NOTHING", (p, id_, evidence['id']))
        state, resume = 'concluida', None
        conn.execute("INSERT INTO validacoes(portfolio,registro,versao_registro,validador,modo,parecer) VALUES(%s,%s,%s,%s,'aceite_humano',%s)", (p, id_, before['versao']+1, actor, d['parecer']))
    conn.execute('UPDATE registros SET estado=%s,estado_antes_bloqueio=%s,versao=versao+1 WHERE portfolio=%s AND id=%s AND versao=%s', (state, resume, p, id_, d['versao_esperada']))
    after = service.snapshot(conn, p, id_, actor, role)
    source = {'operacao_id': op, 'dependencia_antes': prior_dependency, 'dependencia_depois': dep}
    if evidence:
        source['evidencia_id'] = str(evidence['id'])
    conn.execute('INSERT INTO historico(portfolio,registro,operacao,ator,acao,antes,depois,motivo,fonte) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)', (p, id_, op, actor, command, Jsonb(before), Jsonb(after), d.get('justificativa') or d.get('motivo') or d.get('parecer'), Jsonb(source)))
    result['registros'] = [{'id': id_, 'versao': after['versao']}]
    result['resultado'] = {'registro': after}
    result['lacunas'] = after['lacunas']
    if dep:
        result['resultado']['dependencia'] = dep
    if command == 'validar_conclusao':
        result['resultado']['validacao'] = {'modo': 'aceite_humano', 'criterio_atendido': True, 'parecer': d['parecer'], 'artefatos': d['artefatos'], 'validador': actor, 'versao_registro': after['versao']}
    return result


def verify(conn, p, result):
    validation = result['resultado'].get('validacao')
    if not validation:
        return
    record = result['registros'][0]
    row = conn.execute('SELECT modo,parecer,validador FROM validacoes WHERE portfolio=%s AND registro=%s AND versao_registro=%s', (p, record['id'], record['versao'])).fetchone()
    if not row or row['modo'] != validation['modo'] or row['parecer'] != validation['parecer'] or str(row['validador']) != validation['validador']:
        error(503, 'SERVICO_INDISPONIVEL', 'Aceite aguarda reconciliação; não confirmar conclusão.')
