# Plano de implementação — versão 2

## Sequência e situação

| Etapa | Entrega | Situação |
|---|---|---|
| 1 | Especificação, arquitetura e interação aprovadas funcionalmente | Documentadas nesta versão |
| 2 | Modelo lógico, entidades, estados e invariantes | Documentado; esquema físico depende da etapa 3 |
| 3 | Avaliação e escolha de armazenamento | Pendente |
| 4 | Fluxo mínimo pelo Codex | Pendente |
| 5 | Piloto com casos reais e recuperação | Pendente |
| 6 | Planejamento semanal, capacidade e alertas | Pendente |
| 7 | Interface individual para dois integrantes | Posterior à validação do uso individual |

## Etapa 3 — escolha e migração

Avaliar fonte própria, Trello e Notion com documentação oficial atual e prova prática, sem assumir capacidade de anexos, API, histórico ou exportação. Comparar custo, operação, acesso pelo Codex, portfólios, autoria, aprovação por versão, dependências, concorrência, exportação, cópia independente e restauração. Uma ferramenta pode ser interface sem ser a fonte oficial.

Critérios eliminatórios: recuperação completa com arquivos e vínculos; identidade estável; isolamento; histórico; consulta e atualização verificáveis; ausência de fontes oficiais concorrentes. Registrar lacunas e compensações necessárias. Escolher somente depois da comparação.

Inventariar registros existentes, preservar caminhos/IDs e originais, mapear campos e conciliar divergências com fontes. Fazer ensaio de migração e restauração antes do corte. Declarar por conjunto de dados qual fonte passa a valer e quando; preservar versão anterior e plano de reversão. Não migrar dados reais silenciosamente nem transformar metas antigas em fatos atuais.

## Etapa 4 — fluxo mínimo

Implementar operações de captura idempotente, verificação, consulta por ID/assunto/origem/período/status, atualização com evidência, registro de bloqueio e aprovação de reunião por versão. Depois configurar instruções/skills do gestor e os resumos de entrada. Cada operação recebe portfólio explícito. Primeiro uso somente por Fabrício; nenhum menu pode anunciar função ainda indisponível.

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
| Novo chat | Recuperar registros e fontes sem depender do chat anterior |
| Restauração independente | Reconstruir registros, originais, aprovações, relações e histórico; conferir manifesto e checksums |
| Consulta de portfólio | Nenhum conteúdo de outro domínio; visão conjunta somente por pedido explícito |

Usar exemplos sintéticos nos primeiros ensaios; validar os três casos reais sem inventar status, prazo, responsável ou conclusão. Testes de implementação devem exercitar os invariantes, falhas e recuperação, não somente respostas textuais do agente.

## Etapas posteriores

Planejamento: calcular carga a partir de esforço restante e capacidade informada, considerar dias úteis/dependências, distinguir meta e previsão e testar conflito de recursos. Mudança de sprint exige decisão gerencial. Configurar revisão semanal e limiar de prazo próximo com Fabrício; não há automação agendada nesta etapa.

Equipe: autenticação individual, permissões operacionais e autoria; formulário/lista de tarefas com chat opcional. Conselho permanece separado; avaliar sua execução quando o fluxo de ideação for retomado.
