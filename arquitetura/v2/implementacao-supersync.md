# Implementação com infraestrutura do SuperSync — versão 2

> **Situação vigente — 14/10/2026, revisão 6:** implementação isolada descontinuada por decisão de Fabrício. Servidor e banco encerrados; `tmp/supersync-escritorio-v2` removido com cluster e dados sintéticos. As seções abaixo são históricas, não um ambiente disponível. Reiniciar diretamente em `C:\Users\fabri\Projetos\supersync`, com usuários, padrões e banco configurado do SuperSync; a preferência anterior por banco independente fica substituída para esta integração. Cada ação futura exige aprovação prévia. Ver [sprints](sprints-desenvolvimento-supersync.md).

Data: 03/10/2026. Direção de avaliação solicitada por Fabrício: aproveitar servidor existente com PostgreSQL e possibilidade de interfaces/controle de usuários no SuperSync, testando localmente antes de qualquer alteração remota. Outra pessoa fará a implementação; nome, aceite, disponibilidade e prazo ainda não definidos.

## Fatos e limites

- Confirmado por relato de Fabrício: há servidor do SuperSync com PostgreSQL; interfaces e controle de usuários podem ser implementados ali. Não houve inspeção do servidor nem do código nesta etapa.
- O repositório registra o SuperSync no portfólio SAERJ e descreve gestão de usuários/autenticação como serviço compartilhado para o SAC. Isso demonstra a direção arquitetural existente, não compatibilidade já validada para o Escritório.
- A arquitetura v2 e a preparação local estão autorizadas. A iniciativa foi capturada como candidata a projeto em [SAERJ-IDEIA-002](../../conselho/ideias/saerj/escritorio-projetos-ia-v2/01-ficha-ideia.md); não há promoção explícita nem autorização de implantação.
- Não foi alterado servidor, repositório de código, tabelas, usuários ou escopo do SuperSync. Não foi enviada mensagem ao implementador.

## Fronteiras propostas

O Escritório mantém gestão, escopo, documentação, responsável total e aceites próprios. SuperSync pode prover hospedagem, identidade e interface. Reutilizar infraestrutura não transforma a documentação do Escritório em um módulo exclusivamente acessível por SuperSync.

Preferência: banco lógico próprio para o Escritório na instância PostgreSQL existente, se capacidade e política permitirem; alternativa é schema dedicado com papéis restritos, a justificar. Nenhuma tabela operacional deve ser misturada às tabelas atuais sem definição de autoridade. Contrato próprio e versionado atende Codex, Claude Code e interface web. Clientes não recebem acesso SQL administrativo.

A identidade do SuperSync será mapeada para uma identidade estável do Escritório, com autorização por portfólio e operação. Administrador técnico, gerente e executor são papéis diferentes. Autenticação do SuperSync não implica automaticamente acesso a todos os dados do Escritório.

Portfólio pessoal permanece fora do servidor corporativo por padrão; sua eventual hospedagem exige decisão específica. Os ensaios locais de separação podem usar dados sintéticos de dois portfólios. Não migrar documentos pessoais para infraestrutura SAERJ apenas porque o modelo suporta múltiplos domínios.

Arquivos originais precisam de armazenamento persistente e recuperável, com permissões, versões, IDs e checksum. O host existente não comprova que isso já exista. Banco e anexos precisam de proteção fora do host principal e procedimento de restauração coordenado.

## Material de passagem ao implementador

| Item | Fonte / ação |
|---|---|
| Regras e escopo funcional | [Especificação v2](especificacao.md) |
| Entidades, estados e integridade | [Modelo de dados](modelo-dados.md) e [schema aplicado localmente](../../desenvolvimento/migrations/README.md) |
| Operações agnósticas do cliente | [Contrato e OpenAPI](../../desenvolvimento/contratos/README.md) — serviço mínimo local implementado; demais comandos pendentes |
| Interação inicial e futura equipe | [Interação](interacao.md) |
| Critérios de validação | [Plano](plano.md) |
| Serviço mínimo HTTP e cliente de referência | [Piloto local](../../desenvolvimento/servico/README.md), sem integração SuperSync |
| Ambiente local inicializado | [Comandos e limites](../../desenvolvimento/local/README.md) |
| Prova sintética de recuperação | [Ensaio PostgreSQL](experimentos/validar_postgresql.py) |
| Dependência de serviços | [Serviços compartilhados SuperSync](../../portfolios/saerj/projetos/supersync/servicos-compartilhados.md) |

## Sequência de implementação proposta

