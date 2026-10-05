"""Objetos locais imutáveis; chaves internas, sem caminhos fornecidos pelo cliente."""
import hashlib
import os
from pathlib import Path
import tempfile
import uuid

MAX_BYTES=512*1024

class Objetos:
    def __init__(self,root):
        self.root=Path(root)
        self.root.mkdir(parents=True,exist_ok=True,mode=0o700)
    def path(self,portfolio,id_):
        key=hashlib.sha256(portfolio.encode()).hexdigest()+'-'+str(uuid.UUID(id_))
        return self.root/key
    def read(self,portfolio,id_):
        path=self.path(portfolio,id_)
        if path.is_symlink(): raise ValueError('Objeto não pode ser link simbólico')
        fd=os.open(path,os.O_RDONLY|getattr(os,'O_NOFOLLOW',0))
        with os.fdopen(fd,'rb') as file:
            data=file.read(MAX_BYTES+1)
        if len(data)>MAX_BYTES: raise ValueError('Objeto excede limite')
        return data
    def save(self,portfolio,id_,data):
        if len(data)>MAX_BYTES: raise ValueError('Objeto excede limite')
        target=self.path(portfolio,id_)
        fd,name=tempfile.mkstemp(prefix='.upload-',dir=self.root)
        try:
            with os.fdopen(fd,'wb') as file:
                file.write(data);file.flush();os.fsync(file.fileno())
            try: os.link(name,target)
            except FileExistsError:
                if self.read(portfolio,id_)!=data: raise ValueError('Objeto existente diverge')
            if os.name != 'nt':
                directory=os.open(self.root,os.O_RDONLY)
                try: os.fsync(directory)
                finally: os.close(directory)
        finally:
            os.unlink(name)
        if self.read(portfolio,id_)!=data: raise ValueError('Leitura diverge')
