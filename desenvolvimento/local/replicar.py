"""Instalação portável do piloto local. Não instala software no sistema operacional."""
import argparse
import importlib.metadata
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import venv
from plataforma import venv_python, pg_directory, protect_runtime, WINDOWS

ROOT=Path(__file__).resolve().parents[2]
VENV=ROOT/'.runtime/servico-venv'
PYTHON=venv_python(VENV)


def pg_path():
    return pg_directory()


def environment():
    result=os.environ.copy()
    result['PATH']=str(pg_path())+os.pathsep+result.get('PATH','')
    return result


def execute(args):
    subprocess.run([str(x) for x in args],cwd=ROOT,env=environment(),check=True)


def diagnose():
    if sys.version_info<(3,10):raise RuntimeError('Python 3.10 ou posterior necessário; ambiente validado em 3.14.')
    if hasattr(os,'geteuid') and os.geteuid()==0:raise RuntimeError('Execute como usuário comum; initdb não pode executar como root.')
    tools=pg_path()
    versions={}
    for name in ('initdb','pg_ctl','psql','pg_dump','pg_restore'):
        binary=tools/(name+'.exe' if WINDOWS else name)
        if not binary.is_file():raise RuntimeError(f'Ferramenta ausente: {name}')
        versions[name]=subprocess.check_output([str(binary),'--version'],text=True).strip()
    major={line.split()[-1].split('.')[0] for line in versions.values()}
    if len(major)!=1:raise RuntimeError('Ferramentas PostgreSQL com versões principais divergentes.')
    print(json.dumps({'python':sys.version.split()[0],'postgresql':versions,'repositorio':str(ROOT),'piloto':'local, sem SuperSync'},ensure_ascii=False,indent=2))


def prepare(package=None):
    diagnose()
    protect_runtime(ROOT/'.runtime')
    if not PYTHON.exists():
        VENV.parent.mkdir(parents=True,exist_ok=True)
        venv.EnvBuilder(with_pip=True).create(VENV)
    requirements=ROOT/'desenvolvimento/servico/requirements.txt'
    check="import importlib.metadata,json; print(json.dumps({x:importlib.metadata.version(x) for x in "+repr([line.split('==')[0] for line in requirements.read_text().splitlines() if line.strip()])+"}))"
    installed=subprocess.run([str(PYTHON),'-c',check],capture_output=True,text=True)
    expected=dict(line.split('==') for line in requirements.read_text().splitlines() if line.strip())
    if installed.returncode or json.loads(installed.stdout)!=expected:
        execute([PYTHON,'-m','pip','install','--disable-pip-version-check','--no-input','-r',requirements])
    for action in ('init','start','migrate'):
        execute([PYTHON,'desenvolvimento/local/ambiente.py',action])
    if package:
        execute([PYTHON,'desenvolvimento/local/transferir.py','restaurar','--pacote',package])
    else:
        execute([PYTHON,'desenvolvimento/servico/preparar_demo.py'])
    execute([PYTHON,'desenvolvimento/testes/verificar_contrato.py'])
    print('PRONTO: ambiente local preparado. Execute python3 desenvolvimento/local/replicar.py verificar e depois servir.')


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('acao',choices=['diagnosticar','preparar','verificar','servir'])
    parser.add_argument('--pacote',type=Path,help='Dados/documentos de transferência, somente em destino novo')
    args=parser.parse_args()
    if args.acao=='diagnosticar':diagnose()
    elif args.acao=='preparar':prepare(args.pacote.resolve() if args.pacote else None)
    else:
        diagnose()
        if not PYTHON.exists():raise RuntimeError('Execute preparar primeiro.')
        if args.acao=='verificar':
            for script in ('verificar_contrato.py','verificar_esquema.py','verificar_servico.py'):
                execute([PYTHON,'desenvolvimento/testes/'+script])
        else:execute([PYTHON,'desenvolvimento/servico/http_local.py'])


if __name__=='__main__':
    try:main()
    except (RuntimeError,subprocess.CalledProcessError) as exc:
        print('NÃO CONCLUÍDO:',str(exc),file=sys.stderr);raise SystemExit(1)
