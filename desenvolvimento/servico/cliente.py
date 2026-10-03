"""Cliente de referência portável: token local lido de arquivo ignorado pelo Git."""
import argparse
import json
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.error import HTTPError
from urllib.parse import urlencode
import uuid

ROOT=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('acao',choices=['consultar','operacao','executar'])
parser.add_argument('--perfil',choices=['gestor','executor','consulta','outro'],default='gestor')
parser.add_argument('--portfolio',default='demo_escritorio')
parser.add_argument('--pedido',type=Path)
parser.add_argument('--chave',help='Chave estável de repetição; obrigatória em executar')
parser.add_argument('--id')
args=parser.parse_args()
credentials=json.loads((ROOT/'.runtime/servico/clientes.local.json').read_text())['identidades'][args.perfil]
url='http://127.0.0.1:8765/v1/portfolios/'+args.portfolio
headers={'Authorization':'Bearer '+credentials['token']}
body=None
if args.acao=='executar':
    if not args.pedido or not args.chave: parser.error('executar exige --pedido e --chave')
    body=args.pedido.read_bytes();url+='/operacoes'
    headers.update({'Content-Type':'application/json','Idempotency-Key':args.chave})
elif args.acao=='operacao':
    if not args.id: parser.error('operacao exige --id')
    uuid.UUID(args.id);url+='/operacoes/'+args.id
else:
    url+='/registros'
    if args.id:url+='?'+urlencode({'id':args.id})
try:
    with urlopen(Request(url,data=body,headers=headers),timeout=15) as response:
        result=json.loads(response.read())
except HTTPError as error:
    result=json.loads(error.read());print(json.dumps(result,ensure_ascii=False,indent=2));raise SystemExit(1)
print(json.dumps(result,ensure_ascii=False,indent=2))
