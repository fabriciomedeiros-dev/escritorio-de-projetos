"""Reuniões locais: fontes verificadas, revisões imutáveis e efeitos transacionais.
O agente propõe; apenas pedidos explícitos do gestor decidem versões exatas.
"""
import json
import uuid
from psycopg.types.json import Jsonb

COMANDOS = {'receber_reuniao', 'propor_topicos_reuniao', 'aprovar_topicos_reuniao', 'efetivar_topicos_reuniao'}


def error(status, code, message):
    from nucleo import Falha
    raise Falha(status, code, message)


def header(conn, p, lote, version=None):
    query = 'SELECT to_jsonb(pr) AS item FROM propostas pr WHERE portfolio=%s AND id=%s AND lote=%s AND tipo=\'ata_resumida\''
    params = [p, lote, lote]
    if version is not None:
        query += ' AND versao=%s'
        params.append(version)
    row = conn.execute(query+' ORDER BY versao DESC LIMIT 1', params).fetchone()
    if not row:
        error(404, 'NAO_ENCONTRADO', 'Reunião não encontrada no escopo.')
    return row['item']


def snapshot(service, conn, p, actor, role, lote, version=None):
    if role != 'gestor':
        error(403, 'SEM_PERMISSAO', 'Revisão de reunião reservada ao gestor no piloto.')
    h = header(conn, p, lote, version)
    original = conn.execute('SELECT original FROM lotes WHERE portfolio=%s AND id=%s', (p, lote)).fetchone()['original']
    a = service.artifact(conn, p, str(original), actor, role)
    try:
        service.artifact(conn, p, str(original), actor, role, verified=True)
        integrity = 'verificada'
    except Exception as exc:
        from nucleo import Falha
        if not isinstance(exc, Falha):
            raise
        integrity = 'indisponivel_ou_divergente'
    decisions = {str(x['proposta']): x['item'] for x in conn.execute(
        'SELECT proposta,to_jsonb(a) AS item FROM aprovacoes a WHERE portfolio=%s AND versao_proposta=%s AND proposta IN (SELECT id FROM propostas WHERE portfolio=%s AND lote=%s AND versao=%s)',
        (p, h['versao'], p, lote, h['versao']))}
    topics = []
    for id_ in h['conteudo']['topicos']:
        row = conn.execute('SELECT to_jsonb(pr) AS item FROM propostas pr WHERE portfolio=%s AND lote=%s AND id=%s AND versao=%s', (p, lote, id_, h['versao'])).fetchone()
        if not row:
            error(503, 'SERVICO_INDISPONIVEL', 'Revisão incompleta; não confirmar reunião.')
        item = row['item']
        item['aprovacao'] = decisions.get(id_)
        item['efetivacao'] = next((x['item'] for x in conn.execute('SELECT to_jsonb(e) AS item FROM efetivacoes e WHERE portfolio=%s AND proposta=%s AND versao_proposta=%s', (p, id_, h['versao']))), None)
        topics.append(item)
    applied = conn.execute("SELECT id,resultado FROM operacoes WHERE portfolio=%s AND comando='efetivar_topicos_reuniao' AND pedido->'dados'->>'lote_id'=%s AND (pedido->'dados'->>'versao_esperada')::int=%s AND persistencia IN ('persistida','verificada') ORDER BY criada_em LIMIT 1", (p, lote, h['versao'])).fetchone()
    pending = sum(x['aprovacao'] is None for x in topics)
    ata_decision = decisions.get(lote)
    reviewed = bool(topics) and pending == 0 and ata_decision is not None
    return {'lote_id': lote, 'versao': h['versao'], **h['conteudo'], 'original': service.artifact_metadata(a),
            'integridade_original': integrity, 'aprovacao_ata': ata_decision, 'topicos': topics,
            'total_topicos': len(topics), 'topicos_pendentes': pending,
            'situacao': 'efetivada' if applied else 'revisada' if reviewed else 'aguardando_revisao' if topics else 'fonte_recebida',
            'operacao_efetivacao': str(applied['id']) if applied else None,
            'efeitos': applied['resultado']['resultado'].get('efeitos', []) if applied else [],
            'protecao': 'pendente'}


