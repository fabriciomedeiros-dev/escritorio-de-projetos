"""Verifica ramificações Windows por simulação; não homologa execução em Windows."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'local'))
import plataforma
import ambiente

class Windows(unittest.TestCase):
    def test_venv(self):
        self.assertEqual(plataforma.venv_python(Path('venv'),True).as_posix(), 'venv/Scripts/python.exe')

    def test_binarios(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp);(folder/'initdb.exe').touch();(folder/'psql.exe').touch()
            with patch.object(plataforma,'WINDOWS',True),patch.dict('os.environ',{'ESCRITORIO_PG_BIN':tmp}),patch.object(ambiente,'WINDOWS',True):
                self.assertEqual(ambiente.binary('psql'),str(folder/'psql.exe'))
                with self.assertRaises(RuntimeError):ambiente.binary('pg_restore')

    def test_conexao_restrita(self):
        with tempfile.TemporaryDirectory() as tmp:
            state=Path(tmp)/'state.json';password=Path(tmp)/'password';password.write_text('sintetico')
            with patch.object(ambiente,'WINDOWS',True),patch.object(ambiente,'owned'),patch.object(ambiente,'STATE',state),patch.object(ambiente,'PASSWORD',password):
                for host,port in [('servidor-remoto','55432'),('127.0.0.1','5432')]:
                    state.write_text(json.dumps({'host':host,'port':port}))
                    with self.assertRaises(RuntimeError):ambiente.connection()
                state.write_text(json.dumps({'host':'127.0.0.1','port':'55432'}))
                self.assertEqual(ambiente.connection()['PGHOST'],'127.0.0.1')

    def test_acl_falha_interrompe(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(plataforma,'WINDOWS',True),patch.object(plataforma.subprocess,'run') as run:
            run.return_value.returncode=1
            with self.assertRaises(RuntimeError):plataforma.protect_runtime(Path(tmp)/'runtime')
            self.assertIn('-EncodedCommand',run.call_args.args[0])

if __name__=='__main__':unittest.main()