1. Preparar esquema físico e migrations versionadas, contrato de operações e casos sintéticos; definir repositório de código/documentação com o implementador. Os scripts locais deste repositório são preparação, não definição do runtime final.
2. Implementar e validar localmente captura, repetição, consulta, autoria, artefatos, aprovação de reuniões, conclusão e bloqueios. Incluir perfis limitados e comparação de versão. Não usar serviço de autenticação de produção durante ensaio local; usar identidades de teste claramente identificadas.
3. Levantar SuperSync por acesso autorizado: versão PostgreSQL, stack, forma de autenticação, organização de usuários/perfis, capacidade, arquivos, backup, rede, ambientes e processo de publicação. Registrar evidências e lacunas; não adivinhar rotas ou tabelas de autenticação.
4. Definir integração e estimar esforço com o implementador, incluindo impacto nos consumidores atuais. Identificar dono provedor e consumidor; validar responsável total e critérios de aceite.
5. Após decisão de projeto/experimento e autorização de mudança, preparar homologação separada. Migrations não podem ser aplicadas implicitamente pelo chat ou ambiente local.
6. Validar acesso de dois clientes, interface de executor, isolamento, gravação de evidências, conflitos, indisponibilidade e restauração de banco/arquivos em destino novo.
7. Submeter plano de implantação com janela, backup prévio, reversão, credenciais próprias e monitoramento. Somente após aceites e autorizações aplicáveis executar produção.
8. Migrar dados selecionados com conciliação, preservando IDs e fontes; declarar corte de autoridade. Estado atual em Markdown continua oficial até esse marco.

## Pendências

- Nome/aceite do implementador e responsável total pela futura entrega; Fabrício é proponente e decisor da preparação, não designação automática de executor.
- Versão e capacidade reais do PostgreSQL/SuperSync; versão local disponível é 14.20, não homologada como versão final.
- Repositório de desenvolvimento e documentação funcional do Escritório; relação com o código SuperSync a decidir.
- Banco próprio versus schema, interfaces de autenticação, papéis e regras de acesso; sem dependência de comando específico de agente.
- Armazenamento de anexos, destino independente de cópia, frequência e retenção.
- Estimativa do executor, capacidade, meta desejada e previsões; nenhuma data de entrega foi inventada.
- Promoção formal como projeto, ou decisão de experimento, conforme governança existente.

## Integração iniciada como app — 14/10/2026 (revisão 2)

Pedido original de Fabrício: “quero iniciar a integração do escritório de projetos v2 com o supersync, o Escritório de projetos deve ser um app seguindo todos os padrões estabelecidos no supersync.”

Esse pedido autoriza a implementação local do app. Substitui a direção anterior de apenas avaliar infraestrutura e aguardar outro implementador, neste escopo. Não concede autorização de produção, migração de dados reais ou promoção da ideia a projeto.

Primeiro incremento implementado no repositório SuperSync, branch local `codex/escritorio-projetos-v2`, commit `084241b`, baseado na master `f7ddcb3`. Checkout isolado: `tmp/supersync-escritorio-v2/` neste ambiente. Esse caminho é área de desenvolvimento temporária; não é fonte documental ou operacional do Escritório.

App `escritorio_projetos`, rota `/escritorio/`, identidade `usuarios.SyncUsuario`, permissões globais `apuracao_contrato.escritorio_visualizar` e `escritorio_gerenciar`, regras em services, layout base Greeva/Bootstrap e entrada no menu Gestão SAERJ. Permissão global exige também vínculo ativo ao portfólio; usuário externo não recebe acesso. Não foram atribuídas permissões a usuários reais.

Implementado: seleção de portfólio autorizado, captura original, criação explicitamente classificada de ideia/solicitação/tarefa, caixa de entrada sem classificação, consulta paginada, autoria, histórico, transação e repetição sem duplicação. Não há promoção, conclusão, alteração de estado, reunião, anexo ou planejamento neste app inicial.

O incremento usa models e migrations Django, com tabelas `escritorio_projetos_*` no banco configurado pelo SuperSync. Não importa nem reutiliza automaticamente o schema SQL do piloto. Essa adaptação local segue o pedido de app nativo; isolamento físico e estratégia final de migração precisam de validação antes da implantação. Portfólio pessoal permanece fora do ambiente corporativo por padrão.

Validação: 21 testes aprovados com SQLite em memória, dados sintéticos e configurações isoladas, sem importar settings produtivo. Verificados acesso, isolamento, preservação do original, histórico, rollback, idempotência, formulários, renderização dos templates reais e CSRF. `makemigrations --check --dry-run` não encontrou alterações nos apps carregados nesse ambiente. A suíte completa do SuperSync, interface no navegador, migrations em PostgreSQL e concorrência real não foram verificadas.

