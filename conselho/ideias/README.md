# Ideias em avaliação

**Navegação:** [Comitê](../README.md) · [Protocolo](../protocolo.md) · [Regras](../regras.md) · [Modelos](../../modelos/README.md)

Esta pasta contém exclusivamente iniciativas que ainda não foram aprovadas como projetos do Escritório de Projetos.

## Estrutura

```text
conselho/ideias/
├── saerj/
│   └── <identificador-da-ideia>/
└── pessoal/
    └── <identificador-da-ideia>/
```

Cada ideia pode conter, conforme avança:

```text
<identificador-da-ideia>/
├── 01-ficha-ideia.md
├── 02-termo-abertura-preliminar.md
└── 03-canvas-modelo-negocio.md
```

## Estados permitidos

- `Em descoberta`
- `Aguardando decisão da rodada 1`
- `Em definição`
- `Aguardando decisão da rodada 2`
- `Em análise de mercado`
- `Aguardando decisão final`
- `Em experimento`
- `Reformulação solicitada`
- `Arquivada`

`Projeto ativo` não é um estado permitido nesta pasta. Quando uma ideia for promovida, seu dossiê deve ser movido para `portfolios/<portfolio>/projetos/<projeto>/iniciacao/`, e a iniciativa passa a seguir a governança operacional do Escritório.

## Isolamento

O identificador do portfólio é obrigatório desde a entrada. Agentes, relatórios e pesquisas devem consultar somente a pasta do portfólio informado. Método e modelos podem ser compartilhados; contexto, documentos e evidências não podem atravessar portfólios.
