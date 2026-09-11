# Governança — SuperSync

**Navegação:** [Projeto](projeto.md) · [Módulos](modulos.md) · [Decisões](decisoes.md) · [Tarefas](tarefas.md) · [Portfólio](../../portfolio.md)

Documento executivo. Manter em uma página e registrar detalhes somente quando necessários para decisão ou execução.

## Papéis

| Papel | Responsável | Autoridade principal |
|---|---|---|
| Sponsor executivo | Diretoria, representada por Marcelo Rebelo | Direcionamento final, prioridades relevantes e aprovação financeira |
| Gerente do projeto | Fabrício Medeiros | Triagem, planejamento, sprints/ciclos, riscos, status e recomendação executiva |
| Desenvolvimento e segurança | Alexandro Nascimento | Código, publicação controlada, credenciais, acessos técnicos e vulnerabilidades |
| Dados | Filipe Fachetti | Qualidade dos dados do Data Lake, queries, consultas e análises |
| Dono funcional | Definido por módulo | Requisitos, critérios de aceite e aprovação funcional |

## Fluxo de demanda

1. Qualquer área pode solicitar.
2. Fabrício faz a triagem e autoriza a entrada no planejamento.
3. Alexandro não inicia demanda direta sem essa validação, salvo incidente urgente.
4. Incidente urgente pode ser corrigido imediatamente e deve ser sinalizado a Fabrício com causa, impacto e evidência.
5. Funcionalidade já desenvolvida sem planejamento é tratada como entrega adicional e não altera o escopo automaticamente.

## Entrega e produção

- Cada módulo define dono funcional e critérios de aceite antes do ciclo de entrega.
- Alexandro pode publicar com acesso restrito para validação controlada.
- A liberação ampla exige aceite do dono funcional e autorização conjunta de Fabrício e Marcelo.

## Cadência e comunicação

- Acompanhamento executivo semanal do SuperSync.
- Ciclos de entrega definidos por módulo, conforme tamanho, urgência e dependências.
- Status para Marcelo, Alexandro, Filipe e o dono funcional do módulo em pauta.
- Piloto de 30 dias do canal Teams `Demandas SuperSync`, de 11/09/2026 a 11/10/2026.
- Registro mínimo: área, solicitante, módulo, necessidade e urgência. Pedido recebido por WhatsApp deve ser resumido no canal.

## Financeiro

Fabrício apresenta recomendação resumida. Marcelo e a diretoria aprovam compras, fornecedores, infraestrutura e demais custos usando o [modelo de decisão financeira](../../modelos/decisao-financeira.md).
