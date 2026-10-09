"""Ensaio isolado SAERJ. Não altera o piloto nem a autoridade documental."""
import argparse
import hashlib
import html
import json
import re
import sys
import tempfile
import uuid
from pathlib import Path
import ambiente

ROOT = ambiente.ROOT


def inventariar():
    fontes = {}
    registros = []
    for path in sorted((ROOT / 'portfolios/saerj').rglob('*.md')):
        if path.is_symlink():
            raise RuntimeError('Fonte simbólica recusada: ' + str(path))
        raw = path.read_bytes()
        fontes[path.relative_to(ROOT).as_posix()] = {
            'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': raw,
            'texto': raw.decode('utf-8-sig')}
    for path in sorted((ROOT / 'portfolios/saerj/projetos').glob('*/projeto.md')):
        rel = path.relative_to(ROOT).as_posix()
        text = fontes[rel]['texto']
        match = re.search(r'^\*\*ID:\*\*\s*(\S+)', text, re.M)
        id_ = match.group(1) if match else 'LEGADO-' + path.parent.name
        title = text.splitlines()[0].lstrip('# ').removeprefix('Projeto: ')
        registros.append(dict(id=id_, tipo='projeto', titulo=title, estado='planejamento',
                              fonte=rel, linha=1, legado={}, pai=None))
        tasks = path.parent / 'tarefas.md'
        if not tasks.exists():
            continue
        taskrel = tasks.relative_to(ROOT).as_posix()
        headers = None
        for line_no, line in enumerate(fontes[taskrel]['texto'].splitlines(), 1):
            if not line.strip().startswith('|'):
                continue
            cells = [x.strip() for x in re.split(r'(?<!\\)\|', line.strip().strip('|'))]
            if cells[0].lower() == 'id':
                headers = cells
                continue
            if not headers or re.fullmatch(r'[:\- ]+', cells[0]):
                continue
            if len(cells) != len(headers):
                raise RuntimeError(f'Tabela ambígua em {taskrel}:{line_no}; revisar antes de importar.')
            row = dict(zip(headers, cells))
            title = row.get('Tarefa') or row.get('Ação')
            if not title:
                raise RuntimeError(f'Coluna de tarefa desconhecida em {taskrel}:{line_no}')
            registros.append(dict(id=id_ + ':' + cells[0], tipo='tarefa', titulo=title,
                                  estado='capturada', fonte=taskrel, linha=line_no,
                                  legado=row, pai=id_))
    if len({r['id'] for r in registros}) != len(registros):
        raise RuntimeError('IDs duplicados; ensaio recusado.')
    return fontes, registros


def relatorio(destination, fontes, registros, database=None):
    e = html.escape
    rows = ''.join('<tr><td>'+e(r['tipo'])+'</td><td>'+e(r['titulo'])+'</td><td>'+e(r['legado'].get('Status', 'Consultar fonte'))+'</td><td>'+e(r['estado'])+'</td><td>'+e(r['legado'].get('Responsável', 'Consultar fonte'))+'</td><td>'+e(r['legado'].get('Prazo', 'Consultar fonte'))+'</td><td>'+e(r['fonte'])+':'+str(r['linha'])+'</td></tr>' for r in registros)
    originals = ''.join('<details><summary>'+e(name)+'</summary><p>SHA-256: '+f['sha256']+'</p><pre>'+e(f['texto'])+'</pre></details>' for name,f in fontes.items())
    destination.write_text('<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Ensaio SAERJ — legado → v2</title><style>body{font:16px system-ui;margin:32px;color:#182635;background:#f5f7fa}table{border-collapse:collapse;background:white;width:100%}td,th{padding:12px;text-align:left;border-bottom:1px solid #dce2e8;vertical-align:top}pre{white-space:pre-wrap;overflow-wrap:anywhere}details{background:white;padding:12px;margin:8px 0}.scroll{overflow:auto}input{padding:12px;width:min(500px,90%)}td:last-child{overflow-wrap:anywhere}</style><h1>Ensaio de migração · SAERJ</h1><p>'+('Importação PostgreSQL verificada · '+e(database) if database else 'Prévia do mapeamento · importação ainda não executada')+'</p><p>'+str(len(registros))+' registros estruturados · '+str(len(fontes))+' fontes Markdown preservadas.</p><p>Documentos continuam oficiais. Estados v2 são provisórios; responsáveis e prazos permanecem no legado, sem aceite inferido. Decisões e históricos estão nas fontes integrais. Ideias do conselho e anexos binários ainda não incluídos.</p><input id="busca" aria-label="Filtrar registros" placeholder="Buscar projeto, tarefa ou responsável"><div class="scroll"><table><thead><tr><th>Tipo</th><th>Título</th><th>Estado no legado</th><th>Estado v2 provisório</th><th>Responsável no legado</th><th>Prazo no legado</th><th>Fonte</th></tr></thead><tbody>'+rows+'</tbody></table></div><h2>Originais e histórico documental</h2>'+originals+'<script>document.getElementById("busca").addEventListener("input",function(){for(const r of document.querySelectorAll("tbody tr"))r.hidden=!r.textContent.toLocaleLowerCase().includes(this.value.toLocaleLowerCase())})</script></html>', encoding='utf-8')


