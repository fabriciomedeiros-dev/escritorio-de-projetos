"""Prova sintética PostgreSQL em cluster temporário isolado.
Requer initdb, pg_ctl, psql, pg_dump e pg_restore no PATH. Não usa servidor existente.
Execute: python3 arquitetura/v2/experimentos/validar_postgresql.py
"""
import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


def run(args, **kwargs):
    return subprocess.run(args, check=True, capture_output=True, text=True, **kwargs).stdout


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    names = ['initdb', 'pg_ctl', 'psql', 'pg_dump', 'pg_restore']
    binaries = {name: shutil.which(name) for name in names}
    if not all(binaries.values()):
        raise RuntimeError('Binários PostgreSQL necessários não encontrados')
    with tempfile.TemporaryDirectory(prefix='ep-pg-') as directory:
        root = Path(directory)
        data = root / 'cluster'
        socket = root / 'socket'
        socket.mkdir()
        # Sem rede TCP. Confiança local só neste cluster temporário de teste.
        run([binaries['initdb'], '-D', str(data), '-U', 'teste', '--auth=trust', '--no-locale', '-E', 'UTF8'])
        started = False
        try:
            run([binaries['pg_ctl'], '-D', str(data), '-l', str(root / 'server.log'),
                 '-o', f"-k {socket} -c listen_addresses=''", '-w', 'start'])
            started = True
            base = ['-h', str(socket), '-U', 'teste']
            def sql(text, database='postgres'):
                return run([binaries['psql'], *base, '-d', database, '-v', 'ON_ERROR_STOP=1', '-At', '-c', text]).strip()
            sql('''CREATE TABLE portfolios(id text PRIMARY KEY);
                INSERT INTO portfolios VALUES ('saerj'),('pessoal');
                CREATE TABLE tarefas(portfolio text REFERENCES portfolios(id), id text,
                    estado text NOT NULL, versao int NOT NULL, PRIMARY KEY(portfolio,id));
                CREATE TABLE eventos(portfolio text, tarefa text, autor text, relato text,
                    FOREIGN KEY(portfolio,tarefa) REFERENCES tarefas(portfolio,id));
                CREATE TABLE operacoes(id text PRIMARY KEY, resultado text NOT NULL);
                CREATE TABLE artefatos(id text PRIMARY KEY, caminho text, checksum text);
                BEGIN;
                INSERT INTO operacoes VALUES ('OP-TESTE','TAR-TESTE');
                INSERT INTO tarefas VALUES ('saerj','TAR-TESTE','em andamento',1);
                INSERT INTO eventos VALUES ('saerj','TAR-TESTE','executor sintético','Falta API');
                COMMIT;''')
            assert sql("INSERT INTO operacoes VALUES ('OP-TESTE','TAR-TESTE') ON CONFLICT DO NOTHING; SELECT count(*) FROM operacoes;").endswith('1')
            assert sql("BEGIN; INSERT INTO eventos VALUES ('saerj','TAR-TESTE','teste','descartar'); ROLLBACK; SELECT count(*) FROM eventos;").endswith('1')
            try:
                sql("INSERT INTO eventos VALUES ('pessoal','TAR-TESTE','teste','inválido');")
            except subprocess.CalledProcessError:
                pass
            else:
                raise AssertionError('Relação inválida aceita')
            assert sql("UPDATE tarefas SET versao=2 WHERE id='TAR-TESTE' AND versao=1 RETURNING versao;").startswith('2')
            assert sql("UPDATE tarefas SET estado='concluída' WHERE id='TAR-TESTE' AND versao=1 RETURNING id;") == 'UPDATE 0'
            package = root / 'exportacao'
            package.mkdir()
            artifact = package / 'evidencia.txt'
            artifact.write_text('Evidência sintética. Entrega parcial.\n')
            expected = sha(artifact)
            sql(f"INSERT INTO artefatos VALUES ('ART-TESTE','evidencia.txt','{expected}');")
            run([binaries['pg_dump'], *base, '-d', 'postgres', '-Fc', '-f', str(package / 'banco.dump')])
            manifest = {p.name: sha(p) for p in package.iterdir()}
            (package / 'manifesto.json').write_text(json.dumps(manifest, indent=2))
            sql('CREATE DATABASE restaurado;')
            run([binaries['pg_restore'], *base, '-d', 'restaurado', '--exit-on-error', str(package / 'banco.dump')])
            assert sql('SELECT count(*) FROM eventos;', 'restaurado') == '1'
            assert sql('SELECT estado FROM tarefas;', 'restaurado') == 'em andamento'
            assert sql('SELECT checksum FROM artefatos;', 'restaurado') == expected
            for name, checksum in manifest.items():
                assert sha(package / name) == checksum
            artifact.write_text('Alteração intencional')
            assert sha(artifact) != expected
            print('PASSOU: transação/rollback; chave de repetição; relação por portfólio; versão obsoleta;')
            print('dump/restauração com histórico e referência ao artefato; checksum detecta alteração.')
            print(sql('SELECT version();'))
            print('Cluster sintético removido ao terminar; sem dados reais ou acesso TCP.')
            print('Não valida hospedagem, autenticação da equipe, RLS, backup externo ou queda de energia.')
        finally:
            if started:
                run([binaries['pg_ctl'], '-D', str(data), '-m', 'fast', '-w', 'stop'])


if __name__ == '__main__':
    main()
