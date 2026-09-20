# Projetos

**Navegação:** [Início](../../../README.md) · [Portfólio SAERJ](../portfolio.md) · [Modelos](../../../modelos/README.md) · [Conselho](../../../conselho/README.md)

## Projetos ativos

- [SAC — Supermarket](sac-supermarket/projeto.md)
- [SuperSync — Intranet Rede Supermarket](supersync/projeto.md)
- [CRM Rock (antiga BNEX)](crm-rock/projeto.md)
- [Integração com a 99Food](integracao-99food/projeto.md)

Crie uma pasta por projeto usando um identificador claro, por exemplo `integracao-crm`.

Estrutura mínima de cada projeto:

```text
portfolios/saerj/projetos/<nome-do-projeto>/
├── projeto.md
├── decisoes.md
├── tarefas.md
├── historico.md
└── desenvolvimento.md  # quando houver repositório de código
```

Copie os arquivos correspondentes de `../../../modelos/` antes de iniciar o registro.

Todo `projeto.md` deve declarar o portfólio `saerj` e possuir um identificador iniciado por `SAERJ-`.
﻿# Projetos do Portfólio

Cada subpasta representa a memória gerencial de uma iniciativa do portfólio.

Ela deve conter, no mínimo:

- `projeto.md`: estado executivo e linha de base;
- `decisoes.md`: decisões relevantes e sua justificativa;
- `tarefas.md`: plano de ação e acompanhamento;
- `historico.md`: fatos que explicam a evolução.
- `desenvolvimento.md`: revisão observada, stack, estrutura implementada, reprodução local e evidências técnicas.

Não copie documentação técnica ou funcional para esta pasta. Registre links e referências ao repositório de origem.

Quando houver validação de sprint, use `modelos/validacao-sprint.md` e identifique a linha de base planejada e o commit, tag ou branch exatos que foram inspecionados.
