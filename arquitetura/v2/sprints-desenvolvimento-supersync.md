# Sprints — Escritório de Projetos no SuperSync

Versão 1 — 14/10/2026. Portfólio: SAERJ. Estado: planejamento; nenhuma sprint implementada nesta nova etapa.

## Direção confirmada

Desenvolver diretamente em `C:\Users\fabri\Projetos\supersync`, como app nativo, reutilizando padrões, autenticação, usuários e banco configurado do SuperSync. Não criar cópia da aplicação nem banco independente para operar o Escritório. Verificar o destino efetivo do banco antes de migrations: um checkout local pode estar configurado para acessar infraestrutura remota. Apresentar toda ação futura para aprovação prévia de Fabrício.

Escopo: projetos com documentação, artefatos, tarefas e histórico; demandas sem vínculo com projetos, como cotações e manutenções; permissões para cada usuário visualizar e operar somente os registros autorizados. Portfólio pessoal fora do escopo corporativo.

## Histórico e autorização

Pedido original: “Vamos zerar os arquivo de homologação e iniciar do zero, deixe apenas as documentações e crie um documento para as sprint de desenvolvimento ...”. Fabrício confirmou com “confirmado” o encerramento dos processos, remoção da cópia isolada e dados de homologação, preservação documental e criação deste plano. A limpeza foi realizada em 14/10/2026. As entregas e testes anteriores são históricos e não comprovam o novo app.

Referências: [implementação e histórico](implementacao-supersync.md), [especificação](especificacao.md), [modelo de dados](modelo-dados.md) e [operação do gestor](operacao-gestor.md). A direção atual substitui a proposta anterior de banco independente para esta integração; demais divergências devem ser resolvidas antes de implementar.

## Sequência proposta

Datas, duração, esforço, executor e participantes do aceite: a definir com Fabrício. A sequência não autoriza execução nem estabelece prazo contratado.

| Sprint | Entrega proposta | Critérios de aceite | Dependências | Estado |
|---|---|---|---|---|
| 0 — Diagnóstico e desenho | Inspecionar checkout original, padrões, autenticação, permissões, menus, armazenamento e destino do banco; apresentar entidades, telas e impacto. | Destinos confirmados sem divulgar segredos; alterações existentes preservadas; desenho e matriz de acesso revisados por Fabrício. | Aprovação da inspeção. | Não iniciada |
| 1 — App e permissões | Criar app nativo, integrar rotas/menu e usuários existentes; autorização por projeto/demanda, registro e operação. | Login nativo; listas, URLs diretas e downloads respeitam acesso; concessão e revogação verificadas; perfis aprovados. | Sprint 0; aprovação de arquivos e migrations. | Não iniciada |
| 2 — Projetos | Lista e ficha com campos, situação, participantes e navegação para documentos, artefatos, tarefas e histórico. | Cadastro explícito, consulta e filtros autorizados; autoria preservada; sem promoção automática de ideia. | Sprint 1; campos e estados aprovados. | Não iniciada |
| 3 — Demandas avulsas | Lista e ficha sem projeto obrigatório, incluindo cotações e manutenções; classificação, responsáveis e acompanhamento. | Sem projeto fictício; fluxos aprovados por tipo; acesso por demanda; vínculo posterior preserva origem e histórico. | Sprint 1; definição dos fluxos. | Não iniciada |
| 4 — Documentação e artefatos | Documentos/arquivos vinculados a projetos ou demandas, com originais, versões, autoria e armazenamento privado. | Upload/download autorizados; integridade e versões verificadas; limites e política de guarda aprovados. | Sprints 2 e 3; aprovação do armazenamento. | Não iniciada |
| 5 — Tarefas e histórico | Tarefas de projeto ou demanda, responsáveis, prazos, relatos, critérios e histórico das alterações. | Valores anteriores/autoria preservados; conflitos não sobrescrevem; relatos não concluem tarefas; encerramento por aceite autorizado. | Sprints 2 e 3; sprint 4 para evidências. | Não iniciada |
| 6 — Validação integrada | Verificar fluxos completos no SuperSync local, permissões, arquivos, migrations e regressões pertinentes; roteiro de aceite. | Aceite de Fabrício; acessos indevidos bloqueados; restauração de banco/arquivos em destino expressamente autorizado; pendências registradas. | Sprints anteriores; aprovação das validações e ambiente. | Não iniciada |

## Execução e validação

Antes de cada ação, apresentar escopo e impacto para aprovação. Antes de migrations, confirmar destino e solicitar aprovação específica. Cada sprint registra arquivos alterados, impacto no banco, testes pertinentes, evidências e aceite. Testar usuários com acesso amplo ao escopo concedido, limitado e sem acesso, incluindo URL direta, download e revogação. Verificar isolamento, originais, autoria, histórico e persistência. Os 67 testes da implementação descartada não validam esta nova etapa.

Publicação, push com implantação automática, produção, migração de documentos reais, integrações de IA e importação automática de reuniões estão fora da autorização deste plano. Markdown permanece oficial até decisão explícita de migração e corte de autoridade. A iniciativa SAERJ-IDEIA-002 não foi promovida a projeto.

## Próxima decisão

Solicitar aprovação da inspeção da sprint 0. Nenhum novo código ou migration foi criado durante a limpeza.
