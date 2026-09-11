# Escritório de Projetos

Base operacional de gestão de portfólio e projetos assistida por IA.

**Navegação:** [Portfólio](portfolio.md) · [Projetos](projetos/README.md) · [Conselho](conselho/README.md) · [Modelos](modelos/README.md) · [Contexto](CONTEXTO.md)

## Princípios

- A memória pertence ao projeto, não ao modelo de IA.
- Markdown é a fonte oficial de informação; conversas são contexto de trabalho.
- Documentação é um subproduto da gestão: toda discussão deve terminar em decisão, tarefa, pendência ou nenhuma ação necessária.
- O Conselho recomenda e acompanha; o humano direciona, decide e valida assuntos relevantes.

## Estrutura

```text
conselho/  papéis, protocolo e regras de governança
modelos/   modelos reutilizáveis dos registros de cada projeto
projetos/  memória de gestão de cada projeto
portfolio.md  visão executiva consolidada do portfólio
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

Consulte o [Conselho](conselho/README.md), seus [papéis](conselho/papeis.md), [protocolo](conselho/protocolo.md) e [regras](conselho/regras.md) antes de operar um projeto.

## Comunicação de status

Cada projeto pode manter uma `comunicacao.md` com sua matriz oficial de públicos, eventos, canais, frequência, responsáveis e aprovações. O modelo está em `modelos/comunicacao.md`.

No Windows, `scripts/Enviar-StatusProjeto.ps1` gera uma prévia ou envia o status pela API do ZeptoMail. Endereços e tokens não devem ser registrados nos arquivos do projeto; configure-os somente por parâmetros locais ou variáveis de ambiente. Consulte `scripts/README.md`.

## Limites de responsabilidade

Este repositório é a fonte canônica de gestão: portfólio, estado executivo, objetivo, escopo, prioridade, orçamento, riscos relevantes, governança, decisões gerenciais, tarefas, marcos e autorizações executivas.

Os repositórios de documentação e desenvolvimento de cada iniciativa continuam sendo as fontes de suas definições e entregas. Cada pasta em `projetos/` deve apontar claramente para esses repositórios e para suas evidências. Cada decisão deve ter uma única fonte canônica; quando uma decisão de implementação afetar a linha de base gerencial, o impacto e a aprovação devem ser registrados neste repositório.
