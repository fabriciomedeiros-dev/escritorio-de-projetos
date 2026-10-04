# Especificação funcional — versão 2

## Objetivo e escopo

Registrar trabalho sem atrito, recuperar informações com fontes e planejar entregas com capacidade e dependências. Prioridades: atividades registradas e planejamento. Inicialmente Fabrício usa o Codex; futuramente duas pessoas da equipe participam diretamente.

Tipos principais: ideia, solicitação, projeto e tarefa. Diretoria é origem, não tipo; orçamento é uma entrega possível. Uma solicitação pode gerar tarefas sem virar projeto. Inventariar máquinas para planejar reposição pode ser projeto. Orçamentos, demandas cotidianas e projetos futuros devem ser recuperáveis.

## Componentes

| Componente | Responsabilidade |
|---|---|
| Interface substituível | Receber texto e artefatos; apresentar resumo, consultas e aprovações; Codex inicialmente |
| Agente gestor único | Interpretar pedidos, propor classificação e coordenar operações autorizadas |
| Operações verificáveis | Persistir, verificar, consultar, aprovar, vincular fontes e calcular capacidade |
| Fonte operacional única | Estado, responsáveis, prazos, dependências, esforço e histórico |
| Documentação e artefatos | Originais, Markdown e fontes técnicas vinculados por identificadores |
| Proteção e recuperação | Cópia independente, exportação completa e restauração verificada |
| Visões e relatórios | Status e planejamento derivados, com fontes e data de atualização |

O agente não usa a memória da conversa como fonte oficial. Regras de integridade e gravação devem ser verificadas pelas operações de armazenamento, não apenas por instruções ao modelo.

## Independência de agente e interface

Requisito aprovado: Codex é a interface inicial, substituível por Claude Code ou outro agente. Dados, documentação, identidades, aprovações, regras de negócio e operações pertencem ao Escritório e não ao fornecedor do agente.

O núcleo expõe um contrato versionado de operações com entradas e resultados estruturados: portfólio, identidade verificada quando aplicável, ID da operação, versão esperada do registro, conteúdo e referências de evidência; resultados incluem IDs persistidos, verificação, lacunas, conflitos, erros e estado de proteção. A implementação e o transporte (CLI, API ou MCP) serão definidos posteriormente; o contrato não depende de sintaxe de chat, skills ou IDs de sessão de um produto.

Adaptadores traduzem as capacidades de cada cliente para esse contrato. Instruções e modelos portáveis definem o comportamento comum; configurações específicas de cada ferramenta apenas os referenciam. Permissões, aprovações, isolamento, idempotência e critérios de conclusão são aplicados pelo núcleo operacional, independentemente do modelo utilizado.

Trocar de agente não exige migrar os registros nem manter o histórico do chat anterior. O novo cliente consulta a mesma fonte, recupera pendências e originais e continua as operações autorizadas. Identificadores de chats são metadados opcionais de origem, nunca chaves canônicas ou prova de autorização. Funcionalidades de interface indisponíveis devem ter alternativa explícita, como aprovação textual registrada e consulta por links, sem reduzir as verificações.

## Captura e aprovação

- Capturar primeiro em caixa de entrada do portfólio, mesmo com campos ausentes; usar lacunas explícitas.
- Sugerir classificação no ato. Classificação inferida permanece proposta até confirmação; perguntar quando a ambiguidade afeta acompanhamento. Pendências continuam visíveis e entram na revisão semanal.
- Registrar automaticamente informações e compromissos explícitos fornecidos pelo usuário dentro das autorizações vigentes. Inferências não se tornam fatos.
- Aceitar reuniões por MCP de serviço de IA de transcrição ou por texto enviado com tópicos, sem exigir transcrição integral para a segunda forma. Seguir [entrada e revisão de reuniões](reunioes.md); provedor MCP e integração real ainda pendentes.
- Preservar documentos e transcrições originais; extrair decisões, tarefas, requisitos e prazos com localização na fonte.
- Todos os tópicos extraídos de reuniões precisam de revisão e aprovação de Fabrício, inclusive os que não exigem alteração. Permitir aprovação em lote com correções e rejeições individuais. Antes disso, somente o original e as propostas pendentes ficam registrados; não alterar a operação com o conteúdo proposto.
- Um original pode ser vinculado a vários registros do mesmo portfólio, evitando cópias concorrentes. Original que misture portfólios exige definição de acesso e separação antes de exposição.

