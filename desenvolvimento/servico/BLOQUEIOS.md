# Bloqueios, dependências e aceite — piloto local v2

Implementado no serviço local, com identidades sintéticas, migração 002, autorização pelo serviço e histórico por operação. Produção/SuperSync, identidade real e proteção independente permanecem pendentes.

## Dependência versus bloqueio

Uma **dependência** é necessária para terminar a entrega, mas outras partes podem continuar. `impede_avanco=false` não muda o estado da tarefa; a dependência pendente impede sua conclusão.

Um **bloqueio de avanço** é uma dependência com `impede_avanco=true`, informada explicitamente pelo gestor. Muda a tarefa aberta para `bloqueada` e preserva seu estado anterior. Não inferir essa decisão de qualquer dificuldade ou atraso informado em relato. Havendo vários bloqueios, resolver apenas um mantém o estado bloqueado; a última resolução restaura o estado anterior. Isso não conclui a tarefa nem dispensa dependências que ainda impeçam a entrega.

O incremento opera tarefas. Projetos não recebem automaticamente estado bloqueado ou nova data. A relação entre tarefas é recuperável; cálculo de impacto no cronograma e alertas proativos pertencem ao planejamento.

## Registro e acompanhamento

`registrar_dependencia` exige entrega, versão esperada, motivo, responsável pela próxima ação (membro ativo), próxima ação, data civil de acompanhamento, critério de resolução e indicação explícita de impedimento de avanço. Informar **ou** tarefa provedora **ou** nome do terceiro externo; não ambos. Provedor interno deve ser tarefa não cancelada do mesmo portfólio. Impedir ciclos, inclusive quando um pai depende de subtarefas e uma delas tenta depender do próprio pai.

Responsável pela próxima ação e responsável pela entrega total são papéis distintos. Nome de terceiro não atribui acesso ao sistema nem transfere responsabilidade. Uma pessoa interna deve assumir o acompanhamento. Se faltam informações, preservar o texto em captura/relato e destacar o que falta antes de formalizar a dependência; não inventar data ou responsável. O executor pode relatar dificuldade, mas registro/alteração/resolução formal são do gestor no piloto.

`atualizar_dependencia` permite alterar responsável pela próxima ação, próxima ação, acompanhamento e indicação explícita de impedimento de avanço, com motivo e versão da entrega. Retirar o impedimento de avanço permite retomar o trabalho, mas mantém a dependência pendente e continua impedindo conclusão. Não altera silenciosamente provedor, critério ou responsável total. As versões e histórico registram o acompanhamento anterior e posterior. Não há dispensa, cancelamento ou reabertura de dependência nesta entrega.

Consulta de tarefa mostra dependências e contadores `impedimentos`: pendências, bloqueios de avanço e acompanhamentos vencidos. Para cada dependência, o acompanhamento é `vencido`, `hoje`, `agendado` ou `encerrado`, calculado no fuso do portfólio. Datas não demonstram execução; silêncio mantém o estado pendente. Não existe monitor ou notificação automática configurada.

## Resolução

`resolver_dependencia` exige versão da entrega, ID da dependência, evidência verificada, justificativa e `criterio_atendido=true`, declarado no pedido explícito do gestor após examinar o critério e a evidência. O servidor verifica arquivo/tamanho/checksum e autorização; não interpreta automaticamente se uma imagem ou relatório comprova o resultado de negócio. Em produção, é necessário autenticar a pessoa que dá esse aceite.

Se há provedor interno, ele deve estar **concluído**; relato de código implementado ou execução parcial não basta. Verificar também integridade das evidências vinculadas ao provedor. Evidência e justificativa da resolução ficam vinculadas à tarefa e ao histórico, com ID da dependência. Resolução preserva o avanço parcial registrado e não conclui a entrega total.

Versão obsoleta, evidência ausente/divergente, provedor pendente ou dependência de outro registro/portfólio rejeitam o pedido sem aplicar mudanças. Reenviar o mesmo UUID/chave recupera a operação original; uma nova decisão sobre dependência já resolvida é rejeitada.

## Conclusão por aceite humano

`validar_conclusao` foi implementado somente para tarefas abertas, em `modo=aceite_humano`. Exige responsável total ativo, critério de conclusão definido, `criterio_atendido=true`, parecer explícito do gestor e IDs de evidências íntegras. Não pode haver bloqueio, dependência pendente ou subtarefa necessária não concluída/cancelada. Evidências e validação da versão final são salvas na mesma transação que o estado `concluida` e o histórico.

O modo `verificacao` automática continua indisponível. Declarar `aceite_humano` não comprova identidade real; neste piloto a identidade é sintética. O agente só envia o aceite após decisão humana explícita; upload, relato, resolução de bloqueio e término da data não autorizam conclusão. Solicitações/projetos, reabertura/cancelamento e novas regras de prazos/escopo continuam fora desse comando.

## Operação pelo cliente

```bash
.runtime/servico-venv/bin/python desenvolvimento/servico/cliente.py consultar --id ID-DA-TAREFA
.runtime/servico-venv/bin/python desenvolvimento/servico/cliente.py executar --pedido /caminho/pedido.json --chave chave-estavel
.runtime/servico-venv/bin/python desenvolvimento/servico/cliente.py operacao --id UUID-DA-OPERACAO
```

Os caminhos/IDs são ilustrativos. Preparar o JSON conforme OpenAPI, usando versão consultada e UUID/chave estáveis. Falha de confirmação após commit exige consulta da operação antes de reenvio. `estado=verificada` confirma gravação conferida; `protecao=pendente` mantém explícita a ausência de cópia independente. O mesmo contrato atende Codex, Claude Code e futuros clientes.

## Validação

`cenarios_dependencias.py`, chamado por `verificar_servico.py`, usa uma cópia temporária da base: dependência sem interromper avanço, múltiplos bloqueios, estado de retomada, acompanhamento e histórico, acesso restrito, responsabilidade total preservada, evidência ausente/corrompida, provedor parcialmente entregue, ciclos concorrentes, conclusão de pai/subtarefas e aceite recuperável após perda da confirmação. O teste de esquema confere dump/restauração das migrações 001 e 002 e rejeições de conclusão inválida.
