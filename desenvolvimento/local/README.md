# Ambiente local — Escritório v2

Ambiente de teste do PostgreSQL, independente do SuperSync. O esquema físico inicial está aplicado; aplicação, interfaces e integração de usuários ainda não estão implementadas. Preparado e verificado em 03/10/2026.

## Uso

Requer Python 3 e ferramentas PostgreSQL no PATH (`initdb`, `pg_ctl`, `psql` da mesma instalação). Não instala nem atualiza dependências. No Windows, usar ambiente Linux/WSL com essas ferramentas; esse caminho não foi testado aqui.

Da raiz deste repositório:

```bash
python3 desenvolvimento/local/ambiente.py init
python3 desenvolvimento/local/ambiente.py start
python3 desenvolvimento/local/ambiente.py smoke
python3 desenvolvimento/local/ambiente.py status
python3 desenvolvimento/local/ambiente.py stop
```

`init` é repetível e preserva o cluster existente. `start` cria a base `escritorio_test` no cluster próprio, se necessário. `smoke` usa tabelas temporárias e rollback; não popula solicitações nem projetos. O teste atual pressupõe base sem tabelas públicas, portanto será substituído pelo teste do esquema operacional quando este existir. Se um teste falhar, executar `stop` para encerrar o ambiente.

Dados, senha aleatória e logs ficam em `.runtime/escritorio-v2/`, ignorada pelo Git. A senha é gerada localmente com permissão restrita e não aparece na saída. O script ignora variáveis PostgreSQL herdadas e conecta apenas ao socket criado pelo próprio ambiente. O PostgreSQL não escuta conexões TCP; a porta interna 55432 identifica o serviço no socket e não é publicada.

Foi verificado: inicialização, autenticação SCRAM, base própria, ausência de TCP, restrição de relacionamento por portfólio, rejeição de versão obsoleta, rollback e parada. Nenhum acesso remoto foi realizado. O cluster permanece inicializado e parado após a preparação.

## Esquema operacional e testes

O comando `migrate` aplica a revisão 001 somente à base local e verifica seu checksum. Não importa trabalhos existentes nem semeia dados reais. Uma segunda execução não reaplica a migração.

```bash
python3 desenvolvimento/local/ambiente.py start
python3 desenvolvimento/local/ambiente.py migrate
python3 desenvolvimento/testes/verificar_esquema.py
python3 desenvolvimento/local/ambiente.py stop
```

O schema `escritorio` persiste inicializado, sem registros operacionais. Os testes sintéticos revertem suas alterações e verificam dump/restauração do schema em uma base temporária distinta. Consulte o [esquema físico](../migrations/README.md) e o [contrato de operações](../contratos/README.md).

## Limites e próxima implementação

Este ambiente é a infraestrutura local de banco, não um Escritório funcional. Credenciais de desenvolvimento são administrativas e não representam perfis de usuários da aplicação. Testar autorização com papéis limitados no serviço futuro.

O PostgreSQL instalado é 14.20; foi reutilizado apenas para teste sintético local. A documentação oficial recomenda a minor atual e informa fim de suporte da série 14 em 12/11/2026. Não homologar implantação nova a partir desse binário. Confirmar a versão do SuperSync, atualizar/padronizar o teste com uma versão suportada e repetir os ensaios antes da implantação. [Política de versões](https://www.postgresql.org/support/versioning/).

Não usar credenciais de produção, copiar dados reais ou apontar este script para o SuperSync. Para integração, seguir o [roteiro de implementação](../../arquitetura/v2/implementacao-supersync.md). Não transportar o diretório físico do PostgreSQL como migração entre versões; usar esquema e exportações compatíveis.

## Restauração sintética

O ensaio temporário de dump/restauração é separado do ambiente persistente:

```bash
python3 arquitetura/v2/experimentos/validar_postgresql.py
```

Ele não lê o cluster persistente, usa somente dados sintéticos e remove seu cluster ao terminar. Testar banco e arquivos em destino independente continua necessário antes de qualquer migração real.