Migrations preparadas: `escritorio_projetos/0001_initial` e `apuracao_contrato/0023_alter_permissoesglobais_options`. Aplicadas somente ao banco efêmero de testes. Sem push, merge na master, alteração de servidor ou corte de autoridade. Os registros Markdown permanecem oficiais.

Próximos incrementos: validar PostgreSQL e concorrência; integrar contrato portável e autenticação de clientes; portar atualização com versão, relatos e evidências; depois reuniões, bloqueios e aceite humano. Planejamento, recuperação independente e migração conciliada continuam pendentes. O guia específico do app está no commit indicado e referencia `UX_GUIDELINES.md` do SuperSync.

## API v2 e PostgreSQL validados — 14/10/2026 (revisão 3)

Continuação autorizada por Fabrício: “vamos prosseguir”. Segundo incremento salvo no SuperSync, branch local `codex/escritorio-projetos-v2`, commit `b272126`, após `084241b`.

Implementados no app: API DRF em `/escritorio/api/v1`, autenticação Bearer vinculada ao usuário SuperSync e a um portfólio, credenciais com hash, validade e revogação, modo de consulta, comandos administrativos de emissão/revogação e cliente Python de referência. Permissão global, identidade interna e vínculo ativo são reavaliados; a API não aceita identidade no corpo nem usa sessão web como alternativa. HTTPS é exigido fora do ambiente de desenvolvimento. Nenhuma credencial real foi emitida.

Subconjunto integrado do contrato 2.0.0: captura de texto com classificação apenas sugerida; criação explícita de ideia/solicitação/tarefa a partir de entrada preservada; consulta de registros com paginação assinada; recuperação de operação do mesmo usuário por outro cliente autorizado. UUID e Idempotency-Key preservam repetição. Originais podem sustentar vários registros do mesmo portfólio. Promoção, prazos, responsáveis, anexos, atualização, relatos, reuniões, bloqueios e conclusão ainda não estão portados para este app. Comandos indisponíveis são recusados.

Contrato do subconjunto em `escritorio_projetos/api/openapi.json`, no commit indicado. Schemas JSON conferidos com JSON Schema; validação integral por ferramenta OpenAPI não executada. Cliente aceita arquivo protegido ou variável de ambiente; não aceita token na linha de comando e não segue redirecionamentos.

Validação final: 45 testes aprovados no PostgreSQL 17.10 nativo Windows, em cluster próprio temporário com ACL restrita, credencial nova, conexão loopback e dados sintéticos. Inclui aplicação das migrations Django `0001` e `0002`, permissões globais `0023`, concorrência da captura web e do contrato API, IDs sem colisão, repetição sem duplicação, rollback, isolamento, expiração/revogação, recuperação pós-commit e fluxo HTTP real com dois clientes. Banco e cluster temporários foram encerrados e removidos. Nenhum serviço PostgreSQL existente foi alterado. `makemigrations --check --dry-run` não encontrou alteração nos apps do ambiente isolado.

Limites preservados: suíte completa e configuração real do SuperSync não verificadas; PostgreSQL 17.10 usado no teste não confirma a versão de produção; interface não verificada no navegador; proteção independente, homologação, migração e corte de autoridade pendentes. Sem push, merge ou implantação. Markdown permanece oficial.

Próximo incremento: atualização por versão e relato com preservação dos originais, seguido de anexos/evidências. Depois portar reuniões, dependências/bloqueios e aceite humano, conforme os contratos e invariantes existentes.

## Complementos, relatos e evidências integrados — 14/10/2026 (revisão 4)

Continuação autorizada por Fabrício: “vamos em frente”. Terceiro incremento no SuperSync, branch local `codex/escritorio-projetos-v2`, commit `d2f67f4`, após `b272126`.

Implementado: atualização de título, resultado esperado e critério de ideias/solicitações abertas, com versão examinada, motivo, complemento original e histórico anterior/posterior; relatos de tarefa com autoria autenticada separada do autor informado; preparação, envio, verificação e vínculo de anexos/evidências; download autenticado. Captura também referencia artefato verificado. Fichas recuperam complementos, relatos, fontes, integridade e histórico.

Executor exige vínculo ativo, permissão global de relato e atribuição explícita à tarefa. Consulta e download respeitam o recorte de acesso. Gestor continua responsável pelas operações formais de conteúdo e anexos. Nenhuma permissão ou atribuição real foi concedida durante esta implementação.

Relatos preservam conteúdo e propostas de prazo/esforço sem aceitar automaticamente prazo, alterar estado ou concluir tarefas. Atualização de conteúdo não altera tipo, responsável, meta ou prioridade. Conflito de versão impede sobrescrita; repetição recupera a versão efetivada originalmente, mesmo depois de outra edição. Entradas complementares não podem ser reatribuídas silenciosamente.

