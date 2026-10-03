"""Prova sintética de armazenamento; não é o runtime do Escritório.
Execute: python3 arquitetura/v2/experimentos/validar_sqlite.py
Nenhum registro real é lido. Todos os arquivos são temporários.
"""
import hashlib
import json
import sqlite3
import tempfile
from pathlib import Path


def checksum(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    with tempfile.TemporaryDirectory(prefix='escritorio-v2-') as directory:
        root = Path(directory)
        original = root / 'evidencia.txt'
        original.write_text('Evidência sintética; integração ainda pendente.\n')
        db = sqlite3.connect(root / 'operacional.sqlite')
        db.execute('PRAGMA foreign_keys=ON')
        db.execute('PRAGMA journal_mode=WAL')
        db.execute('PRAGMA synchronous=FULL')
        db.executescript('''
            CREATE TABLE portfolios (id TEXT PRIMARY KEY);
            CREATE TABLE operacoes (id TEXT PRIMARY KEY, resultado TEXT NOT NULL);
            CREATE TABLE tarefas (
                portfolio TEXT NOT NULL REFERENCES portfolios(id),
                id TEXT NOT NULL, titulo TEXT NOT NULL, status TEXT NOT NULL,
                versao INTEGER NOT NULL DEFAULT 1, PRIMARY KEY(portfolio,id));
            CREATE TABLE eventos (
                id INTEGER PRIMARY KEY, portfolio TEXT NOT NULL, tarefa TEXT NOT NULL,
                autor TEXT NOT NULL, relato TEXT NOT NULL,
                FOREIGN KEY(portfolio,tarefa) REFERENCES tarefas(portfolio,id));
            CREATE TABLE artefatos (
                id TEXT PRIMARY KEY, caminho TEXT NOT NULL, sha256 TEXT NOT NULL);
        ''')
        with db:
            db.executemany('INSERT INTO portfolios VALUES (?)', [('saerj',), ('pessoal',)])

        def capture(operation):
            with db:
                previous = db.execute('SELECT resultado FROM operacoes WHERE id=?', (operation,)).fetchone()
                if previous:
                    return previous[0]
                db.execute('INSERT INTO tarefas VALUES (?,?,?,?,1)',
                           ('saerj', 'SAERJ-TAR-TESTE', 'Integrar relatório', 'em andamento'))
                db.execute('INSERT INTO eventos(portfolio,tarefa,autor,relato) VALUES (?,?,?,?)',
                           ('saerj', 'SAERJ-TAR-TESTE', 'executor sintetico', 'Código entregue; falta API'))
                db.execute('INSERT INTO artefatos VALUES (?,?,?)',
                           ('ART-TESTE', 'evidencia.txt', checksum(original)))
                db.execute('INSERT INTO operacoes VALUES (?,?)', (operation, 'SAERJ-TAR-TESTE'))
                return 'SAERJ-TAR-TESTE'

        assert capture('OP-TESTE') == capture('OP-TESTE')
        assert db.execute('SELECT count(*) FROM tarefas').fetchone()[0] == 1
        assert db.execute('SELECT status FROM tarefas').fetchone()[0] == 'em andamento'
        before = db.execute('SELECT count(*) FROM eventos').fetchone()[0]
        try:
            with db:
                db.execute('INSERT INTO eventos(portfolio,tarefa,autor,relato) VALUES (?,?,?,?)',
                           ('saerj', 'SAERJ-TAR-TESTE', 'teste', 'Não deve persistir'))
                raise RuntimeError('Falha simulada no lote')
        except RuntimeError:
            pass
        assert db.execute('SELECT count(*) FROM eventos').fetchone()[0] == before
        try:
            with db:
                db.execute('INSERT INTO eventos(portfolio,tarefa,autor,relato) VALUES (?,?,?,?)',
                           ('pessoal', 'SAERJ-TAR-TESTE', 'teste', 'Vínculo inválido'))
        except sqlite3.IntegrityError:
            pass
        else:
            raise AssertionError('Vínculo entre portfólios não foi bloqueado')
        with db:
            assert db.execute('UPDATE tarefas SET versao=versao+1 WHERE id=? AND versao=?',
                              ('SAERJ-TAR-TESTE', 1)).rowcount == 1
            assert db.execute('UPDATE tarefas SET status=? WHERE id=? AND versao=?',
                              ('concluída', 'SAERJ-TAR-TESTE', 1)).rowcount == 0

        # Snapshot pelo mecanismo de backup, não cópia do .sqlite ativo em WAL.
        package = root / 'exportacao'
        package.mkdir()
        backup = sqlite3.connect(package / 'operacional.sqlite')
        db.backup(backup)
        backup.close()
        (package / 'evidencia.txt').write_bytes(original.read_bytes())
        manifest = {name: checksum(package / name) for name in ('operacional.sqlite', 'evidencia.txt')}
        (package / 'manifesto.json').write_text(json.dumps(manifest, indent=2))
        db.close()
        # Verificação de recuperação em outra pasta, sem chats ou caminhos originais.
        restored = root / 'restaurado'
        restored.mkdir()
        for path in package.iterdir():
            (restored / path.name).write_bytes(path.read_bytes())
        for name, expected in json.loads((restored / 'manifesto.json').read_text()).items():
            assert checksum(restored / name) == expected
        check = sqlite3.connect(restored / 'operacional.sqlite')
        assert check.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
        assert check.execute('PRAGMA foreign_key_check').fetchall() == []
        assert check.execute('SELECT count(*) FROM eventos').fetchone()[0] == 1
        path, expected = check.execute('SELECT caminho,sha256 FROM artefatos').fetchone()
        assert checksum(restored / path) == expected
        check.close()
        (restored / path).write_text('Arquivo corrompido intencionalmente')
        assert checksum(restored / path) != expected
        print('PASSOU: repetição sem duplicação; rollback; vínculo de portfólio; conflito de versão;')
        print('snapshot/restauração de banco e artefato; integridade; detecção de alteração do anexo.')
        print('SQLite', sqlite3.sqlite_version, '| Apenas dados sintéticos e arquivos temporários.')
        print('Não verifica autenticação, regras de aceite, backup externo ou recuperação após queda de energia.')


if __name__ == '__main__':
    main()
