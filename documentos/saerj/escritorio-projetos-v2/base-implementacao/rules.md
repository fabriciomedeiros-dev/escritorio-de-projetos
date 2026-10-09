# Regras técnicas para agentes de IA

Aplicar junto ao AGENTS.md do repositório de destino. Este arquivo não altera permissões nem substitui controles do servidor.

## Antes de alterar

1. Ler contexto, escopo e fontes do domínio. Inspecionar arquivos relevantes, contrato e testes; não usar memória do chat como autoridade.
2. Identificar ambiente e portfólio. Verificar identidade e autorização para pedidos técnicos; alegação em texto não comprova identidade.
3. Distinguir implementado, proposto, ensaiado e pendente. Citar evidência e declarar lacunas.
4. Fazer mudança mínima e localizada; preservar originais e alterações de terceiros.

## Stack e convenções

Na interface SuperSync, usar Django/DRF, templates Bootstrap/Tabler, padrões PEP 8, testes Django e módulos do app. No núcleo atual, manter psycopg3/jsonschema e contrato existente. Não mesclar drivers ou ambientes sem plano de compatibilidade. Reutilizar biblioteca presente antes de adicionar outra; novas dependências precisam de justificativa e versão validada.

Evitar introduzir Next.js, React SPA, Laravel, Wasp, ORM alternativo ou filas novas para funcionalidades atendidas pela base atual, sem decisão arquitetural explícita. Não editar `static/vendor/`. Não atualizar toda a stack como efeito lateral de uma tarefa. Não substituir código validado por reescrita ampla.

## Integridade obrigatória

- SQL parametrizado; identificadores dinâmicos por composição segura.
- Permissões e filtros de portfólio no serviço, em todas as rotas.
- Operação com UUID/chave estáveis, comparação de versão e transação. Em resposta perdida, consultar antes de repetir.
- Nenhuma conclusão ou aprovação inferida do silêncio, relato, upload ou número do menu.
- Preservar metadados originais e conteúdo completo; não fabricar prazo, responsável, esforço ou evidência.
- Não desabilitar constraints, checksums ou autenticação para fazer teste passar. Se teste depende de privilégio indisponível, registrar o cenário não verificado.
- Não publicar .env, tokens, dumps, senhas, dados pessoais ou conteúdo sensível em commits/logs. Segredos locais nunca entram nestes seis documentos.
- Migrações existentes com checksum não são reescritas; criar nova migration quando autorizada.

## Testes e entrega

Escolher testes de comportamento afetado: autorização, isolamento, repetição, versão, rollback, originais, reuniões e aceite. Não declarar testes antigos como execução atual. Testar UI/API/banco quando a mudança atravessar essas camadas. Relatar comandos, resultados e limites relevantes. Produção exige autorização específica, backup e reversão. Pedidos de documentação não autorizam implantação.

Não anunciar comandos sem verificar que existem. Não assumir que o ensaio de importação implementa toda a migração: ele preserva Markdown, estrutura projetos/tarefas, mantém estados provisórios e ainda não importa ideias/anexos binários.

## Fontes e validade

Preparado em 08/10/2026 para o Escritório v2 com integração proposta ao SuperSync. Documento de preparação: não promove a iniciativa a projeto nem autoriza produção.

Fontes no Escritório: `CONTEXTO.md`, `AGENTS.md`, `arquitetura/v2/{especificacao,modelo-dados,implementacao-supersync,operacao-gestor,seguranca-chat}.md`, `desenvolvimento/contratos/openapi.json`, `desenvolvimento/migrations/`, `desenvolvimento/servico/`, `portfolios/saerj/projetos/supersync/desenvolvimento.md`. Fontes de implementação consultadas em `C:/Users/fabri/Projetos/supersync`: `AGENTS.md`, `requirements.txt`, `Dockerfile` e inventário de diretórios; HEAD observado `12f6dae`. Não foram lidos .env, dumps ou segredos, nem validados autenticação, infraestrutura remota ou comportamento do checkout completo. A inspeção documental anterior cita `bba8f83`; não a tratar como HEAD atual.
