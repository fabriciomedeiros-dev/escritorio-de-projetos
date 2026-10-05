"""Ensaios em duas cópias/clusters novos; não transporta o cluster atual."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile

ROOT=Path(__file__).resolve().parents[2]
PYTHON=sys.executable


def run(root,*args,ok=True):
    result=subprocess.run([PYTHON,*map(str,args)],cwd=root,capture_output=True,text=True,env=os.environ.copy())
    if ok and result.returncode:raise RuntimeError(result.stdout+'\n'+result.stderr)
    return result


def main():
    with tempfile.TemporaryDirectory(prefix='ep-replica-') as directory:
        work=Path(directory);source=work/'origem';target=work/'destino'
        source.mkdir()
        shutil.copytree(ROOT/'desenvolvimento',source/'desenvolvimento',ignore=shutil.ignore_patterns('__pycache__'))
        shutil.copytree(ROOT/'arquitetura',source/'arquitetura')
        (source/'VERSION').write_text('2.0.0\n');(source/'.gitignore').write_text('.runtime/\n__pycache__/\n')
        subprocess.run(['git','init','-q',str(source)],check=True)
        subprocess.run(['git','add','.'],cwd=source,check=True)
        subprocess.run(['git','-c','user.name=Ensaio local','-c','user.email=ensaio@localhost','commit','-qm','Código de ensaio'],cwd=source,check=True)
        # Dependências já instaladas na venv chamadora; o bootstrap confere as mesmas versões.
        for root in (source,):
            (root/'.runtime').mkdir()
            (root/'.runtime/servico-venv').symlink_to(Path(sys.prefix),target_is_directory=True)
        started=[]
        try:
            started.append(source);run(source,'desenvolvimento/local/replicar.py','preparar')
            fixture=r'''
import sys,uuid,hashlib,base64,json
from pathlib import Path
sys.path.insert(0,str(Path('desenvolvimento/servico').resolve()))
from nucleo import Servico
clients=json.loads(Path('.runtime/servico/clientes.local.json').read_text())['identidades']
service=Servico();actor=clients['gestor']['pessoa'];p='demo_escritorio'
def op(name,data):
 id_=str(uuid.uuid4());return service.operation(p,actor,id_,{'operacao_id':id_,'comando':name,'dados':data})
data=b'Original sintetico que precisa ser recuperado'
a=op('preparar_artefato',{'nome':'original.txt','tipo_midia':'text/plain','bytes_esperados':len(data),'sha256_esperado':hashlib.sha256(data).hexdigest(),'origem':{'canal':'teste'}})['resultado']['artefato']['id']
op('enviar_artefato',{'artefato_id':a,'conteudo_base64':base64.b64encode(data).decode()})
entry=op('capturar_entrada',{'artefato_id':a,'texto':'Solicitação sintética','origem':{'canal':'teste'}})['resultado']['entrada_id']
op('criar_registro',{'tipo':'tarefa','titulo':'Entrega que será transportada','origem_entrada_id':entry,'responsavel_total':clients['executor']['pessoa'],'criterio_conclusao':'Original e conteúdo recuperáveis'})
'''
            run(source,'-c',fixture)
            (source/'.runtime/revisoes-reunioes/ensaio').mkdir(parents=True)
            (source/'.runtime/revisoes-reunioes/ensaio/original.txt').write_text('Original documental sintético')
            (source/'portfolios/saerj').mkdir(parents=True)
            (source/'portfolios/saerj/nota.md').write_text('Documento de trabalho não commitado')
            package=work/'dados.zip'
            run(source,'desenvolvimento/local/transferir.py','exportar','--pacote',package)
            run(source,'desenvolvimento/local/transferir.py','conferir','--pacote',package)
            with zipfile.ZipFile(package) as z:
                assert not any('password.local' in x or 'config.local.json' in x or 'clientes.local.json' in x for x in z.namelist())
            subprocess.run(['git','clone','-q',str(source),str(target)],check=True)
            (target/'.runtime').mkdir();(target/'.runtime/servico-venv').symlink_to(Path(sys.prefix),target_is_directory=True)
            started.append(target);run(target,'desenvolvimento/local/replicar.py','preparar','--pacote',package)
            assert (target/'.runtime/revisoes-reunioes/ensaio/original.txt').read_text()=='Original documental sintético'
            assert (target/'portfolios/saerj/nota.md').read_text()=='Documento de trabalho não commitado'
            # IDs preservados e tokens/senhas diferentes; leitura e download com credenciais novas.
            source_clients=json.loads((source/'.runtime/servico/clientes.local.json').read_text())['identidades']
            target_clients=json.loads((target/'.runtime/servico/clientes.local.json').read_text())['identidades']
            assert {k:v['pessoa'] for k,v in source_clients.items()}=={k:v['pessoa'] for k,v in target_clients.items()}
            assert all(source_clients[k]['token']!=target_clients[k]['token'] for k in source_clients)
            assert (source/'.runtime/escritorio-v2/password.local').read_text()!=(target/'.runtime/escritorio-v2/password.local').read_text()
            check=r'''
import sys,json
from pathlib import Path
sys.path.insert(0,str(Path('desenvolvimento/servico').resolve()))
from nucleo import Servico
c=json.loads(Path('.runtime/servico/clientes.local.json').read_text())['identidades']
s=Servico();r=s.query('demo_escritorio',c['gestor']['pessoa'],{})['itens']
assert len(r)==1 and r[0]['titulo']=='Entrega que será transportada'
assert s.download('demo_escritorio',c['gestor']['pessoa'],r[0]['fontes'][0]['artefato'])==b'Original sintetico que precisa ser recuperado'
'''
            run(target,'-c',check)
            run(target,'desenvolvimento/local/replicar.py','preparar','--pacote',package)
            # Destino com dados próprios é recusado sem apagar/substituir registros.
            (target/'.runtime/replicacao/recebimento.json').unlink()
            refused=run(target,'desenvolvimento/local/transferir.py','restaurar','--pacote',package,ok=False)
            assert refused.returncode and 'destino novo' in refused.stderr
            run(target,'-c',check)
            corrupt=work/'corrompido.zip';corrupt.write_bytes(package.read_bytes()+b'x')
            (Path(str(corrupt)+'.sha256')).write_text(Path(str(package)+'.sha256').read_text())
            assert run(target,'desenvolvimento/local/transferir.py','conferir','--pacote',corrupt,ok=False).returncode
            print('PASSOU: instalação em caminhos diferentes, migrações, transferência lógica de banco/objeto/documento, IDs preservados, credenciais novas, retomada e recusa de destino ocupado/pacote divergente.')
        finally:
            for root in reversed(started):run(root,'desenvolvimento/local/ambiente.py','stop',ok=False)


if __name__=='__main__':main()
