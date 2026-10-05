"""Transferência lógica local: dados/objetos/documentos, sem credenciais ou cluster físico."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tempfile
import zipfile

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'desenvolvimento/local'))
sys.path.insert(0,str(ROOT/'desenvolvimento/servico'))
import ambiente
import psycopg
from psycopg import sql
from psycopg.rows import dict_row
from objetos import Objetos
from preparar_demo import preparar

MAX_TOTAL=512*1024*1024


def sha(data):return hashlib.sha256(data).hexdigest()

def admin():
    env=ambiente.connection()
    return psycopg.connect(host=env['PGHOST'],port=env['PGPORT'],dbname=env['PGDATABASE'],user=env['PGUSER'],password=env['PGPASSWORD'],row_factory=dict_row)


def tables(conn):
    return [x['table_name'] for x in conn.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='escritorio' AND table_type='BASE TABLE' ORDER BY table_name")]


def counts(conn):
    return {name:conn.execute(sql.SQL('SELECT count(*) AS n FROM {}').format(sql.Identifier('escritorio',name))).fetchone()['n'] for name in tables(conn)}


def code_manifest():
    files=[ROOT/'desenvolvimento/servico/requirements.txt',*(ROOT/'desenvolvimento/migrations').glob('*.sql')]
    return {p.relative_to(ROOT).as_posix():sha(p.read_bytes()) for p in sorted(files)}


def git(*args):
    return subprocess.check_output(['git',*args],cwd=ROOT)


def write_private(path,data):
    path.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
    fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    with os.fdopen(fd,'wb') as f:f.write(data)


def export_package(path, include_documents=True):
    if not ambiente.running():raise RuntimeError('Inicie o banco local antes de exportar.')
    if path.exists():raise RuntimeError('Destino já existe; escolha outro nome, sem sobrescrever pacote.')
    members={}
    base_hashes={}
    with admin() as conn, tempfile.TemporaryDirectory(prefix='ep-transferencia-') as directory:
        portfolios=[r['id'] for r in conn.execute('SELECT id FROM escritorio.portfolios ORDER BY id')]
        if set(portfolios)!={'demo_escritorio','demo_outro'}:raise RuntimeError('Transferência habilitada apenas para o piloto sintético local.')
        for p in portfolios:conn.execute('SELECT pg_advisory_xact_lock(hashtextextended(%s,0))',(p,))
        snap=conn.execute('SELECT pg_export_snapshot() AS id').fetchone()['id']
        dump=Path(directory)/'banco.dump'
        ambiente.execute([ambiente.binary('pg_dump'),'-Fc','--data-only','--no-owner','--no-privileges','-n','escritorio','--exclude-table-data=escritorio.migracoes','--snapshot='+snap,'-f',str(dump)],ambiente.connection())
        members['banco.dump']=dump.read_bytes()
        objects=Objetos(ROOT/'.runtime/servico/objetos')
        for a in conn.execute('SELECT * FROM escritorio.artefatos'):
            object_path=objects.path(a['portfolio'],str(a['id']))
            if not object_path.exists():
                if a['estado']=='verificado':raise RuntimeError('Original verificado ausente; transferência não confirmada.')
                continue
            data=objects.read(a['portfolio'],str(a['id']))
            if len(data)!=a['bytes'] or sha(data)!=a['sha256']:raise RuntimeError('Original divergente; transferência não confirmada.')
            members['objetos/'+object_path.name]=data
        clients=json.loads((ROOT/'.runtime/servico/clientes.local.json').read_text())['identidades']
        identities={name:item['pessoa'] for name,item in clients.items()}  # Tokens não são exportados.
        total_counts=counts(conn)
        major=conn.execute('SHOW server_version_num').fetchone()['server_version_num']
        if include_documents:
            review_root=ROOT/'.runtime/revisoes-reunioes'
            if review_root.exists():
                for file in sorted(review_root.rglob('*')):
                    if file.is_symlink():raise RuntimeError('Revisão contém symlink; não copiar fonte externa.')
                    if file.is_file():members['documentos/'+file.relative_to(ROOT).as_posix()]=file.read_bytes()
            changed=git('diff','HEAD','--name-only','-z').split(b'\0')
            untracked=git('ls-files','--others','--exclude-standard','-z','--','portfolios','conselho').split(b'\0')
            for raw in sorted(set(changed+untracked)):
                if not raw:continue
                relative=raw.decode()
                if not relative.startswith(('portfolios/','conselho/')):continue
                file=ROOT/relative
                if not file.is_file() or file.is_symlink():raise RuntimeError('Documento removido ou symlink; revisar antes de transferir.')
                members['documentos/'+relative]=file.read_bytes()
                old=subprocess.run(['git','show','HEAD:'+relative],cwd=ROOT,capture_output=True)
                base_hashes[relative]=sha(old.stdout) if old.returncode==0 else None
        manifest={'formato':1,'codigo_commit':git('rev-parse','HEAD').decode().strip(),'postgresql_major':int(major)//10000,'codigo':code_manifest(),'contagens':total_counts,'identidades_demo':identities,'documentos_base':base_hashes,
                  'arquivos':{name:{'sha256':sha(data),'bytes':len(data)} for name,data in members.items()},'protecao_independente':'pendente','credenciais_incluidas':False}
        if sum(len(x) for x in members.values())>MAX_TOTAL:raise RuntimeError('Pacote excede limite local de 512 MiB.')
        path.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
        fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
        try:
            with os.fdopen(fd,'wb') as file,zipfile.ZipFile(file,'w',compression=zipfile.ZIP_DEFLATED) as z:
                z.writestr('manifesto.json',json.dumps(manifest,ensure_ascii=False,indent=2).encode())
                for name,data in members.items():z.writestr(name,data)
        except Exception:
            path.unlink(missing_ok=True);raise
    digest=sha(path.read_bytes())
    write_private(Path(str(path)+'.sha256'),(digest+'  '+path.name+'\n').encode())
    print(json.dumps({'pacote':str(path),'sha256':digest,'arquivos':len(members),'contagens':total_counts,'credenciais_incluidas':False,'protecao_independente':'pendente'},ensure_ascii=False,indent=2))
    return manifest


def read_package(path, expected=None):
    if path.is_symlink():raise RuntimeError('Pacote deve ser arquivo regular, não symlink.')
    digest=sha(path.read_bytes())
    sidecar=Path(str(path)+'.sha256')
    expected=expected or (sidecar.read_text().split()[0] if sidecar.exists() else None)
    if not expected or digest!=expected:raise RuntimeError('Checksum do pacote ausente/divergente; levar também o arquivo .sha256.')
    with zipfile.ZipFile(path) as z:
        names=z.namelist()
        if len(names)!=len(set(names)) or len(names)>10000 or sum(i.file_size for i in z.infolist())>MAX_TOTAL:
            raise RuntimeError('Pacote excede limites ou contém nomes duplicados.')
        manifest=json.loads(z.read('manifesto.json'))
        if manifest.get('formato')!=1 or manifest.get('credenciais_incluidas') is not False:raise RuntimeError('Formato de transferência não reconhecido.')
        if set(names)!={'manifesto.json',*manifest['arquivos']}:raise RuntimeError('Manifesto não corresponde aos arquivos do pacote.')
        payload={}
        for name,metadata in manifest['arquivos'].items():
            parts=PurePosixPath(name)
            if parts.is_absolute() or '..' in parts.parts or '\\' in name or not (name=='banco.dump' or name.startswith('objetos/') or name.startswith('documentos/')):
                raise RuntimeError('Caminho inválido no pacote.')
            if name.startswith('documentos/'):
                relative=name[len('documentos/'):]
                if not relative.startswith(('.runtime/revisoes-reunioes/','portfolios/','conselho/')):raise RuntimeError('Documento fora do escopo permitido.')
            if name.startswith('objetos/') and len(parts.parts)!=2:raise RuntimeError('Chave de objeto inválida.')
            data=z.read(name)
            if len(data)!=metadata['bytes'] or sha(data)!=metadata['sha256']:raise RuntimeError('Arquivo do pacote diverge do manifesto.')
            payload[name]=data
    return manifest,payload,digest


def restore_package(path, expected=None):
    manifest,payload,digest=read_package(path,expected)
    if manifest['codigo']!=code_manifest():raise RuntimeError('Migrações/dependências do código divergem do pacote; usar o código correspondente.')
    statefile=ROOT/'.runtime/replicacao/recebimento.json'
    prior=json.loads(statefile.read_text()) if statefile.exists() else None
    if prior and prior['pacote_sha256']!=digest:raise RuntimeError('Destino já recebeu outro pacote; não sobrescrever ambiente.')
    with admin() as conn:
        major=int(conn.execute('SHOW server_version_num').fetchone()['server_version_num'])//10000
        if major!=manifest['postgresql_major']:raise RuntimeError('Use a mesma versão principal PostgreSQL do pacote para esta réplica.')
        actual=counts(conn)
        if not prior and (any(n for name,n in actual.items() if name!='migracoes') or (ROOT/'.runtime/servico/config.local.json').exists()):
            raise RuntimeError('Restauração exige destino novo, antes de preparar_demo. Não sobrescrever dados/configurações existentes.')
        if prior and prior.get('banco_restaurado') and actual!=manifest['contagens']:raise RuntimeError('Destino mudou após restauração parcial; não reaplicar automaticamente.')
    if not prior:
        write_private(statefile,json.dumps({'pacote_sha256':digest,'banco_restaurado':False,'estado':'pendente'}).encode())
        prior={'pacote_sha256':digest,'banco_restaurado':False,'estado':'pendente'}
    if not prior['banco_restaurado']:
        # Sem --clean, sem DROP e sem restauração de roles/segredos. Falha reverte a transação.
        with tempfile.TemporaryDirectory(prefix='ep-restauracao-') as directory:
            dump=Path(directory)/'banco.dump';dump.write_bytes(payload['banco.dump'])
            ambiente.execute([ambiente.binary('pg_restore'),'--data-only','--no-owner','--no-privileges','--single-transaction','--exit-on-error','-n','escritorio','-d',ambiente.DATABASE,str(dump)],ambiente.connection())
        prior['banco_restaurado']=True
        statefile.write_text(json.dumps(prior))
    for name,data in payload.items():
        if name=='banco.dump':continue
        relative='.runtime/servico/objetos/'+name[len('objetos/'):] if name.startswith('objetos/') else name[len('documentos/'):]
        target=ROOT/relative
        if target.is_symlink() or any(parent.is_symlink() for parent in target.parents if parent!=ROOT and ROOT in parent.parents):raise RuntimeError('Destino contém symlink; não gravar fora do repositório.')
        if target.exists():
            current=sha(target.read_bytes())
            if current==sha(data):continue
            if current!=manifest['documentos_base'].get(relative):raise RuntimeError('Destino contém arquivo divergente; não sobrescrever trabalho local.')
            target.write_bytes(data)
        else:write_private(target,data)
    identities=ROOT/'.runtime/replicacao/identidades-restauradas.json'
    if not identities.exists():write_private(identities,json.dumps(manifest['identidades_demo']).encode())
    preparar(manifest['identidades_demo'])
    with admin() as conn:
        if counts(conn)!=manifest['contagens']:raise RuntimeError('Contagens restauradas divergem; não confirmar réplica.')
        objects=Objetos(ROOT/'.runtime/servico/objetos')
        for a in conn.execute("SELECT * FROM escritorio.artefatos WHERE estado='verificado'"):
            data=objects.read(a['portfolio'],str(a['id']))
            if len(data)!=a['bytes'] or sha(data)!=a['sha256']:raise RuntimeError('Original restaurado diverge.')
    prior['estado']='verificada';statefile.write_text(json.dumps(prior))
    print('RÉPLICA VERIFICADA: banco, objetos e documentos conferidos; credenciais locais novas. Proteção independente contínua pendente.')


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('acao',choices=['exportar','restaurar','conferir'])
    parser.add_argument('--pacote',required=True,type=Path)
    parser.add_argument('--sha256')
    parser.add_argument('--sem-documentos',action='store_true',help='Somente banco e objetos, para ensaio sintético')
    args=parser.parse_args()
    if args.acao=='exportar':export_package(args.pacote.resolve(),not args.sem_documentos)
    elif args.acao=='restaurar':restore_package(args.pacote.resolve(),args.sha256)
    else:
        manifest,_,_=read_package(args.pacote.resolve(),args.sha256)
        print('PACOTE ÍNTEGRO:',len(manifest['arquivos']),'arquivos; credenciais excluídas.')


if __name__=='__main__':
    try:main()
    except (RuntimeError,OSError,ValueError,psycopg.Error) as exc:
        print('NÃO CONCLUÍDO:',str(exc),file=sys.stderr);raise SystemExit(1)
