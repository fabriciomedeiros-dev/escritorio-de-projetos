# Ambiente local — Escritório v2

Banco PostgreSQL e serviço HTTP de teste, isolados do SuperSync, com identidades sintéticas.

Para instalar em outra máquina, restaurar os dados e iniciar o serviço, siga [Replicação](REPLICACAO.md). O comando `replicar.py preparar` reúne venv, dependências fixadas, banco, migrações e configuração local. `verificar` executa contrato, esquema e serviço; `servir` inicia a API local.

Os comandos individuais de `ambiente.py` são `init`, `start`, `migrate`, `smoke`, `status` e `stop`. Migrações 001 e 002 são aplicadas em ordem com checksum. Dados e credenciais locais ficam em `.runtime/`, ignorada pelo Git. Clusters novos usam socket local, sem TCP; configurações anteriores do DBeaver não são alteradas.

PostgreSQL 14.20 foi reutilizado no piloto; homologação da versão central, autenticação real e proteção independente permanecem pendentes. Não transportar o diretório físico do banco ou apontar estes scripts ao SuperSync. Consulte [integração](../../arquitetura/v2/implementacao-supersync.md).
