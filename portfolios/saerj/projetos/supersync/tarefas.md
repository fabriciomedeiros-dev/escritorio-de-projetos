# Tarefas — SuperSync

**Navegação:** [Projeto](projeto.md) · [Governança](governanca.md) · [Módulos](modulos.md) · [Decisões](decisoes.md) · [Histórico](historico.md)

| ID | Tarefa | Responsável | Prazo | Prioridade | Status | Dependência / evidência |
|---|---|---|---|---|---|---|
| SS-001 | Confirmar sponsor, responsável gerencial, decisores e equipe executora. | Fabrício Medeiros | 11/09/2026 | Alta | Concluída | `governanca.md`; decisão de 11/09/2026. |
| SS-002 | Inventariar módulos e confirmar quais estão em produção, desenvolvimento ou inativos. | Fabrício Medeiros | A confirmar | Alta | Em andamento | `modulos.md`; faltam os módulos indicados em “Ainda a classificar”. |
| SS-003 | Avaliar a validade e a exposição das credenciais versionadas, revogar se necessário e propor retirada segura do histórico. | Alexandro Nascimento | Imediato | Crítica | Encerrada — desconsiderada no status | Direcionamento gerencial de 24/09/2026: credencial GCP não será considerada risco deste projeto. |
| SS-004 | Documentar e validar a reprodução local em ambiente limpo, incluindo configuração de exemplo, banco, migrations, seed e testes. | Responsável técnico a confirmar | A confirmar | Alta | Em andamento | Ambiente local existente passou em `manage.py check` e 551 testes; ambiente limpo, seed e configuração de exemplo continuam pendentes. |
| SS-005 | Identificar a sprint atual, sua linha de base, requisitos, critérios de aceite e revisão de código correspondente. | Responsável do projeto a confirmar | A confirmar | Alta | Em andamento | Revisão candidata atualizada para `bba8f83`; ainda faltam a linha de base planejada e os critérios de aceite vinculados. |
| SS-006 | Executar a primeira validação de sprint usando `../../../../modelos/validacao-sprint.md`. | Fabrício Medeiros e equipe do projeto | 24/09/2026 | Alta | Concluída | Todas as funcionalidades planejadas foram validadas e estão OK; `bba8f83` passou em 551 testes. |
| SS-007 | Executar piloto do canal Teams `Demandas SuperSync` e avaliar adesão após 30 dias. | Fabrício Medeiros e Alexandro Nascimento | 11/10/2026 | Média | Não iniciada | Registro mínimo definido em `governanca.md`. |
| SS-008 | Definir o serviço compartilhado de usuários para o SAC, incluindo interface, segurança, disponibilidade e contingência. | Alexandro Nascimento e Fabrício Medeiros | A confirmar | Alta | Não iniciada | `servicos-compartilhados.md`; tarefa SAC-007. |
| SS-010 | Definir e implementar justificativas padronizadas para o processo de cobrança. | Filipe Fachetti e Alexandro Nascimento | 24/09/2026 | Alta | Concluída | Fluxo implementado e validado, com catálogo de motivos, justificativa por nota, análise e decisão de cobrança. |
| SS-011 | Definir escopo, autenticação, segregação de dados, segurança, testes e cronograma da área externa do associado. | Fabrício Medeiros, Alexandro Nascimento e Filipe Fachetti | 14/10/2026 | Alta | Implementação e validação concluídas — aprovação executiva pendente | Todas as funcionalidades planejadas foram validadas e estão OK; próxima etapa é a apresentação a Marcelo Rebelo. |
| SS-012 | Apresentar as implementações do Portal do Associado e obter aprovação executiva. | Fabrício Medeiros | A agendar | Alta | Não iniciada | Reunião com Marcelo Rebelo; registrar aprovação, condicionantes e encaminhamento das melhorias. |
| SS-013 | Consolidar, priorizar e implementar as sugestões de melhoria do Portal do Associado. | Fabrício Medeiros, Alexandro Nascimento e Filipe Fachetti | Após aprovação | Média | Planejada | Melhorias não bloqueiam a aprovação do escopo atual e serão tratadas no ciclo seguinte. |
| SS-014 | Apresentar o Portal do Associado aos diretores após a aprovação de Marcelo Rebelo. | Fabrício Medeiros | Após SS-012 | Alta | Planejada | Demonstrar funcionalidades validadas e alinhar a implantação com a diretoria. |
| SS-015 | Definir os responsáveis e pontos focais do Portal em cada associado. | Fabrício Medeiros e diretores | Após SS-014 | Alta | Planejada | Registrar nome, função, contato, responsabilidades e cobertura de cada associado. |
| SS-016 | Concluir a análise de crescimento de vendas da Apuração de Contratos. | Filipe Fachetti | 06/10/2026 | Alta | Em análise | Resultado da análise e evidências utilizadas. |
| SS-017 | Entregar o relatório de triangulação para evoluir o processo e iniciar a homologação. | Filipe Fachetti | 01/09/2026, conforme informado | Alta | Pendente; prazo a confirmar | A data informada é anterior à reunião de 29/09; confirmar se houve erro de mês antes de replanejar. |
| SS-018 | Definir o processo de devolução de mercadorias pelo fornecedor. | A confirmar | Não definido | Média | Não iniciada | Definir responsável, fluxo, regras, evidências e critérios de aceite. |
| SS-019 | Estruturar a análise gerencial dos dados da Apuração de Contratos. | A confirmar | Novembro ou dezembro de 2026 | Alta | Planejada | Confirmar mês, responsável, fontes e critérios de aceite; indicadores registrados na reunião de 29/09. |

## Atividade transferida

A antiga tarefa SS-009, referente à mensuração dos ganhos de Acordos Comerciais, foi transferida para a atividade transversal [Mensuração de Ganhos e Valoração da Área de TI](../../../../atividades/mensuracao-ganhos-valor-ti.md), acompanhada pelas tarefas PMO-001 a PMO-005. O SuperSync permanece como fonte das evidências do primeiro caso de aplicação.

## Indicadores previstos para SS-019

- valor apurado × valor realizado;
- contratos com upload;
- contratos com venda e contratos apurados;
- linha do tempo de término da apuração;
- contratos que precisam de renovação e seus estados;
- contratos novos;
- percentual do faturamento dentro de contrato;
- percentual do faturamento de contrato da rede em relação à compra total dos associados;
- percentual de produtos cobertos por mês;
- peso da evasão mês a mês.

As informações requeridas pela DHS para auditoria e desligamento do Observador são acompanhadas no projeto [Desligamento do Observador](../desligamento-observador/projeto.md).
