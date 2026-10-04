# Plano de implementação — versão 2

## Sequência e situação

| Etapa | Entrega | Situação |
|---|---|---|
| 1 | Especificação, arquitetura e interação aprovadas funcionalmente | Documentadas nesta versão |
| 2 | Modelo lógico, entidades, estados e invariantes | Documentado; esquema físico 001 aplicado e testado localmente |
| 3 | Avaliação e escolha de armazenamento | PostgreSQL central escolhido; comparação e ensaios sintéticos concluídos; comparação de hospedagem concluída, decisão pendente |
| 4 | Fluxo mínimo pelo Codex | Piloto HTTP/cliente local implementados para texto, criação, relato, atualização de conteúdo com originais vinculados e consulta; anexos/evidências verificados implementados; reuniões e integração SuperSync pendentes |
| 5 | Piloto com casos reais e recuperação | Pendente |
| 6 | Planejamento semanal, capacidade e alertas | Pendente |
| 7 | Interface individual para dois integrantes | Posterior à validação do uso individual |

## Etapa 3 — escolha e migração

Resultado: [comparação de armazenamento](armazenamento.md). PostgreSQL central, serviço autenticado e arquivos centrais; Fabrício precisa de acesso por vários computadores desde o início. Ensaios sintéticos SQLite e PostgreSQL passaram. Escolha técnica não significa implantação: hospedagem e proteção externa continuam pendentes.

Avaliar fonte própria, Trello e Notion com documentação oficial atual e prova prática, sem assumir capacidade de anexos, API, histórico ou exportação. Comparar custo, operação, acesso por clientes substituíveis (Codex inicialmente), portfólios, autoria, aprovação por versão, dependências, concorrência, exportação, cópia independente e restauração. Uma ferramenta pode ser interface sem ser a fonte oficial.

Critérios eliminatórios: independência de fornecedor do agente e acesso por contrato portável; recuperação completa com arquivos e vínculos; identidade estável; isolamento; histórico; consulta e atualização verificáveis; ausência de fontes oficiais concorrentes. Registrar lacunas e compensações necessárias. Escolher somente depois da comparação.

Inventariar registros existentes, preservar caminhos/IDs e originais, mapear campos e conciliar divergências com fontes. Fazer ensaio de migração e restauração antes do corte. Declarar por conjunto de dados qual fonte passa a valer e quando; preservar versão anterior e plano de reversão. Não migrar dados reais silenciosamente nem transformar metas antigas em fatos atuais.

Comparação de hospedagem: [alternativas, custos e recomendação](hospedagem.md). Após Fabrício informar servidor PostgreSQL existente, priorizar avaliação do SuperSync; Supabase permanece alternativa. Não houve aprovação de implantação. Esquema físico e contrato podem avançar sem depender dessa decisão.

Preparação local: PostgreSQL isolado inicializado e smoke test aprovado, schema 001 aplicado e testes de integridade aprovados. Serviço mínimo HTTP e cliente local implementados e testados com identidades sintéticas; integração SuperSync pendente. Seguir [roteiro de passagem](implementacao-supersync.md) e [comandos locais](../../desenvolvimento/local/README.md). A iniciativa está capturada como SAERJ-IDEIA-002, sem promoção formal.

## Etapa 4 — fluxo mínimo

Implementar operações de captura idempotente, verificação, consulta por ID/assunto/origem/período/status, atualização com evidência, registro de bloqueio e aprovação de reunião por versão. Definir contrato versionado de operações e instruções portáveis do gestor; depois configurar o adaptador inicial do Codex e os resumos de entrada. Cada operação recebe portfólio explícito. Primeiro uso somente por Fabrício; nenhum menu pode anunciar função ainda indisponível.

## Critérios de aceitação do piloto

| Cenário | Resultado esperado |
|---|---|
| Relatório de faturamento pontual | Solicitação recuperável, tarefas e responsável, prazo e fonte; consulta sem criar projeto artificial |
| Inventário de máquinas | Projeto com responsável total, subtarefas, evidências e dependências |
| Projeto ativo selecionado com Fabrício | Recuperar estado e documentação existentes, preservando lacunas e autoridade técnica |
| Reunião com vários assuntos | Original preservado; todos os tópicos revisáveis; nenhum efeito operacional antes da aprovação; lote aplicado sem duplicação |
| Entrega de código dependente de API | Avanço parcial visível; tarefa total pendente; motivo e próxima ação recuperáveis |
| Relatos conflitantes | Preservar autores/datas, sinalizar conflito e não concluir por recência |
| Falha de gravação/anexo e reenvio | Não confirmar íntegro; retomar sem duplicar efeitos; mostrar pendência |
| Troca de agente | Cliente alternativo ou adaptador de referência recupera IDs, documentos, pendências e aprovações sem importar chats; mesmas regras e permissões, sem duplicar efeitos |
| Novo chat | Recuperar registros e fontes sem depender do chat anterior |
| Restauração independente | Reconstruir registros, originais, aprovações, relações e histórico; conferir manifesto e checksums |
| Consulta de portfólio | Nenhum conteúdo de outro domínio; visão conjunta somente por pedido explícito |

Usar exemplos sintéticos nos primeiros ensaios; validar os três casos reais sem inventar status, prazo, responsável ou conclusão. Testes de implementação devem exercitar os invariantes, falhas e recuperação, não somente respostas textuais do agente.

## Etapas posteriores

Planejamento: calcular carga a partir de esforço restante e capacidade informada, considerar dias úteis/dependências, distinguir meta e previsão e testar conflito de recursos. Mudança de sprint exige decisão gerencial. Configurar revisão semanal e limiar de prazo próximo com Fabrício; não há automação agendada nesta etapa.

Equipe: autenticação individual, permissões operacionais e autoria; formulário/lista de tarefas com chat opcional. Conselho permanece separado; avaliar sua execução quando o fluxo de ideação for retomado.

## Incremento local — complementos recuperáveis (2026-10-03)

Implementada atualização de conteúdo de ideias/solicitações abertas, com vínculo dos textos originais, histórico e versão. Consultas recuperam os complementos sem depender do chat anterior. Instruções comuns do gestor documentadas; anexos/evidências implementados no incremento seguinte; reuniões continuam pendentes. Testes HTTP em cópia temporária via backup/restauração, sem encerrar sessões do banco de demonstração.

## Incremento local — originais e evidências (2026-10-03)

Implementados preparação, envio, revalidação, download autenticado, captura de anexo e vínculos por versão/finalidade. Arquivos imutáveis locais com tamanho e checksum; recuperação de envio interrompido entre filesystem e banco testada. Cliente portável permite envio e download. Limite inicial 512 KiB por arquivo; somente identidades sintéticas. Conclusão, reuniões e proteção independente continuam pendentes. Não houve alteração no SuperSync ou migração de dados reais.