## Entregas e evidência

- Toda entrega tem responsável pela conclusão total. Delegação não transfere essa responsabilidade automaticamente.
- Subtarefas e dependências mostram codificação, revisão, integração, validação e trabalhos de terceiros separadamente.
- Conclusão exige evidência compatível com o resultado esperado. Tela ou relatório anexado não basta por si só.
- Quando o agente não puder verificar o critério, registrar conclusão informada aguardando validação humana.
- Trabalho individual concluído com integração pendente é avanço parcial, não conclusão da entrega total.
- Preservar relatos conflitantes com autor e data; sinalizar divergência e solicitar esclarecimento. Recência não resolve conflito automaticamente.

## Planejamento e prioridade

- Sprints de aproximadamente uma semana; calendário de trabalho sem fins de semana por padrão, com exceções explícitas.
- Estimar esforço restante aproximado em horas, incluindo revisão, testes, integração e validação. Capacidade semanal por pessoa inclui reserva para demandas cotidianas.
- Separar meta desejada para a diretoria de previsão atual. Previsão tem método, entradas, data e incerteza; não representa garantia.
- Executores propõem prazos. Aceitar automaticamente quando compatíveis com restrições já aprovadas; conflito de capacidade, dependência ou meta requer decisão. Preservar prazo anterior e motivo de reprogramação.
- Diretoria, bugs e atualizações recebem destaque conforme urgência, impacto e prazo. O agente propõe prioridade; Fabrício decide trocas de sprint e alterações que afetam metas.
- Ausência de dados significa capacidade não avaliada, não ausência de sobrecarga. Previsão não deve inventar esforço nem percentual de conclusão.

## Alertas

Distinguir ausência de prazo, prazo vencido com entrega pendente e informação sem atualização. Tarefa concluída não fica desatualizada porque sua data passou. Revisão semanal, antecipada quando houver prazo próximo. Bloqueios exigem motivo, responsável pela próxima ação e data de acompanhamento. Silêncio não significa avanço.

Alertar durante registro e consulta sobre conflito de datas e capacidade; agrupar alertas repetidos sem mudança. Revisão semanal agendada é requisito futuro, ainda não configurado. Dia, horário e limiares de proximidade serão configurados na implantação.

## Recuperação, autoria e proteção

Responder status, motivo de pendência, trabalho restante e decisões com fontes, autor e data. Preservar distinção entre fato confirmado, relato, estimativa, hipótese e decisão.

Confirmar registrado somente após salvar e verificar leitura e vínculos dos anexos. Cada operação tem identificador e permite repetição sem duplicar registros. Falha parcial fica visível; não confirmar uma operação incompleta como íntegra.

Cópia independente tem estado separado da gravação. Não prometer perda zero enquanto existir pendência de proteção. Exportar todos os registros, originais, propostas pendentes, histórico e relações em formatos abertos; verificar integridade e testar restauração. Não exigir atividade em dias sem trabalho; reconciliar entradas recebidas com resultados persistidos.

## Ideias e portfólios

Captura simples → autorização de preparação → conselho → termo de abertura → avaliação da diretoria → promoção explícita. Manter os portões e documentos do protocolo existente; TAP não equivale a aprovação. Ideias não aparecem como projetos ativos.

Portfólios isolados por padrão. Toda operação declara portfólio ou solicita sua identificação. Visão conjunta de capacidade somente por solicitação explícita, sem misturar documentos ou relatórios executivos dos domínios.
