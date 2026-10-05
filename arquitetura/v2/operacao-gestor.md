# Operação do gestor no piloto local — versão 2

Instruções comuns para Codex, Claude Code ou outro cliente autorizado. O cliente de referência usa o contrato HTTP, não SQL administrativo. O portfólio `demo_escritorio` contém somente demonstrações; não importar dados reais enquanto proteção e corte de autoridade estiverem pendentes.

## Entrada guiada

Seguir [menu e termos de entrada](menu-gestor.md) para acolhimento, seleção de domínio/fonte, opções numeradas e questionamentos graduais. A navegação não substitui consulta nem concede autorização.

## Abertura e consulta

Ao receber “oi” em contexto de gestão ou “consultar demandas”, identificar portfólio e fonte antes de mostrar dados. No piloto demonstrativo, consultar o serviço; nos portfólios reais, consultar os documentos oficiais. Mostrar portfólio, título, tipo, estado, responsável, prazo e lacunas, sem inventar avanço. Percorrer as páginas quando o pedido exigir todos os registros. O cliente aceita filtros `--id`, `--assunto`, `--tipo`, `--estado`, `--limite` e `--cursor`; a busca por assunto cobre título e resultado esperado.

Não depender de IDs lembrados do chat para recuperar complementos: cada ficha inclui `entradas`, com os textos originais vinculados, origem e data. Campos em `origem` são contexto informado, não prova de autenticação ou permissão. Distinguir relatos, decisões e autorizações.

## Captura e classificação

Preservar o texto em `capturar_entrada`. Quando o usuário solicitar explicitamente uma ideia, solicitação ou tarefa, criar o registro com referência à entrada e informar a classificação aplicada. Se estiver ambíguo, deixar em triagem e solicitar a informação necessária. Não transformar ideia em projeto nem criar tarefa implicitamente. Classificação sugerida não é classificação confirmada.

## Complemento e correção

Consultar a ficha e sua versão. Capturar o complemento original com `origem.registro_id` apontando ao registro correto e contexto de origem. Depois executar `atualizar_registro` com `registro_id`, `versao_esperada`, `motivo`, `entrada_id` e, quando solicitado, `alteracoes`. No piloto, apenas gestor pode atualizar conteúdo de ideias e solicitações abertas. Campos permitidos: título, resultado esperado e critério de conclusão; não inferir critérios aprovados.

Preservar o conteúdo existente ao consolidar: incluir definições novas sem remover requisitos anteriores não revogados. O comando também permite apenas vincular uma entrada, sem mudar campos. O serviço valida o vínculo e guarda os valores anteriores e posteriores em histórico, na mesma transação. Referências ficam no campo estruturado `origem` e são verificadas pelo serviço; não há nova tabela de vínculos com FK nesta entrega. Uma entrada já vinculada não pode ser reatribuída silenciosamente.

Um conflito de versão exige nova consulta e avaliação da mudança antes de preparar outro pedido. Falha após commit exige consultar o UUID da operação antes de repetir. Manter UUID e chave estáveis para repetição do mesmo pedido. Confirmar somente após resposta verificada; em falha parcial, informar o que ficou salvo e o que está pendente.

## Resposta e limites

Mostrar resumo salvo, identificador, situação, lacunas e pendência de proteção. Uma ideia pode estar capturada sem responsável, prazo ou esforço; lacunas não equivalem a atraso. Relatos de tarefas não concluem entregas nem aceitam prazos automaticamente.

Reuniões estão disponíveis somente no piloto local, conforme limites abaixo. Conclusão de tarefa está disponível somente por aceite humano explícito, conforme seção abaixo. Não anunciar promoção, verificação automática, conclusão de solicitação/projeto, planejamento ou proteção independente como disponíveis. Estados mudam apenas por bloqueio/retomada e aceite; cadastro de usuário, meta, prioridade e mudança de responsável total continuam fora desta entrega. A política de acesso técnico segue `seguranca-chat.md`; identidade sintética de demonstração não comprova autorização administrativa.

## Anexos e evidências

No piloto, use `cliente.py anexar` para arquivo local de até 512 KiB, com UUID e chave estáveis. Preserve o original, confirme tamanho/checksum no serviço e só então vincule ao registro na finalidade solicitada. Não basta receber um arquivo no chat para confirmar que ele está registrado. Preparação, envio e vínculo têm confirmações separadas: comunicar a etapa pendente em caso de falha.

A ficha apresenta ID, nome, checksum e integridade de suas fontes; use download autenticado para recuperar o original. Nome do arquivo não é identificador. Não apresentar evidência como conclusão nem tratar upload de reunião como aprovação de seus tópicos. Em original ausente ou divergente, explicitar a falha de integridade e não confirmar recuperação completa. A proteção independente continua pendente.

## Reuniões — piloto implementado

Seguir [fluxo de reuniões](../../desenvolvimento/servico/REUNIOES.md). Importar original manual ou resposta de MCP autorizado com `cliente.py importar-reuniao`; consultar por `cliente.py reunioes`. Síntese e identificação de tópicos são propostas produzidas pelo agente cliente, a partir das fontes, sem modelo embutido no servidor.

Apresentar primeiro a ata resumida agrupando apresentações e discussões; depois revisar os encaminhamentos por grupos, com contador e opções. Registrar a aprovação explícita da ata e de todos os tópicos nas revisões exatas; nenhuma aprovação deve ser inferida do original. Decisões parciais são recuperáveis e não aplicam ações. Correções criam nova revisão e não herdam aprovações.

Somente após revisão integral, enviar `efetivar_topicos_reuniao` com versão esperada. A API aplica ações suportadas sem duplicação e preserva fontes/histórico. Não confirmar responsáveis/prazos aceitos, criação de projeto ou conclusão como efeito desse fluxo. Dados reais dos ensaios documentais permanecem fora do banco sintético; autenticação real e proteção continuam pendentes.

## Bloqueios e conclusão de tarefa

Seguir [regras do piloto](../../desenvolvimento/servico/BLOQUEIOS.md). Diferenciar dependência necessária à entrega de impedimento de avanço; não transformar toda dificuldade em bloqueio. Capturar relato com lacunas, depois obter motivo, próxima ação, responsável interno, acompanhamento e critério antes de formalizar. Gestor registra/altera/resolve; executor relata.

Resolver exige decisão explícita sobre atendimento do critério e evidência íntegra; provedor interno deve estar concluído. A última resolução de bloqueio restaura o estado anterior, sem concluir a entrega. Consultas mostram acompanhamentos vencidos, sem automação agendada.

`validar_conclusao` em `aceite_humano` exige decisão explícita do gestor, critério definido/atendido, responsável e evidências, sem dependências/subtarefas necessárias pendentes. Não inferir aceite de relato, upload, silêncio ou resolução de bloqueio. Identidade sintética não comprova identidade real.
