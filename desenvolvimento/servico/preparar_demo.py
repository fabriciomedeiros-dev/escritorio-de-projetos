"""Inicializa somente identidades/portfólios sintéticos no banco local."""
import hashlib
import json
import os
from pathlib import Path
import secrets
import sys
import uuid
import psycopg
from psycopg import sql
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'local'))
import ambiente
from nucleo import CONFIG


def main():
    if not ambiente.running(): raise RuntimeError('Inicie e migre o ambiente local primeiro.')
    CONFIG.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
    os.chmod(CONFIG.parent,0o700)
    client_file=CONFIG.parent/'clientes.local.json'
    if CONFIG.exists():
        env=ambiente.connection()
        with psycopg.connect(host=env['PGHOST'],port=env['PGPORT'],dbname=env['PGDATABASE'],user=env['PGUSER'],password=env['PGPASSWORD']) as conn:
            conn.execute('GRANT INSERT ON escritorio.artefatos,escritorio.fontes TO escritorio_api_local')
            conn.execute('GRANT UPDATE ON escritorio.artefatos TO escritorio_api_local')
            conn.execute('GRANT INSERT ON escritorio.lotes,escritorio.propostas,escritorio.aprovacoes,escritorio.efetivacoes,escritorio.vinculos_registros TO escritorio_api_local')
        print('Configuração sintética existente; privilégios de artefatos/reuniões conferidos, credenciais preservadas.')
        return
    actors={name:str(uuid.uuid4()) for name in ('gestor','executor','consulta','outro')}
    tokens={name:secrets.token_urlsafe(40) for name in actors}
    password=secrets.token_urlsafe(40)
    env=ambiente.connection()
    with psycopg.connect(host=env['PGHOST'],port=env['PGPORT'],dbname=env['PGDATABASE'],user=env['PGUSER'],password=env['PGPASSWORD']) as conn:
        conn.execute("SELECT pg_advisory_xact_lock(20261003,2)")
        conn.execute("INSERT INTO escritorio.portfolios(id,nome) VALUES ('demo_escritorio','Demonstração sintética'),('demo_outro','Outro domínio sintético')")
        for name,id_ in actors.items():
            conn.execute('INSERT INTO escritorio.pessoas(id,nome) VALUES(%s,%s)',(id_,'Pessoa sintética '+name))
            conn.execute('INSERT INTO escritorio.membros(portfolio,pessoa,papel) VALUES(%s,%s,%s)',('demo_outro' if name=='outro' else 'demo_escritorio',id_,'gestor' if name=='outro' else name))
        conn.execute(sql.SQL('CREATE ROLE escritorio_api_local LOGIN PASSWORD {} NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT').format(sql.Literal(password)))
        conn.execute('GRANT CONNECT ON DATABASE escritorio_test TO escritorio_api_local')
        conn.execute('GRANT USAGE ON SCHEMA escritorio TO escritorio_api_local')
        conn.execute('GRANT SELECT ON ALL TABLES IN SCHEMA escritorio TO escritorio_api_local')
        conn.execute('GRANT INSERT ON escritorio.operacoes,escritorio.entradas,escritorio.registros,escritorio.atualizacoes,escritorio.historico,escritorio.artefatos,escritorio.fontes TO escritorio_api_local')
        conn.execute('GRANT UPDATE ON escritorio.operacoes,escritorio.entradas,escritorio.registros,escritorio.artefatos TO escritorio_api_local')
        conn.execute('GRANT INSERT ON escritorio.lotes,escritorio.propostas,escritorio.aprovacoes,escritorio.efetivacoes,escritorio.vinculos_registros TO escritorio_api_local')
        conn.execute('GRANT USAGE ON ALL SEQUENCES IN SCHEMA escritorio TO escritorio_api_local')
    config={'senha_banco':password,'cursor_secret':secrets.token_urlsafe(40),'tokens':[{'hash':hashlib.sha256(tokens[name].encode()).hexdigest(),'pessoa':id_} for name,id_ in actors.items()]}
    # Permissões restritas desde a criação, não apenas após escrever o segredo.
    for path,value in [(CONFIG,config),(client_file,{'identidades':{name:{'pessoa':id_,'token':tokens[name]} for name,id_ in actors.items()}})]:
        fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
        with os.fdopen(fd,'w') as file: json.dump(value,file,indent=2)
    print('Demonstração preparada: demo_escritorio e demo_outro, com quatro identidades sintéticas.')
    print('Usuário SQL restrito; credenciais locais ignoradas pelo Git. Nenhum dado real foi importado.')


if __name__=='__main__': main()
