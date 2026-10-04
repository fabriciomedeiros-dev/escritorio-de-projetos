"""Servidor HTTP exclusivamente local para o piloto, não destinado a produção."""
import json
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit,parse_qs
import psycopg
from nucleo import Servico,Falha


class Handler(BaseHTTPRequestHandler):
    service=None
    protocol_version='HTTP/1.0'
    def log_message(self,*args): pass  # Não registrar tokens, conteúdo ou query string.
    def reply(self,status,body):
        raw=json.dumps(body,ensure_ascii=False,allow_nan=False).encode()
        self.send_response(status)
        self.send_header('Content-Type','application/json; charset=utf-8')
        self.send_header('Cache-Control','no-store')
        self.send_header('Content-Length',str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)
    def dispatch(self):
        try:
            url=urlsplit(self.path)
            match=re.fullmatch(r'/v1/portfolios/([a-z][a-z0-9_-]*)/(operacoes|registros|artefatos|reunioes)(?:/([0-9a-fA-F-]+))?',url.path)
            if not match: raise Falha(404,'NAO_ENCONTRADO','Rota não disponível.')
            auth=self.headers.get('Authorization','')
            if not auth.startswith('Bearer '): raise Falha(401,'NAO_AUTENTICADO','Bearer token obrigatório.')
            actor=self.service.identity(auth[7:])
            p,resource,id_=match.groups()
            if self.command=='GET' and resource=='artefatos' and id_:
                if url.query: raise Falha(400,'PEDIDO_INVALIDO','Download não aceita filtros.')
                import uuid
                try: id_=str(uuid.UUID(id_))
                except ValueError: raise Falha(400,'PEDIDO_INVALIDO','ID de artefato inválido.')
                data=self.service.download(p,actor,id_)
                self.send_response(200)
                self.send_header('Content-Type','application/octet-stream')
                self.send_header('Content-Disposition',f'attachment; filename="{id_}.bin"')
                self.send_header('X-Content-Type-Options','nosniff')
                self.send_header('Cache-Control','no-store')
                self.send_header('Content-Length',str(len(data)))
                self.end_headers();self.wfile.write(data)
                return
            if self.command=='POST' and resource=='operacoes' and not id_:
                if url.query: raise Falha(400,'PEDIDO_INVALIDO','POST não aceita filtros na URL.')
                if self.headers.get('Content-Type','').split(';')[0]!='application/json': raise Falha(400,'PEDIDO_INVALIDO','Content-Type deve ser application/json.')
                try:
                    size=int(self.headers.get('Content-Length','0'))
                    if not 1<=size<=1024*1024: raise ValueError()
                    def unique(pairs):
                        result={}
                        for key,value in pairs:
                            if key in result: raise ValueError('Campo JSON duplicado')
                            result[key]=value
                        return result
                    def invalid(value): raise ValueError('Número não finito')
                    pedido=json.loads(self.rfile.read(size),object_pairs_hook=unique,parse_constant=invalid)
                except (ValueError,UnicodeError): raise Falha(400,'PEDIDO_INVALIDO','JSON ou tamanho inválido.')
                result=self.service.operation(p,actor,self.headers.get('Idempotency-Key',''),pedido)
            elif self.command=='GET' and resource=='operacoes' and id_:
                if url.query: raise Falha(400,'PEDIDO_INVALIDO','Consulta de operação não aceita filtros.')
                result=self.service.get_operation(p,actor,id_)
            elif self.command=='GET' and resource=='registros' and not id_:
                query=parse_qs(url.query,keep_blank_values=True)
                if any(len(values)!=1 for values in query.values()): raise Falha(400,'PEDIDO_INVALIDO','Filtro repetido.')
                result=self.service.query(p,actor,{key:value[0] for key,value in query.items()})
            elif self.command=='GET' and resource=='reunioes':
                query=parse_qs(url.query,keep_blank_values=True)
                if any(len(values)!=1 for values in query.values()): raise Falha(400,'PEDIDO_INVALIDO','Filtro repetido.')
                result=self.service.query_meetings(p,actor,id_,{key:value[0] for key,value in query.items()})
            else: raise Falha(404,'NAO_ENCONTRADO','Rota não disponível.')
            self.reply(200,result)
        except Falha as error:
            self.reply(error.status,{'codigo':error.codigo,'mensagem':error.mensagem,'detalhes':{}})
        except psycopg.IntegrityError:
            self.reply(422,{'codigo':'PEDIDO_INVALIDO','mensagem':'Gravação rejeitada pelas regras de integridade.','detalhes':{}})
        except (psycopg.Error,OSError):
            self.reply(503,{'codigo':'SERVICO_INDISPONIVEL','mensagem':'Consultar operação antes de reenviar o pedido.','detalhes':{}})
        except Exception:
            self.reply(500,{'codigo':'SERVICO_INDISPONIVEL','mensagem':'Falha interna sem confirmação de registro; consultar operação.','detalhes':{}})
    do_GET=dispatch
    do_POST=dispatch


def server(service=None,port=8765):
    # Instância de handler por servidor permite teste isolado sem estado global compartilhado.
    handler=type('LocalHandler',(Handler,),{'service':service or Servico()})
    http=ThreadingHTTPServer(('127.0.0.1',port),handler)
    http.daemon_threads=True
    return http


if __name__=='__main__':
    http=server()
    print('Piloto local em http://127.0.0.1:8765 — captura, criação, relatos, consultas e reuniões com revisão/aplicação; proteção pendente.')
    try: http.serve_forever()
    except KeyboardInterrupt: pass
    finally: http.server_close()