def original_verified(service, conn, p, actor, role, lote):
    row = conn.execute('SELECT original FROM lotes WHERE portfolio=%s AND id=%s', (p, lote)).fetchone()
    if not row:
        error(404, 'NAO_ENCONTRADO', 'Reunião não encontrada no escopo.')
    return service.artifact(conn, p, str(row['original']), actor, role, verified=True)


def check_location(raw, loc):
    # A referência é verificável sem inferir timestamps/nomes pela IA.
    try:
        text = raw.decode('utf-8')
        if 'ponteiro_json' in loc:
            value = json.loads(text)
            pointer = loc['ponteiro_json']
            if pointer:
                if not pointer.startswith('/'):
                    raise ValueError()
                for part in pointer[1:].split('/'):
                    part = part.replace('~1', '/').replace('~0', '~')
                    value = value[int(part)] if isinstance(value, list) else value[part]
            text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
        if loc['trecho'] not in text:
            raise ValueError()
    except (UnicodeError, ValueError, KeyError, IndexError, TypeError):
        error(422, 'FONTE_NAO_VERIFICADA', 'Trecho ou ponteiro não encontrado no original; revisar a referência.')


def apply(service, conn, p, actor, role, op, command, d, result):
    if command == 'receber_reuniao':
        a = service.artifact(conn, p, d['original_id'], actor, role, verified=True)
        origin = d['origem_reuniao']
        # Proveniência, não título, identifica a fonte. Nova fonte/hash não herda aprovação.
        prior = conn.execute("SELECT pr.lote,a.sha256,pr.conteudo FROM propostas pr JOIN lotes l ON (l.portfolio,l.id)=(pr.portfolio,pr.lote) JOIN artefatos a ON (a.portfolio,a.id)=(l.portfolio,l.original) WHERE pr.portfolio=%s AND pr.tipo='ata_resumida' AND pr.versao=1 AND pr.conteudo->'origem_reuniao'=%s", (p, Jsonb(origin))).fetchall()
        equal = next((x for x in prior if x['sha256'] == a['sha256']), None)
        if equal:
            for key in ('titulo', 'data_reuniao', 'local'):
                if equal['conteudo'].get(key) != d.get(key):
                    error(409, 'REPETICAO_DIVERGENTE', 'Fonte já recebida com outros metadados; corrigir por nova revisão.')
            lote = str(equal['lote'])
        else:
            lote = str(uuid.uuid4())
            conn.execute('INSERT INTO lotes(portfolio,id,original) VALUES(%s,%s,%s)', (p, lote, a['id']))
            content = {'titulo': d.get('titulo'), 'data_reuniao': d.get('data_reuniao'), 'local': d.get('local'),
                       'origem_reuniao': origin, 'fontes_anteriores': [str(x['lote']) for x in prior],
                       'ata_resumida': None, 'topicos': []}
            conn.execute("INSERT INTO propostas(portfolio,id,versao,lote,tipo,conteudo,localizacao_fonte) VALUES(%s,%s,1,%s,'ata_resumida',%s,'{}')", (p, lote, lote, Jsonb(content)))
        result['resultado'] = {'reuniao': snapshot(service, conn, p, actor, role, lote)}
        result['lacunas'] = ['Ata e tópicos ainda não propostos', 'Conteúdo importado não é autorização de execução']
        return result

    lote = d['lote_id']
    h = header(conn, p, lote)
    a = original_verified(service, conn, p, actor, role, lote)
    if h['versao'] != d['versao_esperada']:
        error(409, 'VERSAO_DIVERGENTE', 'Reunião mudou; consultar a revisão atual antes de decidir.')
    current = snapshot(service, conn, p, actor, role, lote)
    if command == 'propor_topicos_reuniao':
        if current['situacao'] == 'efetivada':
            error(409, 'VERSAO_DIVERGENTE', 'Reunião já efetivada; registrar complemento separado, sem reaplicar ações.')
        ids = [t['proposta_id'] for t in d['topicos']]
        if len(ids) != len(set(ids)) or lote in ids:
            error(400, 'PEDIDO_INVALIDO', 'Identificadores de tópicos duplicados ou reservados.')
        if not set(h['conteudo']['topicos']).issubset(ids):
            error(422, 'PEDIDO_INVALIDO', 'Correção deve preservar todos os tópicos; rejeitar explicitamente os excluídos.')
        version = h['versao'] + 1
        for topic in d['topicos']:
            other = conn.execute('SELECT lote FROM propostas WHERE portfolio=%s AND id=%s LIMIT 1', (p, topic['proposta_id'])).fetchone()
            if other and str(other['lote']) != lote:
                error(409, 'VERSAO_DIVERGENTE', 'Tópico pertence a outra reunião.')
            check_location(service.check_object(p, a), topic['localizacao_fonte'])
            action = topic['conteudo']['acao']
            if topic['conteudo'].get('destino_id'):
                service.record(conn, p, topic['conteudo']['destino_id'], actor, role)
            if action['comando'] != 'sem_acao':
                payload = action['dados']
                if 'registro_id' in payload:
                    service.record(conn, p, payload['registro_id'], actor, role)
                if payload.get('responsavel_total'):
                    service.member(conn, p, payload['responsavel_total'])
            conn.execute('INSERT INTO propostas(portfolio,id,versao,lote,tipo,conteudo,localizacao_fonte) VALUES(%s,%s,%s,%s,%s,%s,%s)', (p, topic['proposta_id'], version, lote, topic['tipo'], Jsonb(topic['conteudo']), Jsonb(topic['localizacao_fonte'])))
        content = {**h['conteudo'], **d.get('metadados', {}), 'ata_resumida': d['ata_resumida'], 'topicos': ids}
        conn.execute("INSERT INTO propostas(portfolio,id,versao,lote,tipo,conteudo,localizacao_fonte) VALUES(%s,%s,%s,%s,'ata_resumida',%s,'{}')", (p, lote, version, lote, Jsonb(content)))

    elif command == 'aprovar_topicos_reuniao':
        if not current['topicos']:
            error(422, 'APROVACAO_PENDENTE', 'Propor ata e tópicos antes da revisão.')
        ids = [x['proposta_id'] for x in d['itens']]
        if len(ids) != len(set(ids)):
            error(400, 'PEDIDO_INVALIDO', 'Decisões duplicadas no mesmo pedido.')
        valid = {lote, *h['conteudo']['topicos']}
        for item in d['itens']:
            if item['proposta_id'] not in valid or item['versao'] != h['versao']:
                error(409, 'VERSAO_DIVERGENTE', 'Decisão exige tópico e versão da revisão atual.')
            old = conn.execute('SELECT decisao,justificativa FROM aprovacoes WHERE portfolio=%s AND proposta=%s AND versao_proposta=%s', (p, item['proposta_id'], h['versao'])).fetchone()
            if old:
                if old['decisao'] != item['decisao'] or old['justificativa'] != item.get('justificativa'):
                    error(409, 'VERSAO_DIVERGENTE', 'Decisão já registrada; criar nova revisão para corrigi-la.')
                continue
            conn.execute('INSERT INTO aprovacoes(portfolio,proposta,versao_proposta,decisor,decisao,operacao,justificativa) VALUES(%s,%s,%s,%s,%s,%s,%s)', (p, item['proposta_id'], h['versao'], actor, item['decisao'], op, item.get('justificativa')))

    elif command == 'efetivar_topicos_reuniao':
        if current['situacao'] == 'efetivada':
            result['resultado'] = {'reuniao': current, 'efeitos': current['efeitos'], 'ja_efetivada': True}
            return result
        if current['topicos_pendentes'] or not current['topicos'] or not current['aprovacao_ata'] or current['aprovacao_ata']['decisao'] != 'aprovada':
            error(422, 'APROVACAO_PENDENTE', 'Todos os tópicos devem ser revisados e a ata aprovada antes de aplicar ações.')
        effects = []
        for topic in current['topicos']:
            if topic['aprovacao']['decisao'] == 'rejeitada':
                effects.append({'proposta_id': topic['id'], 'situacao': 'rejeitada', 'registros': []})
                continue
            action = topic['conteudo']['acao']
            if action['comando'] == 'sem_acao':
                effects.append({'proposta_id': topic['id'], 'situacao': 'registrada_sem_acao', 'registros': []})
                continue
            data = dict(action['dados'])
            if action['comando'] == 'criar_registro':
                entry = service.apply(conn, p, actor, role, op, 'capturar_entrada', {
                    'artefato_id': str(a['id']), 'texto': topic['conteudo']['resumo'],
                    'origem': {'lote_id': lote, 'proposta_id': topic['id'], 'versao': h['versao']}})
                data['origem_entrada_id'] = entry['resultado']['entrada_id']
            inner = service.apply(conn, p, actor, role, op, action['comando'], data)
            ref = inner['registros'][0]
            before = service.snapshot(conn, p, ref['id'], actor, role)
            # Vincula o original e a aprovação exata; nunca tratar reunião como evidência de entrega.
            conn.execute("INSERT INTO fontes(portfolio,registro,artefato,finalidade,localizacao) VALUES(%s,%s,%s,'origem',%s) ON CONFLICT DO NOTHING", (p, ref['id'], a['id'], Jsonb({'lote_id': lote, 'proposta_id': topic['id'], 'versao': h['versao'], **topic['localizacao_fonte']})))
            conn.execute('INSERT INTO efetivacoes(portfolio,proposta,versao_proposta,operacao,registro) VALUES(%s,%s,%s,%s,%s)', (p, topic['id'], h['versao'], op, ref['id']))
            if topic['conteudo'].get('destino_id'):
                target = service.record(conn, p, topic['conteudo']['destino_id'], actor, role)
                relation = 'parte_de' if before['tipo'] == 'tarefa' and target['tipo'] == 'projeto' else 'relacionado'
                if target['id'] == ref['id']:
                    error(422, 'PEDIDO_INVALIDO', 'Destino não pode ser o próprio registro.')
                conn.execute('INSERT INTO vinculos_registros(portfolio,origem,destino,relacao) VALUES(%s,%s,%s,%s) ON CONFLICT DO NOTHING', (p, ref['id'], target['id'], relation))
            after = service.snapshot(conn, p, ref['id'], actor, role)
            conn.execute('INSERT INTO historico(portfolio,registro,operacao,ator,acao,antes,depois,motivo,fonte) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)', (p, ref['id'], op, actor, 'encaminhamento_reuniao', Jsonb(before), Jsonb(after), 'Aplicação da revisão explicitamente aprovada', Jsonb({'lote_id': lote, 'proposta_id': topic['id'], 'versao_proposta': h['versao'], 'destino_id': topic['conteudo'].get('destino_id')})))
            result['registros'].extend(inner['registros'])
            effects.append({'proposta_id': topic['id'], 'situacao': 'aplicada', 'registros': inner['registros']})
        result['resultado']['efeitos'] = effects
    result['resultado']['reuniao'] = snapshot(service, conn, p, actor, role, lote)
    if command == 'efetivar_topicos_reuniao':
        result['resultado']['reuniao'].update(situacao='efetivada', operacao_efetivacao=op, efeitos=result['resultado']['efeitos'])
    result['fontes'] = [service.artifact_metadata(a)]
    return result


