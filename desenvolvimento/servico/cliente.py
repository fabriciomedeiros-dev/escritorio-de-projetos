"""Cliente de referência portável: token local lido de arquivo ignorado pelo Git."""
import argparse
import json
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.error import HTTPError
from urllib.parse import urlencode
import uuid
import base64
import hashlib
import mimetypes
from objetos import MAX_BYTES

ROOT=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('acao',choices=['consultar','operacao','executar','anexar','baixar'])
parser.add_argument('--perfil',choices=['gestor','executor','consulta','outro'],default='gestor')
parser.add_argument('--portfolio',default='demo_escritorio')
parser.add_argument('--pedido',type=Path)
parser.add_argument('--chave',help='Chave estável de repetição; obrigatória em executar')
parser.add_argument('--id')
parser.add_argument('--assunto')
parser.add_argument('--tipo',choices=['ideia','solicitacao','projeto','tarefa'])
parser.add_argument('--estado')
parser.add_argument('--limite',type=int)
parser.add_argument('--cursor')
parser.add_argument('--arquivo',type=Path)
parser.add_argument('--registro')
parser.add_argument('--versao',type=int)
parser.add_argument('--finalidade',choices=['documentacao','evidencia','origem'],default='documentacao')
parser.add_argument('--porta',type=int,default=8765,help='Porta do serviço, sempre em 127.0.0.1')
args=parser.parse_args()
credentials=json.loads((ROOT/'.runtime/servico/clientes.local.json').read_text())['identidades'][args.perfil]
if not 1<=args.porta<=65535: parser.error('Porta inválida')
url='http://127.0.0.1:'+str(args.porta)+'/v1/portfolios/'+args.portfolio
headers={'Authorization':'Bearer '+credentials['token']}
body=None
if args.acao in ('anexar','baixar'):
    if not args.id or not args.arquivo: parser.error('anexar/baixar exige --id UUID e --arquivo')
    try: master=uuid.UUID(args.id)
    except ValueError: parser.error('--id deve ser UUID')
    if args.acao=='baixar':
        # O servidor verifica o original antes de devolver bytes; não sobrescrever destino.
        try:
            with urlopen(Request(url+'/artefatos/'+str(master),headers=headers),timeout=15) as response:
                data=response.read(MAX_BYTES+1)
                if len(data)>MAX_BYTES: raise ValueError('Download excede limite local')
        except HTTPError as error:
            print(error.read().decode());raise SystemExit(1)
        with args.arquivo.open('xb') as target: target.write(data)
        print(json.dumps({'arquivo':str(args.arquivo),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()},ensure_ascii=False))
        raise SystemExit(0)
    if not args.chave or len(args.chave)>160: parser.error('anexar exige --chave estável de até 160 caracteres')
    if (args.registro is None)!=(args.versao is None): parser.error('--registro e --versao devem ser usados juntos')
    with args.arquivo.open('rb') as source: data=source.read(MAX_BYTES+1)
    if len(data)>MAX_BYTES: parser.error('Arquivo excede limite do piloto: 512 KiB')
    def step(command,payload):
        pedido={'operacao_id':str(uuid.uuid5(master,command)),'comando':command,'dados':payload}
        request_headers={**headers,'Content-Type':'application/json','Idempotency-Key':args.chave+':'+command}
        try:
            with urlopen(Request(url+'/operacoes',data=json.dumps(pedido).encode(),headers=request_headers),timeout=15) as response:
                return json.loads(response.read())
        except HTTPError as error:
            print(error.read().decode());raise SystemExit(1)
    prepared=step('preparar_artefato',{'nome':args.arquivo.name,'tipo_midia':mimetypes.guess_type(args.arquivo.name)[0] or 'application/octet-stream','bytes_esperados':len(data),'sha256_esperado':hashlib.sha256(data).hexdigest(),'origem':{'canal':'cliente de referência'}})
    artifact_id=prepared['resultado']['artefato']['id']
    # Mostra o ID antes das próximas etapas, permitindo recuperação de falha parcial.
    print(json.dumps({'artefato_id':artifact_id,'preparacao':'verificada','envio':'pendente'},ensure_ascii=False),flush=True)
    uploaded=step('enviar_artefato',{'artefato_id':artifact_id,'conteudo_base64':base64.b64encode(data).decode()})
    print(json.dumps(uploaded,ensure_ascii=False,indent=2),flush=True)
    if args.registro:
        linked=step('vincular_artefato',{'artefato_id':artifact_id,'registro_id':args.registro,'versao_esperada':args.versao,'finalidade':args.finalidade,'motivo':'Vínculo solicitado explicitamente pelo cliente'})
        print(json.dumps(linked,ensure_ascii=False,indent=2))
    raise SystemExit(0)
if args.acao=='executar':
    if not args.pedido or not args.chave: parser.error('executar exige --pedido e --chave')
    body=args.pedido.read_bytes();url+='/operacoes'
    headers.update({'Content-Type':'application/json','Idempotency-Key':args.chave})
elif args.acao=='operacao':
    if not args.id: parser.error('operacao exige --id')
    uuid.UUID(args.id);url+='/operacoes/'+args.id
else:
    url+='/registros'
    filters={name:getattr(args,name) for name in ('id','assunto','tipo','estado','limite','cursor') if getattr(args,name) is not None}
    if filters:url+='?'+urlencode(filters)
try:
    with urlopen(Request(url,data=body,headers=headers),timeout=15) as response:
        result=json.loads(response.read())
except HTTPError as error:
    result=json.loads(error.read());print(json.dumps(result,ensure_ascii=False,indent=2));raise SystemExit(1)
print(json.dumps(result,ensure_ascii=False,indent=2))