Arquivos usam backend Django privado `STORAGES['escritorio_artefatos']`, sem fallback público ou temporário de produção. Chaves internas por portfólio/UUID; limite de 512 KiB; conferência de tamanho e SHA-256. Preparação não confirma recebimento; envio e vínculo têm estados e verificações separados. Arquivo físico salvo antes de rollback é reconciliado por repetição, sem sobrescrever. Ausência/corrupção impede confirmação e aparece na ficha. Download é binário, como anexo, com checksum e cache privado desativado. Coleta de órfãos e cópia independente ainda pendentes.

Interface nativa inclui formulários de complemento, relato, anexo e download. Cliente portável inclui `anexar` e `baixar`, com UUID/chave estáveis, etapas separadas, checksum e preservação de destino existente. Contrato OpenAPI do subconjunto ampliado; schemas JSON conferidos, sem validação integral OpenAPI.

Validação: 64 testes aprovados no PostgreSQL 17.10 Windows em cluster temporário isolado. Inclui migrations `0003`, `0004` e permissão global `0024`, atualização concorrente da mesma versão com um sucesso/um conflito, isolamento de executor, originais, relatórios de avanço, integridade, rollback parcial, formulários e transferências HTTP reais. Cluster temporário encerrado e removido. `makemigrations --check --dry-run` não encontrou alterações nos apps isolados.

Limites: armazenamento privado precisa ser configurado e homologado no ambiente real do SuperSync; nenhum bucket, credencial ou servidor foi alterado. Suíte completa, interface no navegador, implantação, migração real e proteção independente continuam pendentes. Sem push ou merge. Markdown permanece oficial. Próximos incrementos: reuniões, dependências/bloqueios e aceite humano de tarefas; planejamento permanece posterior.

## Homologação local disponível — 14/10/2026 (revisão 5)

Pedido original de Fabrício: “crie o ambiente de homologação para que eu possa visualizar no supérsync”. Ambiente local preparado no checkout isolado do SuperSync, branch `codex/escritorio-projetos-v2`, commit `470cb67`, após `d2f67f4`.

SuperSync com todas as aplicações, rotas, modelos, login, menu, templates e arquivos estáticos nativos. Configuração própria em `escritorio_projetos/homologacao/`, sem importar settings produtivo nem `.env` ou credenciais externas. PostgreSQL 17.10 exclusivo e persistente, conexão loopback; armazenamento privado de originais configurado. Banco, configuração, senhas e logs ficam em `.runtime/homologacao/`, com ACL restrita e fora do Git.

Endereço de visualização: `http://127.0.0.1:8876/escritorio/`, disponível somente neste computador. Servidor local iniciado em segundo plano e deixado ativo. Banner identifica homologação e dados sintéticos. Integrações externas, chat IA e demais módulos operacionais estão bloqueados neste modo; não representa homologação das integrações GCP. Nenhum recurso ou serviço de produção foi alterado.

Perfis locais sintéticos de gestor, executor e consulta; três exemplos de trabalho, sem importação dos portfólios reais. Senhas geradas e mantidas somente no arquivo local protegido; não registrar valores neste histórico. Uma quarta solicitação sintética foi criada pelo navegador para verificar o fluxo. Atribuição e permissões concedidas somente a usuários desse banco de homologação.

Validação: `django check` do SuperSync completo sem problemas; todas as migrations aplicadas no banco exclusivo; login pelo formulário nativo, menu Gestão SAERJ, portfólio, captura e ficha conferidos no navegador. Persistência da solicitação `DEMO_HOMOLOGACAO-SOL-000004` verificada diretamente no banco, versão 1, autor sintético e evento de histórico. Suíte do app ampliada para 67 testes aprovados em outro cluster PostgreSQL temporário; inclui bloqueio de acesso fora de loopback, de serviços externos e identificação de homologação.

Operação no Windows: usar Python do venv do SuperSync com `escritorio_projetos/homologacao/ambiente.py iniciar`; `parar` encerra o processo HTTP verificado e o cluster próprio, preservando dados. `preparar` aplica migrations e reconcilia exemplos sem apagar registros. Guia no `escritorio_projetos/CLAUDE.md` do commit indicado. A versão do banco de produção continua não verificada.

Não houve push, merge, implantação remota, migração de dados reais ou corte de autoridade. Markdown permanece oficial. Homologação funcional dos demais fluxos, restauração independente, acesso por outros computadores e implantação continuam pendentes.
