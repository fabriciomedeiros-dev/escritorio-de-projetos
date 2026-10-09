# PRD — Escritório de Projetos v2

## Produto e problema

Um Gestor do Escritório acompanha ideias, solicitações, projetos e tarefas, preservando fontes e autoria. Hoje documentos Markdown e chats dispersam consultas e complementos; uma atualização pode perder contexto, um relato pode ser confundido com conclusão e vários computadores podem divergir. O produto fornece uma fonte operacional central com documentação vinculada e clientes substituíveis.

Usuários: gestor (Fabrício inicialmente), executor e consulta. Administrador técnico não recebe automaticamente poder de gestão. Diretoria pode ser origem da demanda; não é um tipo de registro. Identidades individuais e autorização por portfólio são requisitos do MVP operacional, ainda ausentes no piloto.

## Estado de partida

- Implementado no piloto: captura, consulta, criação de ideia/solicitação/tarefa, complementos delimitados, relatos, anexos verificados, reuniões revisadas por versão, bloqueios/dependências e conclusão de tarefa por aceite humano.
- Ensaiado em Windows com Python 3.14/PostgreSQL 17.10: contrato, restauração, integridade e fluxo HTTP; link simbólico real não verificado por falta de privilégio.
- Ensaio legado SAERJ: 5 projetos, 47 tarefas e 47 fontes Markdown em banco separado. Estados provisórios; não é migração oficial. Ideias do conselho e anexos binários ainda fora do ensaio.
- Pendentes: integração SuperSync, autenticação real, interface operacional, proteção independente e corte de autoridade.

## MVP proposto para homologação

| Requisito | Comportamento e aceite |
|---|---|
| Identidade e isolamento | Cada requisição valida pessoa, portfólio e operação; usuário de outro domínio recebe recusa sem dados. |
| Lista e ficha | Buscar por ID, título, tipo e estado; ficha mostra fontes, versão, histórico, responsáveis, prazos e lacunas. Paginação completa quando solicitada. |
| Captura | Preservar original antes da classificação; ambiguidade fica em triagem. Criar ideia, solicitação ou tarefa sem inventar campos. |
| Complementos e relatos | Conteúdo anterior preservado; alteração exige versão, motivo e autoria. Relato registra entregue/restante/dificuldade sem concluir tarefa. |
| Reuniões | Apresentar ata e tópicos; aprovação explícita da revisão exata antes de aplicar ações suportadas, em lote atômico e repetível. |
| Documentos | Upload, checksum, tamanho, integridade e download autorizado; vínculo por registro/versão/finalidade. Limite inicial do piloto: 512 KiB. |
| Bloqueios e aceite | Distinguir dependência de impedimento; resolver com evidência. Concluir tarefa só com critério, responsável, aceite e ausência de pendências necessárias. |
| Migração conciliada | Mapear originais/IDs/vínculos, revisar campos, reconciliar contagens/checksums, testar restauração e aprovar corte por conjunto de dados. |
| Recuperação | Backup coordenado de banco e arquivos em destino independente; restauração comprovada antes do uso oficial. Frequência, retenção e metas de recuperação: a definir. |

Jornada principal: autenticar → selecionar portfólio permitido → consultar ficha → registrar entrada/ação → revisar quando necessário → executar operação → verificar resultado → mostrar ID, versão e lacunas. Confirmar sucesso somente após verificação.

## Fora do MVP

Planejamento automático de sprint/capacidade, previsão automática, Kanban/calendário completos, alertas proativos, conclusão automática, encerramento de projeto/solicitação, promoção de ideia a projeto, importação automática de transcrições e sincronização bidirecional Markdown/banco. Projetos existentes podem entrar por migração aprovada; isso não habilita criação/promoção no piloto. Não hospedar portfólio pessoal na infraestrutura corporativa por padrão.

## Aceite da entrega

Demonstrar fluxo UI → contrato → serviço → banco → leitura de verificação; conflito de versão, confirmação perdida, repetição concorrente e recuperação de anexos. Validar perfis reais, isolamento, revisão de reunião, integridade da conclusão e recuperação externa. Definir responsáveis, homologação, backup e reversão antes de produção.

Indicadores a instrumentar, sem metas inventadas: taxa de operações verificadas, duplicações por repetição, registros com lacunas e restaurações bem-sucedidas. Prazos, orçamento e executor: a definir.

## Fontes e validade

Preparado em 08/10/2026 para o Escritório v2 com integração proposta ao SuperSync. Documento de preparação: não promove a iniciativa a projeto nem autoriza produção.

Fontes no Escritório: `CONTEXTO.md`, `AGENTS.md`, `arquitetura/v2/{especificacao,modelo-dados,implementacao-supersync,operacao-gestor,seguranca-chat}.md`, `desenvolvimento/contratos/openapi.json`, `desenvolvimento/migrations/`, `desenvolvimento/servico/`, `portfolios/saerj/projetos/supersync/desenvolvimento.md`. Fontes de implementação consultadas em `C:/Users/fabri/Projetos/supersync`: `AGENTS.md`, `requirements.txt`, `Dockerfile` e inventário de diretórios; HEAD observado `12f6dae`. Não foram lidos .env, dumps ou segredos, nem validados autenticação, infraestrutura remota ou comportamento do checkout completo. A inspeção documental anterior cita `bba8f83`; não a tratar como HEAD atual.
