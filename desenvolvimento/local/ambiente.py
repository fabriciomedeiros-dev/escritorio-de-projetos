"""PostgreSQL local isolado para validação do Escritório v2.
Não usa URLs, credenciais ou servidores existentes. Requer ferramentas PostgreSQL.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import shutil
import subprocess
import tempfile
from plataforma import WINDOWS, pg_directory, protect_runtime

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / '.runtime' / 'escritorio-v2'
DATA = RUNTIME / 'postgres'
PASSWORD = RUNTIME / 'password.local'
STATE = RUNTIME / 'estado.json'
USER = 'escritorio_local'
DATABASE = 'escritorio_test'
PORT = '55432'


def socket_root():
    # macOS resolve /tmp para /private/tmp; Linux/WSL usa o temporário do sistema.
    return Path('/tmp').resolve()


def binary(name):
    candidate = pg_directory() / (name + '.exe' if WINDOWS else name)
    if not candidate.is_file():
        raise RuntimeError(f'Binário compatível não encontrado: {name}')
    return str(candidate)


def execute(args, env=None, allowed=(0,)):
    clean = {key: value for key, value in os.environ.items() if not key.startswith('PG')}
    if env:
        clean.update(env)
    result = subprocess.run(args, env=clean, capture_output=True, text=True)
    if result.returncode not in allowed:
        # Os comandos nunca incluem a senha; stderr pode conter somente diagnóstico local.
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or f'Falha em {Path(args[0]).name}')
    return result


def owned():
    marker = RUNTIME / 'ambiente.json'
    if not marker.exists() or json.loads(marker.read_text()).get('repositorio') != str(ROOT):
        raise RuntimeError('Ambiente local não inicializado ou marcador de propriedade incompatível.')


def running():
    owned()
    return execute([binary('pg_ctl'), '-D', str(DATA), 'status'], allowed=(0, 3)).returncode == 0


def connection():
    owned()
    state = json.loads(STATE.read_text())
    if WINDOWS:
        if state.get('host') != '127.0.0.1' or str(state.get('port')) != PORT:
            raise RuntimeError('Conexão fora do ambiente local permitido.')
        return {'PGHOST':'127.0.0.1','PGPORT':PORT,'PGUSER':USER,
                'PGPASSWORD':PASSWORD.read_text().strip(),'PGDATABASE':DATABASE}
    socket = Path(state['socket'])
    if socket.parent.resolve() != socket_root() or not socket.name.startswith('ep-v2-'):
        raise RuntimeError('Socket fora do espaço local permitido.')
    return {'PGHOST': str(socket), 'PGPORT': PORT, 'PGUSER': USER,
            'PGPASSWORD': PASSWORD.read_text().strip(), 'PGDATABASE': DATABASE}


def sql(statement, database=DATABASE):
    env = connection()
    env['PGDATABASE'] = database
    return execute([binary('psql'), '-X', '-v', 'ON_ERROR_STOP=1', '-At', '-c', statement], env).stdout.strip()


def initialize():
    protect_runtime(ROOT / '.runtime')
    RUNTIME.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(RUNTIME, 0o700)
    marker = RUNTIME / 'ambiente.json'
    if marker.exists():
        owned()
    elif DATA.exists():
        raise RuntimeError('Diretório preexistente sem propriedade verificada; não será modificado.')
    else:
        marker.write_text(json.dumps({'repositorio': str(ROOT), 'finalidade': 'teste local v2'}))
    if (DATA / 'PG_VERSION').exists():
        print('Cluster local já inicializado; dados preservados.')
        return
    if not PASSWORD.exists():
        PASSWORD.write_text(secrets.token_urlsafe(32) + '\n')
    os.chmod(PASSWORD, 0o600)
    execute([binary('initdb'), '-D', str(DATA), '-U', USER,
             '--auth-local=scram-sha-256', '--auth-host=scram-sha-256',
             '--pwfile', str(PASSWORD), '--no-locale', '-E', 'UTF8'])
    print('Cluster local inicializado, separado de qualquer servidor existente.')


def start():
    if running():
        print('Cluster local já em execução.')
        return
    socket = None if WINDOWS else Path(tempfile.mkdtemp(prefix='ep-v2-', dir=str(socket_root())))
    if socket: os.chmod(socket, 0o700)
    options = f'-p {PORT} -c listen_addresses=127.0.0.1 -c unix_socket_directories=' if WINDOWS else f'-p {PORT} -k "{socket}" -c listen_addresses='''
    try:
        execute([binary('pg_ctl'), '-D', str(DATA), '-l', str(RUNTIME / 'postgres.log'),
                 '-o', options, '-w', 'start'])
    except Exception:
        if socket: socket.rmdir()
        raise
    STATE.write_text(json.dumps({'host':'127.0.0.1','port':PORT} if WINDOWS else {'socket':str(socket),'port':PORT}))
    os.chmod(STATE, 0o600)
    if Path(sql('SHOW data_directory;', 'postgres')).resolve() != DATA.resolve():
        raise RuntimeError('Servidor não pertence ao cluster do Escritório; interrompido.')
    if sql(f"SELECT count(*) FROM pg_database WHERE datname='{DATABASE}';", 'postgres') == '0':
        sql(f'CREATE DATABASE {DATABASE};', 'postgres')
    print('Banco escritorio_test pronto; TCP restrito a 127.0.0.1:55432.' if WINDOWS else 'Banco escritorio_test pronto; conexão somente por socket local, sem TCP.')


def smoke():
    if not running():
        raise RuntimeError('Inicie o ambiente antes de executar smoke.')
    assert sql('SHOW listen_addresses;') == ('127.0.0.1' if WINDOWS else '')
    result = sql('''BEGIN;
        CREATE TEMP TABLE probe_portfolios(id text PRIMARY KEY) ON COMMIT DROP;
        CREATE TEMP TABLE probe_tarefas(portfolio text REFERENCES probe_portfolios(id),
            id text, estado text, versao integer, PRIMARY KEY(portfolio,id)) ON COMMIT DROP;
        CREATE TEMP TABLE probe_eventos(portfolio text, tarefa text,
            FOREIGN KEY(portfolio,tarefa) REFERENCES probe_tarefas(portfolio,id)) ON COMMIT DROP;
        INSERT INTO probe_portfolios VALUES ('saerj'),('pessoal');
        INSERT INTO probe_tarefas VALUES ('saerj','TESTE','em andamento',1);
        DO $$ BEGIN
            BEGIN
                INSERT INTO probe_eventos VALUES ('pessoal','TESTE');
                RAISE EXCEPTION 'Relação inválida aceita';
            EXCEPTION WHEN foreign_key_violation THEN NULL;
            END;
            UPDATE probe_tarefas SET versao=2 WHERE id='TESTE' AND versao=1;
            UPDATE probe_tarefas SET estado='concluída' WHERE id='TESTE' AND versao=1;
            IF FOUND THEN RAISE EXCEPTION 'Atualização obsoleta aceita'; END IF;
            IF (SELECT estado FROM probe_tarefas WHERE id='TESTE') <> 'em andamento'
                THEN RAISE EXCEPTION 'Estado parcial não preservado'; END IF;
        END $$;
        SELECT estado FROM probe_tarefas;
        ROLLBACK;''')
    assert result.endswith('ROLLBACK')
    assert sql("SELECT count(*) FROM information_schema.tables WHERE table_schema='public';") == '0'
    print('PASSOU: conexão local autenticada; vínculo por portfólio; conflito de versão; rollback.')
    print('Versão local: ' + sql('SHOW server_version;'))
    print('Nenhuma tabela operacional foi criada; aplicação e integração SuperSync ainda não implementadas.')


def migrate():
    if not running():
        raise RuntimeError('Inicie o ambiente local antes da migração.')
    migrations = sorted((ROOT / 'desenvolvimento' / 'migrations').glob('[0-9][0-9][0-9]_*.sql'))
    has_schema = sql("SELECT count(*) FROM information_schema.schemata WHERE schema_name='escritorio';") == '1'
    for migration in migrations:
        version = int(migration.name.split('_')[0])
        digest = hashlib.sha256(migration.read_bytes()).hexdigest()
        current = sql(f'SELECT hash_sql FROM escritorio.migracoes WHERE versao={version};') if has_schema else ''
        if current:
            if current != digest:
                raise RuntimeError(f'Checksum da migração {version:03d} diverge; não reaplicar nem modificar schema existente.')
            print(f'Migração {version:03d} já aplicada e checksum conferido; nada alterado.')
            continue
        execute([binary('psql'), '-X', '-v', 'ON_ERROR_STOP=1', '-v', 'hash_sql=' + digest,
                 '-f', str(migration)], connection())
        has_schema = True
        assert sql(f'SELECT hash_sql FROM escritorio.migracoes WHERE versao={version};') == digest
        print(f'Migração {version:03d} aplicada e verificada somente no banco local escritorio_test.')


def stop():
    if not running():
        print('Cluster local já parado; dados preservados.')
        return
    execute([binary('pg_ctl'), '-D', str(DATA), '-m', 'fast', '-w', 'stop'])
    # Só remover o diretório de socket criado por este ambiente, depois do shutdown.
    socket_name = json.loads(STATE.read_text()).get('socket')
    if not socket_name:
        print('Cluster local parado; dados preservados.')
        return
    socket = Path(socket_name)
    if socket.parent.resolve() == socket_root() and socket.name.startswith('ep-v2-'):
        socket.rmdir()
    print('Cluster local parado; banco e senha local preservados fora do Git.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['init', 'start', 'smoke', 'migrate', 'stop', 'status'])
    command = parser.parse_args().command
    if command == 'status':
        print('Em execução' if running() else 'Parado')
    else:
        {'init': initialize, 'start': start, 'smoke': smoke, 'migrate': migrate, 'stop': stop}[command]()


if __name__ == '__main__':
    main()