def executar(fontes, registros):
    import psycopg
    from psycopg import sql
    from psycopg.types.json import Jsonb
    env = ambiente.connection()
    database = 'ep_ensaio_saerj_' + uuid.uuid4().hex[:12]
    ambiente.sql('CREATE DATABASE ' + database, database='postgres')
    try:
        target = dict(env, PGDATABASE=database)
        for migration in sorted((ROOT/'desenvolvimento/migrations').glob('[0-9][0-9][0-9]_*.sql')):
            digest = hashlib.sha256(migration.read_bytes()).hexdigest()
            ambiente.execute([ambiente.binary('psql'), '-X', '-v', 'ON_ERROR_STOP=1', '-v', 'hash_sql='+digest, '-f', str(migration)], target)
        with psycopg.connect(host=env['PGHOST'],port=env['PGPORT'],dbname=database,user=env['PGUSER'],password=env['PGPASSWORD']) as conn:
            conn.execute("CREATE SCHEMA ensaio")
            conn.execute("REVOKE ALL ON SCHEMA ensaio FROM PUBLIC")
            conn.execute('CREATE TABLE ensaio.fontes(caminho text PRIMARY KEY, sha256 text NOT NULL, original bytea NOT NULL)')
            conn.execute("INSERT INTO escritorio.portfolios(id,nome,configuracao) VALUES ('saerj','SAERJ — ensaio legado',%s)", (Jsonb({'ensaio':True,'oficial':False}),))
            actor = uuid.uuid4()
            conn.execute('INSERT INTO escritorio.pessoas(id,nome) VALUES(%s,%s)',(actor,'Importador de ensaio; identidade técnica'))
            conn.execute("INSERT INTO escritorio.membros(portfolio,pessoa,papel) VALUES ('saerj',%s,'gestor')",(actor,))
            for name, f in fontes.items():
                conn.execute('INSERT INTO ensaio.fontes VALUES(%s,%s,%s)',(name,f['sha256'],f['bytes']))
            for r in registros:
                origin = {'ensaio':True,'fonte':r['fonte'],'linha':r['linha'],'sha256':fontes[r['fonte']]['sha256'],'legado':r['legado'],'estado_provisorio':True}
                conn.execute("INSERT INTO escritorio.registros(portfolio,id,tipo,titulo,estado,origem,criado_por) VALUES ('saerj',%s,%s,%s,%s,%s,%s)",(r['id'],r['tipo'],r['titulo'],r['estado'],Jsonb(origin),actor))
                if r['pai']:
                    conn.execute("INSERT INTO escritorio.vinculos_registros VALUES ('saerj',%s,%s,'parte_de')",(r['id'],r['pai']))
        with psycopg.connect(host=env['PGHOST'],port=env['PGPORT'],dbname=database,user=env['PGUSER'],password=env['PGPASSWORD']) as conn:
            assert conn.execute('SELECT count(*) FROM escritorio.registros').fetchone()[0] == len(registros)
            actual = conn.execute('SELECT caminho,sha256,original FROM ensaio.fontes').fetchall()
            assert len(actual) == len(fontes)
            for name, digest, raw in actual:
                assert bytes(raw) == fontes[name]['bytes'] and hashlib.sha256(bytes(raw)).hexdigest() == digest
            saved = conn.execute('SELECT id,titulo,tipo,estado,origem FROM escritorio.registros ORDER BY id').fetchall()
            expected = {r['id']:r for r in registros}
            for id_, title, kind, state, origin in saved:
                r = expected[id_]
                assert (title,kind,state,origin['legado']) == (r['titulo'],r['tipo'],r['estado'],r['legado'])
        return database
    except Exception:
        ambiente.sql('DROP DATABASE '+database, database='postgres')
        raise


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--executar', action='store_true')
    parser.add_argument('--saida', type=Path)
    args = parser.parse_args()
    fontes, registros = inventariar()
    database = executar(fontes, registros) if args.executar else None
    destination = args.saida or Path(tempfile.mkdtemp(prefix='ensaio-saerj-'))/'resultado.html'
    destination.parent.mkdir(parents=True,exist_ok=True)
    relatorio(destination,fontes,registros,database)
    print(json.dumps({'estado':'importacao_verificada' if database else 'previa', 'banco_isolado':database, 'projetos':sum(r['tipo']=='projeto' for r in registros),'tarefas':sum(r['tipo']=='tarefa' for r in registros),'fontes':len(fontes),'visualizacao':str(destination)},ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
