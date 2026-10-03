# Serviço mínimo local — Escritório v2

Piloto implementado e testado em 03/10/2026. Usa o PostgreSQL isolado, contrato agnóstico e identidades sintéticas. Não é implantação do SuperSync nem servidor de produção.

## Disponível

- Capturar texto como entrada de triagem, preservando conteúdo e origem.
- Criar tarefa, solicitação ou ideia em estado inicial, com lacunas explícitas.
- Registrar relato em tarefa aberta, com entregue, restante, dificuldade, esforço e prazo proposto.
- Consultar registros por ID, tipo, situação, assunto, origem e período, com paginação assinada.
- Consultar operação por UUID e reconciliar confirmação perdida após commit.

A resposta contém versão, histórico de origem, fontes, dependências, últimas 25 atualizações e lacunas. Relato não conclui tarefa nem aceita prazo automaticamente. O nome informado do autor do relato é separado do remetente autenticado. ID de registro usa prefixo do portfólio/tipo e UUID; título não é identificador.

Indisponível: persistência de anexos, conclusão, aprovação/extração de reuniões, promoção a projeto, dependências via API, cronograma, backup independente e interface web/menu do gestor. Comandos correspondentes são rejeitados explicitamente; não confirme seus efeitos em chat.

## Preparação e execução

Pré-requisitos: Python 3.10+ e ferramentas PostgreSQL do ambiente local. A configuração testada usa Python 3.14.3, psycopg 3.3.6, jsonschema 4.26.0 e PostgreSQL local 14.20. A política de versões e a homologação do SuperSync continuam pendentes.

```bash
python3 -m venv .runtime/servico-venv
.runtime/servico-venv/bin/python -m pip install -r desenvolvimento/servico/requirements.txt
.runtime/servico-venv/bin/python desenvolvimento/local/ambiente.py start
.runtime/servico-venv/bin/python desenvolvimento/local/ambiente.py migrate
.runtime/servico-venv/bin/python desenvolvimento/servico/preparar_demo.py
.runtime/servico-venv/bin/python desenvolvimento/servico/http_local.py
```

`preparar_demo` cria apenas `demo_escritorio`, `demo_outro` e quatro identidades fictícias: gestor, executor, consulta e outro. Não cria portfólios SAERJ/pessoal nem importa documentos. Senhas e tokens ficam exclusivamente em `.runtime/servico/`, com permissões restritas, ignorada pelo Git. Não copiar esses arquivos para a documentação ou mensagens.

O serviço escuta somente `127.0.0.1:8765`; PostgreSQL usa socket local próprio. O endereço não permite uso remoto e não altera o servidor existente. A conexão SQL usa papel sem superuser, sem criação de banco/schema e sem DELETE; os scripts de preparação/teste usam credencial administrativa somente no cluster local.

## Cliente de referência

Em outro terminal, sem colocar token na linha de comando:

```bash
.runtime/servico-venv/bin/python desenvolvimento/servico/cliente.py consultar
.runtime/servico-venv/bin/python desenvolvimento/servico/cliente.py executar --pedido desenvolvimento/servico/exemplos/criar_tarefa.json --chave exemplo-tarefa-001
.runtime/servico-venv/bin/python desenvolvimento/servico/cliente.py consultar --perfil consulta
```

O exemplo é sintético e contém ID fixo: executar novamente devolve a mesma operação, não cria outra tarefa. Para novo trabalho, preparar novo UUID e nova chave; para repetir o mesmo pedido, manter ambos. O cliente lê credenciais do arquivo local e envia Bearer token; qualquer agente pode usar esse cliente ou o mesmo contrato HTTP, sem acesso SQL administrativo.

Para atualização pelo executor, criar tarefa com `responsavel_total` correspondente à identidade sintética; ler seu UUID localmente, sem publicar o arquivo de credenciais. O cliente aceita pedido JSON do contrato. Não há autoatribuição de pessoas reais neste piloto.

`Ctrl+C` encerra o serviço HTTP. Depois:

```bash
.runtime/servico-venv/bin/python desenvolvimento/local/ambiente.py stop
```

Ao final desta implementação os serviços ficaram parados. Dados do ambiente e credenciais sintéticas persistem para uso posterior.

## Autorização e verificabilidade

Tokens aleatórios locais identificam pessoas; o servidor mantém hashes dos tokens, e o cliente guarda os valores em arquivo restrito. Esse mecanismo é exclusivo do piloto; não integra o login do SuperSync e ainda não oferece expiração/rotação/revogação gerenciada. Não reutilizar esses tokens em produção.

Gestor captura/cria e acompanha seu portfólio; executor consulta/atualiza apenas tarefas de que é responsável ou executor atribuído; consulta só lê. Operações de outro autor só são consultáveis pelo gestor, respeitando o domínio. Membros inativos são bloqueados por consulta ao banco em cada requisição. O corpo não aceita identidade ou papel declarados pelo agente.

Mutação serializada por portfólio, SQL parametrizado, estado e histórico na mesma transação; repetição identifica pedido, pessoa, chave e UUID. Conteúdo divergente retorna 409. Após commit, outra conexão verifica registros/histórico e entrada antes de marcar `verificada`. Falha depois de salvar é reconciliada por consulta da operação. A resposta preserva `protecao=pendente`: nenhuma cópia independente está configurada.

O serviço rejeita campos desconhecidos e valida tipos, datas, UUIDs e demais restrições do JSON Schema do contrato. Paginação vincula cursor ao portfólio, identidade e filtros. Resultados são ordenados por ID imutável; não é snapshot global da busca, e inserções posteriores podem exigir uma nova consulta para uma visão atualizada.

## Testes

Com PostgreSQL iniciado e demo preparada:

```bash
.runtime/servico-venv/bin/python desenvolvimento/testes/verificar_servico.py
.runtime/servico-venv/bin/python desenvolvimento/testes/verificar_contrato.py
```

O teste HTTP clona a base local em banco temporário, usa porta de loopback alocada dinamicamente e remove somente o banco de teste ao terminar. Verifica fluxo HTTP → banco, autorização/perfis/domínios, executor atribuído, estados e prazos preservados, histórico, conflito de versão, repetição simultânea, recuperação após falha simulada pós-commit, filtros com texto adverso, paginação, validação de respostas e rejeição de funções indisponíveis.

O clone inclui a demonstração local; não usar este runner para dados reais. O script não aponta para servidor externo e não depende de conexão do SuperSync. A validade estrutural das partes JSON Schema foi testada; validação integral da especificação OpenAPI por ferramenta especializada continua pendente.

## Limites para passagem ao implementador

`http.server` é um servidor de desenvolvimento local, sem TLS, hardening ou adequação produtiva. Escolher runtime de produção, autenticação SuperSync, papéis SQL/isolamento, pool, limites/monitoramento e deploy somente na etapa de integração. A biblioteca padrão documenta esse limite. [HTTP local](https://docs.python.org/3/library/http.server.html).

A próxima entrega funcional é armazenamento/verificação de originais e vínculos de evidências, seguido por reuniões e conclusão. Não migrar dados reais antes de proteger/restaurar banco e arquivos e declarar o corte de autoridade.

Referências técnicas: [parâmetros psycopg](https://www.psycopg.org/psycopg3/docs/basic/params.html), [JSON Schema](https://python-jsonschema.readthedocs.io/en/stable/validate/), [contrato](../contratos/README.md).
