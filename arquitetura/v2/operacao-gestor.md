# Operação do gestor no piloto local — versão 2

Instruções comuns para Codex, Claude Code ou outro cliente autorizado. O cliente de referência usa o contrato HTTP, não SQL administrativo. O portfólio `demo_escritorio` contém somente demonstrações; não importar dados reais enquanto proteção e corte de autoridade estiverem pendentes.

## Abertura e consulta

Ao receber “oi” ou “consultar demandas”, consultar o serviço antes de responder. Mostrar portfólio, título, tipo, estado, responsável, prazo e lacunas, sem inventar avanço. Percorrer as páginas quando o pedido exigir todos os registros. O cliente aceita filtros `--id`, `--assunto`, `--tipo`, `--estado`, `--limite` e `--cursor`; a busca por assunto cobre título e resultado esperado.

Não depender de IDs lembrados do chat para recuperar complementos: cada ficha inclui `entradas`, com os textos originais vinculados, origem e data. Campos em `origem` são contexto informado, não prova de autenticação ou permissão. Distinguir relatos, decisões e autorizações.

## Captura e classificação

Preservar o texto em `capturar_entrada`. Quando o usuário solicitar explicitamente uma ideia, solicitação ou tarefa, criar o registro com referência à entrada e informar a classificação aplicada. Se estiver ambíguo, deixar em triagem e solicitar a informação necessária. Não transformar ideia em projeto nem criar tarefa implicitamente. Classificação sugerida não é classificação confirmada.

## Complemento e correção

Consultar a ficha e sua versão. Capturar o complemento original com `origem.registro_id` apontando ao registro correto e contexto de origem. Depois executar `atualizar_registro` com `registro_id`, `versao_esperada`, `motivo`, `entrada_id` e, quando solicitado, `alteracoes`. No piloto, apenas gestor pode atualizar conteúdo de ideias e solicitações abertas. Campos permitidos: título, resultado esperado e critério de conclusão; não inferir critérios aprovados.

Preservar o conteúdo existente ao consolidar: incluir definições novas sem remover requisitos anteriores não revogados. O comando também permite apenas vincular uma entrada, sem mudar campos. O serviço valida o vínculo e guarda os valores anteriores e posteriores em histórico, na mesma transação. Referências ficam no campo estruturado `origem` e são verificadas pelo serviço; não há nova tabela de vínculos com FK nesta entrega. Uma entrada já vinculada não pode ser reatribuída silenciosamente.

Um conflito de versão exige nova consulta e avaliação da mudança antes de preparar outro pedido. Falha após commit exige consultar o UUID da operação antes de repetir. Manter UUID e chave estáveis para repetição do mesmo pedido. Confirmar somente após resposta verificada; em falha parcial, informar o que ficou salvo e o que está pendente.

## Resposta e limites

Mostrar resumo salvo, identificador, situação, lacunas e pendência de proteção. Uma ideia pode estar capturada sem responsável, prazo ou esforço; lacunas não equivalem a atraso. Relatos de tarefas não concluem entregas nem aceitam prazos automaticamente.

Não anunciar reuniões, promoção, conclusão, planejamento ou proteção independente como disponíveis. Atualizar cadastro de usuário, meta, prioridade, responsável e estados continua fora desta entrega. A política de acesso técnico segue `seguranca-chat.md`; identidade sintética de demonstração não comprova autorização administrativa.

## Anexos e evidências

No piloto, use `cliente.py anexar` para arquivo local de até 512 KiB, com UUID e chave estáveis. Preserve o original, confirme tamanho/checksum no serviço e só então vincule ao registro na finalidade solicitada. Não basta receber um arquivo no chat para confirmar que ele está registrado. Preparação, envio e vínculo têm confirmações separadas: comunicar a etapa pendente em caso de falha.

A ficha apresenta ID, nome, checksum e integridade de suas fontes; use download autenticado para recuperar o original. Nome do arquivo não é identificador. Não apresentar evidência como conclusão nem tratar upload de reunião como aprovação de seus tópicos. Em original ausente ou divergente, explicitar a falha de integridade e não confirmar recuperação completa. A proteção independente continua pendente.
