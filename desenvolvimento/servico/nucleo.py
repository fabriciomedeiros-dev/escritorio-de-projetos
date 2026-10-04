"""Núcleo do piloto local. Nenhum acesso ao SuperSync."""
import base64
import hashlib
import hmac
import json
from pathlib import Path
import sys
import uuid
from datetime import date

import psycopg
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb
from psycopg import sql
from jsonschema import Draft202012Validator, FormatChecker
from objetos import Objetos, MAX_BYTES

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'local'))
import ambiente
ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / '.runtime' / 'servico' / 'config.local.json'
API = json.loads((ROOT / 'desenvolvimento/contratos/openapi.json').read_text())
VALIDATOR = Draft202012Validator({'components': API['components'], 'allOf': [API['components']['schemas']['Pedido']]}, format_checker=FormatChecker())
IMPLEMENTADOS = {'capturar_entrada', 'criar_registro', 'registrar_relato', 'atualizar_registro', 'preparar_artefato', 'enviar_artefato', 'verificar_artefato', 'vincular_artefato'}


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)


class Falha(Exception):
    def __init__(self, status, codigo, mensagem):
        self.status, self.codigo, self.mensagem = status, codigo, mensagem
        super().__init__(mensagem)


class Servico:
    def __init__(self, config=None, database=None, objetos=None):
        self.config = config or json.loads(CONFIG.read_text())
        self.database = database
        self.objetos = Objetos(objetos or ROOT / '.runtime/servico/objetos')

    def artifact(self,conn,p,id_,actor,role,verified=False):
        row=conn.execute('SELECT * FROM artefatos WHERE portfolio=%s AND id=%s',(p,id_)).fetchone()
        if not row:
            raise Falha(404,'NAO_ENCONTRADO','Artefato não encontrado no escopo.')
        if role!='gestor' and str(row['remetente'])!=actor:
            sources=conn.execute('SELECT registro FROM fontes WHERE portfolio=%s AND artefato=%s',(p,id_)).fetchall()
            accessible=False
            for source in sources:
                try: self.record(conn,p,source['registro'],actor,role);accessible=True;break
                except Falha: pass
            if not accessible: raise Falha(404,'NAO_ENCONTRADO','Artefato não encontrado no escopo.')
        if verified:
            if row['estado']!='verificado': raise Falha(422,'FONTE_NAO_VERIFICADA','Original ainda não verificado.')
            self.check_object(p,row)
        return row

    def check_object(self,p,row):
        try: data=self.objetos.read(p,str(row['id']))
        except (OSError,ValueError): raise Falha(422,'FONTE_NAO_VERIFICADA','Original ausente ou indisponível; não confirmar integridade.')
        if len(data)!=row['bytes'] or hashlib.sha256(data).hexdigest()!=row['sha256']:
            raise Falha(422,'FONTE_NAO_VERIFICADA','Original diverge do tamanho ou checksum registrado.')
        return data

    def artifact_metadata(self,row):
        return {k:(v.isoformat() if hasattr(v,'isoformat') else str(v) if isinstance(v,uuid.UUID) else v) for k,v in row.items() if k!='chave_objeto'}

    def download(self,p,actor,id_):
        with self.connect() as conn:
            role=self.member(conn,p,actor)
            row=self.artifact(conn,p,id_,actor,role,verified=True)
            return self.check_object(p,row)

    def connect(self):
        env = ambiente.connection()
        return psycopg.connect(host=env['PGHOST'], port=env['PGPORT'], dbname=self.database or env['PGDATABASE'],
                              user='escritorio_api_local', password=self.config['senha_banco'],
                              row_factory=dict_row, connect_timeout=5,
                              options='-c search_path=escritorio,pg_catalog -c statement_timeout=10000')

    def identity(self, token):
        digest = hashlib.sha256(token.encode()).hexdigest()
        for entry in self.config['tokens']:
            if hmac.compare_digest(digest, entry['hash']):
                return entry['pessoa']
        raise Falha(401, 'NAO_AUTENTICADO', 'Credencial local ausente ou inválida.')

    def member(self, conn, portfolio, actor):
        row = conn.execute('SELECT papel FROM membros WHERE portfolio=%s AND pessoa=%s AND ativo', (portfolio, actor)).fetchone()
        if not row:
            raise Falha(403, 'SEM_PERMISSAO', 'Sem acesso ao portfólio.')
        return row['papel']

    def record(self, conn, portfolio, id_, actor, role):
        row = conn.execute('SELECT to_jsonb(r) AS item FROM registros r WHERE portfolio=%s AND id=%s', (portfolio, id_)).fetchone()
        if not row:
            raise Falha(404, 'NAO_ENCONTRADO', 'Registro não encontrado no escopo.')
        r = row['item']
        if role == 'executor' and r['responsavel_total'] != actor:
            assigned = conn.execute('SELECT 1 FROM executores WHERE portfolio=%s AND tarefa=%s AND pessoa=%s', (portfolio, id_, actor)).fetchone()
            if not assigned:
                raise Falha(404, 'NAO_ENCONTRADO', 'Registro não encontrado no escopo.')
        return r

    def snapshot(self, conn, portfolio, id_, actor, role):
        r = self.record(conn, portfolio, id_, actor, role)
        # Referências validadas pelo serviço; o vínculo não depende do histórico do chat.
        ids = [r['origem'].get('entrada_id'), *r['origem'].get('entradas_complementares', [])]
        r['entradas'] = []
        for entrada_id in dict.fromkeys(x for x in ids if x):
            entry = conn.execute('SELECT to_jsonb(e) AS item FROM entradas e WHERE portfolio=%s AND id=%s', (portfolio, entrada_id)).fetchone()
            if entry:
                r['entradas'].append(entry['item'])
        r['fontes'] = [x['item'] for x in conn.execute('SELECT to_jsonb(f) AS item FROM fontes f WHERE portfolio=%s AND registro=%s', (portfolio, id_))]
        for source in r['fontes']:
            artifact=self.artifact(conn,portfolio,source['artefato'],actor,role)
            source['artefato_detalhes']=self.artifact_metadata(artifact)
            try:
                self.check_object(portfolio,artifact)
                source['integridade']='verificada' if artifact['estado']=='verificado' else 'pendente'
            except Falha: source['integridade']='indisponivel_ou_divergente'
        r['dependencias'] = [x['item'] for x in conn.execute('SELECT to_jsonb(d) AS item FROM dependencias d WHERE portfolio=%s AND entrega=%s', (portfolio, id_))]
        r['atualizacoes'] = [x['item'] for x in conn.execute('SELECT to_jsonb(a) AS item FROM atualizacoes a WHERE portfolio=%s AND registro=%s ORDER BY criada_em DESC,id DESC LIMIT 25', (portfolio, id_))]
        r['lacunas'] = [label for field, label in [('responsavel_total','Responsável não definido'), ('prazo_aceito','Prazo não aceito'), ('esforco_restante','Esforço restante não informado')] if r[field] is None]
        return r

    def operation(self, portfolio, actor, key, pedido):
        if not key or len(key) > 200:
            raise Falha(400, 'PEDIDO_INVALIDO', 'Idempotency-Key obrigatório, até 200 caracteres.')
        if not VALIDATOR.is_valid(pedido):
            raise Falha(400, 'PEDIDO_INVALIDO', 'Pedido não atende ao contrato JSON.')
        command, data, op = pedido['comando'], pedido['dados'], str(uuid.UUID(pedido['operacao_id']))
        digest = hashlib.sha256(canonical({'contrato':'2.0.0','pedido':pedido}).encode()).hexdigest()
        with self.connect() as conn:
            conn.execute('SELECT pg_advisory_xact_lock(hashtextextended(%s,0))', (portfolio,))
            role = self.member(conn, portfolio, actor)
            old = conn.execute('SELECT * FROM operacoes WHERE portfolio=%s AND (id=%s OR (ator=%s AND chave_repeticao=%s))', (portfolio,op,actor,key)).fetchall()
            if old:
                if len(old)!=1 or str(old[0]['id'])!=op or str(old[0]['ator'])!=actor or old[0]['chave_repeticao']!=key or old[0]['hash_pedido']!=digest:
                    raise Falha(409,'REPETICAO_DIVERGENTE','Identificador/chave já usados para outro pedido.')
            else:
                if command not in IMPLEMENTADOS:
                    raise Falha(422,'PEDIDO_INVALIDO','Comando ainda não disponível no piloto local.')
                if role=='consulta' or (command != 'registrar_relato' and role!='gestor'):
                    raise Falha(403,'SEM_PERMISSAO','Perfil sem autorização para esse comando.')
                conn.execute('INSERT INTO operacoes(portfolio,id,ator,chave_repeticao,hash_pedido,comando,pedido) VALUES(%s,%s,%s,%s,%s,%s,%s)', (portfolio,op,actor,key,digest,command,Jsonb(pedido)))
                result = self.apply(conn,portfolio,actor,role,op,command,data)
                conn.execute("UPDATE operacoes SET persistencia='persistida',resultado=%s WHERE portfolio=%s AND id=%s", (Jsonb(result),portfolio,op))
        # Nova conexão/read-after-commit. Em falha, consulta por operação permite retomada.
        return self.get_operation(portfolio,actor,op)

    def apply(self, conn, p, actor, role, op, command, d):
        result = {'operacao_id':op,'portfolio':p,'estado':'persistida','protecao':'pendente','registros':[], 'lacunas':[],'fontes':[],'verificada_em':None,'resultado':{}}
        if command=='preparar_artefato':
            id_=str(uuid.uuid4())
            conn.execute('INSERT INTO artefatos(portfolio,id,nome,tipo_midia,chave_objeto,sha256,bytes,origem,remetente) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)',(p,id_,d['nome'],d['tipo_midia'],id_,d['sha256_esperado'],d['bytes_esperados'],Jsonb(d['origem']),actor))
            row=self.artifact(conn,p,id_,actor,role)
            result['resultado']={'artefato':self.artifact_metadata(row)}
            result['lacunas']=['Arquivo preparado; envio e verificação do original pendentes']
            return result
        if command in ('enviar_artefato','verificar_artefato'):
            row=self.artifact(conn,p,d['artefato_id'],actor,role)
            if command=='enviar_artefato':
                try: data=base64.b64decode(d['conteudo_base64'],validate=True)
                except ValueError: raise Falha(400,'PEDIDO_INVALIDO','Conteúdo base64 inválido.')
                if len(data)>MAX_BYTES or len(data)!=row['bytes'] or hashlib.sha256(data).hexdigest()!=row['sha256']:
                    raise Falha(422,'FONTE_NAO_VERIFICADA','Arquivo enviado diverge do tamanho ou checksum esperado.')
                try: self.objetos.save(p,str(row['id']),data)
                except ValueError: raise Falha(422,'FONTE_NAO_VERIFICADA','Objeto existente diverge; não sobrescrever original.')
            self.check_object(p,row)
            conn.execute("UPDATE artefatos SET estado='verificado',verificado_em=clock_timestamp() WHERE portfolio=%s AND id=%s",(p,row['id']))
            result['resultado']={'artefato':self.artifact_metadata(self.artifact(conn,p,str(row['id']),actor,role))}
            return result
        if command=='capturar_entrada':
            if 'artefato_id' in d:
                self.artifact(conn,p,d['artefato_id'],actor,role,verified=True)
            id_ = str(uuid.uuid4())
            conn.execute("INSERT INTO entradas(portfolio,id,operacao,conteudo,artefato,origem,classificacao_proposta,estado) VALUES(%s,%s,%s,%s,%s,%s,%s,'triagem_pendente')", (p,id_,op,d.get('texto'),d.get('artefato_id'),Jsonb(d['origem']),d.get('classificacao_sugerida')))
            result['resultado']={'entrada_id':id_,'classificacao_confirmada':None,'entrada':{'id':id_,'texto':d.get('texto'),'artefato_id':d.get('artefato_id'),'origem':d['origem'],'classificacao_sugerida':d.get('classificacao_sugerida')}}
            result['lacunas']=['Classificação pendente; entrada ainda não vinculada a registro']
            return result
        if command=='criar_registro':
            if d['tipo']=='projeto' or 'decisao_promocao_id' in d:
                raise Falha(422,'APROVACAO_PENDENTE','Promoção a projeto não implementada no piloto.')
            if 'origem_entrada_id' in d:
                entry=conn.execute('SELECT estado,origem,artefato FROM entradas WHERE portfolio=%s AND id=%s', (p,d['origem_entrada_id'])).fetchone()
                if not entry:
                    raise Falha(404,'NAO_ENCONTRADO','Entrada não encontrada no escopo.')
                if entry['estado']=='vinculada' or entry['origem'].get('registro_id'):
                    raise Falha(409,'ENTRADA_JA_VINCULADA','Entrada vinculada ou destinada a registro existente; não criar outro registro.')
            if d.get('responsavel_total') and not conn.execute('SELECT 1 FROM membros WHERE portfolio=%s AND pessoa=%s AND ativo', (p,d['responsavel_total'])).fetchone():
                raise Falha(422,'PEDIDO_INVALIDO','Responsável não é membro ativo do portfólio.')
            prefix={'tarefa':'TAR','solicitacao':'SOL','ideia':'IDE'}[d['tipo']]
            id_ = p.upper()+'-'+prefix+'-'+str(uuid.uuid4())
            conn.execute("INSERT INTO registros(portfolio,id,tipo,titulo,estado,responsavel_total,resultado_esperado,criterio_conclusao,prazo_proposto,meta,origem,criado_por) VALUES(%s,%s,%s,%s,'capturada',%s,%s,%s,%s,%s,%s,%s)", (p,id_,d['tipo'],d['titulo'],d.get('responsavel_total'),d.get('resultado_esperado'),d.get('criterio_conclusao'),d.get('prazo_proposto'),d.get('meta'),Jsonb({'entrada_id':d.get('origem_entrada_id')}),actor))
            if 'origem_entrada_id' in d:
                if entry['artefato']:
                    self.artifact(conn,p,str(entry['artefato']),actor,role,verified=True)
                    conn.execute("INSERT INTO fontes(portfolio,registro,artefato,finalidade) VALUES(%s,%s,%s,'origem')",(p,id_,entry['artefato']))
                conn.execute("UPDATE entradas SET estado='vinculada',classificacao_confirmada=%s WHERE portfolio=%s AND id=%s", (d['tipo'],p,d['origem_entrada_id']))
            before=None
            after=self.snapshot(conn,p,id_,actor,role)
        elif command=='vincular_artefato':
            id_=d['registro_id']
            before=self.snapshot(conn,p,id_,actor,role)
            if before['estado'] in ('concluida','cancelada','encerrado','promovida','arquivada'):
                raise Falha(422,'PEDIDO_INVALIDO','Vínculo exige registro aberto.')
            if before['versao']!=d['versao_esperada']:
                raise Falha(409,'VERSAO_DIVERGENTE','Registro mudou; consultar antes de vincular.')
            row=self.artifact(conn,p,d['artefato_id'],actor,role,verified=True)
            conn.execute('INSERT INTO fontes(portfolio,registro,artefato,finalidade) VALUES(%s,%s,%s,%s) ON CONFLICT DO NOTHING',(p,id_,row['id'],d['finalidade']))
            conn.execute('UPDATE registros SET versao=versao+1 WHERE portfolio=%s AND id=%s AND versao=%s',(p,id_,d['versao_esperada']))
            after=self.snapshot(conn,p,id_,actor,role)
        elif command=='atualizar_registro':
            id_=d['registro_id']
            before=self.snapshot(conn,p,id_,actor,role)
            if before['tipo'] not in ('ideia','solicitacao') or before['estado'] in ('promovida','arquivada','concluida','cancelada'):
                raise Falha(422,'PEDIDO_INVALIDO','Atualização de conteúdo exige ideia ou solicitação aberta.')
            if before['versao']!=d['versao_esperada']:
                raise Falha(409,'VERSAO_DIVERGENTE','Registro mudou; consultar antes de atualizar.')
            changes=dict(d.get('alteracoes',{}))
            if 'entrada_id' in d:
                entry=conn.execute('SELECT * FROM entradas WHERE portfolio=%s AND id=%s',(p,d['entrada_id'])).fetchone()
                if not entry:
                    raise Falha(404,'NAO_ENCONTRADO','Entrada não encontrada no escopo.')
                # Uma entrada já classificada não pode ser reatribuída silenciosamente.
                linked=[before['origem'].get('entrada_id'),*before['origem'].get('entradas_complementares',[])]
                if entry['estado']=='vinculada' and d['entrada_id'] not in linked:
                    raise Falha(409,'ENTRADA_JA_VINCULADA','Entrada já vinculada; não é possível reatribuir pelo piloto.')
                reference=entry['origem'].get('registro_id')
                if reference and reference!=id_:
                    raise Falha(409,'ENTRADA_DIVERGENTE','Entrada referencia outro registro.')
                origin=dict(before['origem'])
                complements=list(origin.get('entradas_complementares',[]))
                if d['entrada_id'] not in linked: complements.append(d['entrada_id'])
                origin['entradas_complementares']=complements
                changes['origem']=Jsonb(origin)
                if entry['artefato']:
                    self.artifact(conn,p,str(entry['artefato']),actor,role,verified=True)
                    conn.execute("INSERT INTO fontes(portfolio,registro,artefato,finalidade) VALUES(%s,%s,%s,'origem') ON CONFLICT DO NOTHING",(p,id_,entry['artefato']))
                conn.execute("UPDATE entradas SET estado='vinculada',classificacao_confirmada=%s WHERE portfolio=%s AND id=%s",(before['tipo'],p,d['entrada_id']))
            assignments=[sql.SQL('{}=%s').format(sql.Identifier(field)) for field in changes]
            query=sql.SQL('UPDATE registros SET {},versao=versao+1 WHERE portfolio=%s AND id=%s AND versao=%s').format(sql.SQL(',').join(assignments))
            conn.execute(query,(*changes.values(),p,id_,d['versao_esperada']))
            after=self.snapshot(conn,p,id_,actor,role)
        else:
            id_=d['registro_id']
            before=self.snapshot(conn,p,id_,actor,role)
            if before['tipo']!='tarefa' or before['estado'] in ('concluida','cancelada'):
                raise Falha(422,'PEDIDO_INVALIDO','Relato neste piloto exige tarefa aberta.')
            if before['versao']!=d['versao_esperada']:
                raise Falha(409,'VERSAO_DIVERGENTE','Registro mudou; consultar antes de atualizar.')
            if d.get('artefatos'):
                for artifact_id in d['artefatos']:
                    self.artifact(conn,p,artifact_id,actor,role,verified=True)
            conn.execute('INSERT INTO atualizacoes(portfolio,registro,operacao,remetente,autor_informado,entregue,restante,dificuldade,esforco_restante,prazo_proposto,fontes) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', (p,id_,op,actor,d.get('autor_informado'),d.get('entregue'),d.get('restante'),d.get('dificuldade'),d.get('esforco_restante'),d.get('prazo_proposto'),Jsonb(d.get('artefatos',[]))))
            # Informação do executor é proposta. Não aceita prazo nem altera estado implicitamente.
            conn.execute('UPDATE registros SET versao=versao+1,esforco_restante=CASE WHEN %s THEN %s ELSE esforco_restante END,prazo_proposto=CASE WHEN %s THEN %s ELSE prazo_proposto END WHERE portfolio=%s AND id=%s AND versao=%s', ('esforco_restante' in d,d.get('esforco_restante'),'prazo_proposto' in d,d.get('prazo_proposto'),p,id_,d['versao_esperada']))
            if d.get('artefatos'):
                for artifact_id in d['artefatos']:
                    conn.execute("INSERT INTO fontes(portfolio,registro,artefato,finalidade) VALUES(%s,%s,%s,'evidencia') ON CONFLICT DO NOTHING",(p,id_,artifact_id))
            after=self.snapshot(conn,p,id_,actor,role)
        conn.execute('INSERT INTO historico(portfolio,registro,operacao,ator,acao,antes,depois,motivo,fonte) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)', (p,id_,op,actor,command,Jsonb(before),Jsonb(after),d.get('motivo','Pedido explícito autorizado'),Jsonb({'operacao_id':op,'entrada_id':d.get('entrada_id')})))
        result['registros']=[{'id':id_,'versao':after['versao']}]
        result['lacunas']=after['lacunas']
        result['resultado']={'registro':after}
        return result

    def get_operation(self,p,actor,op):
        try: uuid.UUID(op)
        except (ValueError,TypeError): raise Falha(400,'PEDIDO_INVALIDO','ID de operação inválido.')
        with self.connect() as conn:
            conn.execute('SELECT pg_advisory_xact_lock(hashtextextended(%s,0))',(p,))
            role=self.member(conn,p,actor)
            row=conn.execute('SELECT * FROM operacoes WHERE portfolio=%s AND id=%s',(p,op)).fetchone()
            if not row or (str(row['ator'])!=actor and role!='gestor'):
                raise Falha(404,'NAO_ENCONTRADO','Operação não encontrada no escopo.')
            result=row['resultado']
            if result:
                artifact=result['resultado'].get('artefato')
                if artifact:
                    current=self.artifact(conn,p,artifact['id'],actor,role)
                    if row['comando'] in ('enviar_artefato','verificar_artefato'):
                        self.check_object(p,current)
                for ref in result['registros']:
                    for source in result['resultado']['registro'].get('fontes',[]):
                        self.artifact(conn,p,source['artefato'],actor,role,verified=True)
                captured=result['resultado'].get('entrada',{}).get('artefato_id')
                if captured: self.artifact(conn,p,captured,actor,role,verified=True)
            if result and role=='executor':
                for ref in result['registros']: self.record(conn,p,ref['id'],actor,role)
            if row['persistencia']=='persistida':
                for ref in result['registros']:
                    r=conn.execute('SELECT versao FROM registros WHERE portfolio=%s AND id=%s',(p,ref['id'])).fetchone()
                    h=conn.execute('SELECT 1 FROM historico WHERE portfolio=%s AND registro=%s AND operacao=%s',(p,ref['id'],op)).fetchone()
                    if not r or r['versao']<ref['versao'] or not h:
                        raise Falha(503,'SERVICO_INDISPONIVEL','Gravação aguarda reconciliação.')
                entrada=result['resultado'].get('entrada_id')
                if entrada and not conn.execute('SELECT 1 FROM entradas WHERE portfolio=%s AND id=%s AND operacao=%s',(p,entrada,op)).fetchone():
                    raise Falha(503,'SERVICO_INDISPONIVEL','Entrada aguarda reconciliação.')
                at=conn.execute('SELECT clock_timestamp() AS instante').fetchone()['instante'].isoformat()
                result={**result,'estado':'verificada','verificada_em':at}
                conn.execute("UPDATE operacoes SET persistencia='verificada',verificada_em=%s,resultado=%s WHERE portfolio=%s AND id=%s",(at,Jsonb(result),p,op))
            if result is None:
                raise Falha(503,'SERVICO_INDISPONIVEL','Operação ainda sem resultado reconciliado.')
            return {**result,'protecao':row['protecao']}

    def query(self,p,actor,filters):
        allowed={'id','tipo','estado','assunto','origem','cursor','desde','ate','limite'}
        if set(filters)-allowed:
            raise Falha(400,'PEDIDO_INVALIDO','Filtro desconhecido.')
        try:
            limit=int(filters.get('limite',25))
            assert 1<=limit<=100
            for field in ('desde','ate'):
                if field in filters: date.fromisoformat(filters[field])
        except (ValueError,TypeError,AssertionError): raise Falha(400,'PEDIDO_INVALIDO','Limite ou período inválido.')
        fingerprint=hashlib.sha256(canonical({k:v for k,v in filters.items() if k!='cursor'}).encode()).hexdigest()
        last=''
        if filters.get('cursor'):
            try:
                raw,signature=filters['cursor'].split('.')
                if not hmac.compare_digest(signature,hmac.new(self.config['cursor_secret'].encode(),raw.encode(),'sha256').hexdigest()): raise ValueError()
                state=json.loads(base64.urlsafe_b64decode(raw))
                if state['portfolio']!=p or state['ator']!=actor or state['filtro']!=fingerprint: raise ValueError()
                last=state['ultimo']
            except (ValueError,KeyError,TypeError): raise Falha(400,'PEDIDO_INVALIDO','Cursor inválido ou incompatível com a consulta.')
        with self.connect() as conn:
            role=self.member(conn,p,actor)
            clauses=['r.portfolio=%s','r.id>%s']; params=[p,last]
            if role=='executor':
                clauses.append('(r.responsavel_total=%s OR EXISTS(SELECT 1 FROM executores e WHERE e.portfolio=r.portfolio AND e.tarefa=r.id AND e.pessoa=%s))');params.extend([actor,actor])
            for name,column in [('id','id'),('tipo','tipo'),('estado','estado')]:
                if name in filters: clauses.append('r.'+column+'=%s');params.append(filters[name])
            for name,column in [('assunto','titulo'),('origem','origem::text')]:
                if name in filters:
                    if name=='assunto':
                        clauses.append('(r.titulo ILIKE %s OR r.resultado_esperado ILIKE %s)')
                        params.extend(['%'+filters[name]+'%']*2)
                    else:
                        clauses.append('r.'+column+' ILIKE %s');params.append('%'+filters[name]+'%')
            for name,operator in [('desde','>='),('ate','<=')]:
                if name in filters: clauses.append("(r.criado_em AT TIME ZONE 'America/Sao_Paulo')::date"+operator+'%s');params.append(filters[name])
            rows=conn.execute('SELECT r.id FROM registros r WHERE '+' AND '.join(clauses)+' ORDER BY r.id LIMIT %s',(*params,limit+1)).fetchall()
            items=[self.snapshot(conn,p,x['id'],actor,role) for x in rows[:limit]]
            cursor=None
            if len(rows)>limit:
                raw=base64.urlsafe_b64encode(canonical({'portfolio':p,'ator':actor,'filtro':fingerprint,'ultimo':items[-1]['id']}).encode()).decode()
                cursor=raw+'.'+hmac.new(self.config['cursor_secret'].encode(),raw.encode(),'sha256').hexdigest()
            return {'itens':items,'proximo_cursor':cursor}
