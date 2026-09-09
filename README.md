# Escritório de Projetos

Base operacional de gestão de portfólio e projetos assistida por IA.

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

## Como iniciar um projeto

1. Crie `projetos/<nome-do-projeto>/`.
2. Copie os arquivos de `modelos/` para a nova pasta.
3. Preencha primeiro `projeto.md` com a linha de base e o estado atual conhecido.
4. Registre somente decisões, tarefas e acontecimentos que alterem ou expliquem o projeto.

Consulte [papéis do Conselho](conselho/papeis.md), [protocolo](conselho/protocolo.md) e [regras](conselho/regras.md) antes de operar um projeto.

## Limites de responsabilidade

Este repositório é a fonte oficial de gestão: portfólio, estado executivo, riscos, decisões, tarefas, marcos e notificações.

O repositório de cada iniciativa continua sendo a fonte de suas entregas técnicas e funcionais. Cada pasta em `projetos/` deve apontar claramente para esse repositório e para suas evidências.
