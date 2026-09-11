# Tarefas — SuperSync

**Navegação:** [Projeto](projeto.md) · [Governança](governanca.md) · [Módulos](modulos.md) · [Decisões](decisoes.md) · [Histórico](historico.md)

| ID | Tarefa | Responsável | Prazo | Prioridade | Status | Dependência / evidência |
|---|---|---|---|---|---|---|
| SS-001 | Confirmar sponsor, responsável gerencial, decisores e equipe executora. | Fabrício Medeiros | 11/09/2026 | Alta | Concluída | `governanca.md`; decisão de 11/09/2026. |
| SS-002 | Inventariar módulos e confirmar quais estão em produção, desenvolvimento ou inativos. | Fabrício Medeiros | A confirmar | Alta | Em andamento | `modulos.md`; faltam os módulos indicados em “Ainda a classificar”. |
| SS-003 | Avaliar a validade e a exposição das credenciais versionadas, revogar se necessário e propor retirada segura do histórico. | Alexandro Nascimento | Imediato | Crítica | `gcp_credencials.json`; não expor conteúdo. |
| SS-004 | Documentar e validar a reprodução local em ambiente limpo, incluindo configuração de exemplo, banco, migrations, seed e testes. | Responsável técnico a confirmar | A confirmar | Alta | `README.md`, `Dockerfile`, `requirements.txt`. |
| SS-005 | Identificar a sprint atual, sua linha de base, requisitos, critérios de aceite e revisão de código correspondente. | Responsável do projeto a confirmar | A confirmar | Alta | Planejamento e repositório de documentação. |
| SS-006 | Executar a primeira validação de sprint usando `modelos/validacao-sprint.md`. | Validadores funcional e técnico a confirmar | A confirmar | Alta | Conclusão de SS-002, SS-004 e SS-005. |
| SS-007 | Executar piloto do canal Teams `Demandas SuperSync` e avaliar adesão após 30 dias. | Fabrício Medeiros e Alexandro Nascimento | 11/10/2026 | Média | Não iniciada | Registro mínimo definido em `governanca.md`. |
| SS-008 | Definir o serviço compartilhado de usuários para o SAC, incluindo interface, segurança, disponibilidade e contingência. | Alexandro Nascimento e Fabrício Medeiros | A confirmar | Alta | Não iniciada | `servicos-compartilhados.md`; tarefa SAC-007. |
