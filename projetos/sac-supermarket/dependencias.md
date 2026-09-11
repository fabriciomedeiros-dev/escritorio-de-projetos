# Dependências — SAC — Supermarket

**Navegação:** [Projeto](projeto.md) · [Tarefas](tarefas.md) · [SuperSync](../supersync/projeto.md) · [Serviços do SuperSync](../supersync/servicos-compartilhados.md)

| Dependência | Projeto provedor | Dono provedor | Dono consumidor | Situação | Critério de aceite | Risco/contingência |
|---|---|---|---|---|---|---|
| Gestão de usuários e autenticação | SuperSync | Alexandro Nascimento | Fabrício Medeiros | Planejada; validação técnica pendente | Perfis do SAC autenticam e acessam somente as funções autorizadas | Definir comportamento em indisponibilidade e evitar acoplamento não documentado |

O SAC permanece independente na gestão. Requisitos de perfis e permissões pertencem ao SAC; segurança, disponibilidade e compatibilidade do serviço pertencem ao SuperSync.