def verify(service, conn, p, actor, role, result):
    meeting = result['resultado'].get('reuniao')
    if not meeting:
        return
    original_verified(service, conn, p, actor, role, meeting['lote_id'])
    actual = snapshot(service, conn, p, actor, role, meeting['lote_id'], meeting['versao'])
    for key in ('ata_resumida', 'origem_reuniao', 'total_topicos', 'titulo', 'data_reuniao', 'local'):
        if actual[key] != meeting[key]:
            error(503, 'SERVICO_INDISPONIVEL', 'Revisão aguarda reconciliação.')
    if meeting['aprovacao_ata'] and meeting['aprovacao_ata'] != actual['aprovacao_ata']:
        error(503, 'SERVICO_INDISPONIVEL', 'Aprovação da ata aguarda reconciliação.')
    for effect in result['resultado'].get('efeitos', []):
        if effect['situacao'] == 'aplicada':
            row = conn.execute('SELECT registro FROM efetivacoes WHERE portfolio=%s AND proposta=%s AND versao_proposta=%s', (p, effect['proposta_id'], meeting['versao'])).fetchone()
            if not row or row['registro'] != effect['registros'][0]['id']:
                error(503, 'SERVICO_INDISPONIVEL', 'Efeito aguarda reconciliação.')
    for expected, saved in zip(meeting['topicos'], actual['topicos']):
        for key in ('id', 'conteudo', 'localizacao_fonte', 'versao'):
            if expected[key] != saved[key]:
                error(503, 'SERVICO_INDISPONIVEL', 'Tópico aguarda reconciliação.')
        if expected['aprovacao'] and expected['aprovacao'] != saved['aprovacao']:
            error(503, 'SERVICO_INDISPONIVEL', 'Aprovação aguarda reconciliação.')
