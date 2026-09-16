# Escritório de Projetos

Base operacional de gestão de portfólio e projetos assistida por IA.

**Navegação:** [Portfólio](portfolio.md) · [Tarefas do Escritório](tarefas-escritorio.md) · [Mensuração de ganhos e valor da TI](atividades/mensuracao-ganhos-valor-ti.md) · [Contratações de ferramentas](atividades/avaliacao-contratacoes-ferramentas.md) · [Divulgação no Trello](atividades/divulgacao-andamento-trello.md) · [Projetos](projetos/README.md) · [Conselho](conselho/README.md) · [Modelos](modelos/README.md) · [Contexto](CONTEXTO.md)

## Princípios

- A memória pertence ao projeto, não ao modelo de IA.
- Markdown é a fonte oficial de informação; conversas são contexto de trabalho.
- Documentação é um subproduto da gestão: toda discussão deve terminar em decisão, tarefa, pendência ou nenhuma ação necessária.
- O Conselho recomenda e acompanha; o humano direciona, decide e valida assuntos relevantes.
- Toda nova proposta deve explicitar como o valor será medido; projetos atuais incorporarão essa mensuração progressivamente, sempre distinguindo fatos, estimativas e hipóteses.

## Estrutura

```text
conselho/  papéis, protocolo e regras de governança
modelos/   modelos reutilizáveis dos registros de cada projeto
projetos/  memória de gestão de cada projeto
portfolio.md  visão executiva consolidada do portfólio
tarefas-escritorio.md  iniciativas transversais e evolução do PMO
```

## Camadas de informação

O Escritório opera três camadas complementares, cada uma com sua própria autoridade:

1. **Gestão:** este repositório é a fonte canônica de objetivo, escopo gerencial, prioridade, orçamento, riscos, marcos, decisões e acompanhamento.
2. **Documentação do projeto:** o repositório indicado por cada iniciativa é a fonte do comportamento esperado, requisitos, regras e critérios de aceite.
3. **Desenvolvimento:** o repositório de código é a fonte do que foi efetivamente implementado, incluindo stack, modelos de dados, migrações, testes e instruções de execução local.

O código não altera automaticamente o escopo aprovado. Diferenças entre o planejado e o implementado devem ser classificadas, avaliadas e, quando relevantes, submetidas à decisão humana antes de atualizar a linha de base.

## Como iniciar um projeto

1. Crie `projetos/<nome-do-projeto>/`.
2. Copie os arquivos de `modelos/` para a nova pasta.
3. Preencha primeiro `projeto.md` com a linha de base e o estado atual conhecido.
4. Registre somente decisões, tarefas e acontecimentos que alterem ou expliquem o projeto.
5. Preencha a mensuração de valor com objetivo, resultado-chave, linha de base, meta, evidências e nível de confiança.

## Mensuração de valor

O Escritório mantém uma linha transversal de mensuração de valor aplicável a cada nova proposta e, progressivamente, aos projetos existentes. A análise pode combinar custo interno, referência de mercado, custo evitado, ganhos financeiro e operacional, produtividade ou capacidade liberada, risco mitigado e públicos beneficiados. Toda medida deve indicar sua evidência e ser classificada como `Confirmado`, `Estimado` ou `Hipótese`. Use `modelos/mensuracao-valor.md` e acompanhe a implantação em `tarefas-escritorio.md`.

Consulte o [Conselho](conselho/README.md), seus [papéis](conselho/papeis.md), [protocolo](conselho/protocolo.md) e [regras](conselho/regras.md) antes de operar um projeto.

## Comunicação de status

Cada projeto pode manter uma `comunicacao.md` com sua matriz oficial de públicos, eventos, canais, frequência, responsáveis e aprovações. O modelo está em `modelos/comunicacao.md`.

O Trello será utilizado como camada de divulgação do andamento do portfólio. Ele não substitui os registros canônicos: os cartões devem resumir informações confirmadas no Escritório e seguir o fluxo definido em [Divulgação do andamento dos projetos no Trello](atividades/divulgacao-andamento-trello.md).

No Windows, `scripts/Enviar-StatusProjeto.ps1` gera uma prévia ou envia o status pela API do ZeptoMail. Endereços e tokens não devem ser registrados nos arquivos do projeto; configure-os somente por parâmetros locais ou variáveis de ambiente. Consulte `scripts/README.md`.

## Avaliação de contratações

Solicitações para contratação, renovação ou substituição de ferramentas e serviços são conduzidas pela atividade transversal de [Avaliação de Contratações de Ferramentas e Serviços](atividades/avaliacao-contratacoes-ferramentas.md). Cada solicitação deve comparar alternativas, explicitar critérios, custos, riscos e condições, apresentar uma recomendação e registrar a decisão humana. O Trello acompanha o fluxo, mas não substitui o arquivo canônico nem a aprovação formal.

## Limites de responsabilidade

Este repositório é a fonte canônica de gestão: portfólio, estado executivo, objetivo, escopo, prioridade, orçamento, riscos relevantes, governança, decisões gerenciais, tarefas, marcos e autorizações executivas.

Os repositórios de documentação e desenvolvimento de cada iniciativa continuam sendo as fontes de suas definições e entregas. Cada pasta em `projetos/` deve apontar claramente para esses repositórios e para suas evidências. Cada decisão deve ter uma única fonte canônica; quando uma decisão de implementação afetar a linha de base gerencial, o impacto e a aprovação devem ser registrados neste repositório.
