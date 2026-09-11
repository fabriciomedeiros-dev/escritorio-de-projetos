# Contexto para continuidade em nuvem — Escritório de Projetos

## Objetivo deste projeto

O Escritório de Projetos e a base operacional para organizar, acompanhar e preservar a memoria do portfólio. Ele atua como um PMO assistido por IA: estrutura novos projetos, acompanha sua evolucao, identifica riscos e prepara comunicacoes executivas. Ele apoia a gestao, mas nao substitui as decisoes e validacoes humanas.

## Como a memoria funciona

- Arquivos Markdown versionados no Git sao a fonte oficial.
- Chats servem para analise e trabalho; fatos relevantes devem ser registrados nos arquivos.
- Cada projeto fica em `projetos/<nome-do-projeto>/` e usa os modelos existentes em `modelos/`.
- A pasta `conselho/` contem as regras de governanca, papeis e protocolo de trabalho.
- Este repositorio e a fonte canonica das decisoes gerenciais; o repositorio de cada iniciativa e a fonte das decisoes tecnicas e funcionais de implementacao e de suas evidencias.
- Cada decisao deve ter uma unica fonte canonica. Se uma decisao de implementacao afetar a linha de base gerencial, registrar aqui o impacto e a aprovacao correspondente.
- Cada iniciativa pode possuir tres camadas: gestao neste Escritorio, documentacao do comportamento esperado e desenvolvimento do que foi efetivamente implementado.
- O repositorio de desenvolvimento deve permitir reproduzir a aplicacao localmente e preservar stack, codigo, modelo de dados, migracoes, testes e evidencias de entrega.
- Divergencias entre sprint, documentacao e codigo devem ser classificadas como atendido, parcial, divergente, nao implementado ou adicional. Codigo adicional nao altera o escopo sem validacao humana.

## Estrutura do repositorio

```text
conselho/  governanca, papeis e protocolo operacional
modelos/   modelos de projeto, decisoes, tarefas e historico
projetos/  memoria especifica de cada projeto
```

## Principios inegociaveis

1. Diferenciar fato, hipotese, recomendacao, decisao e acao.
2. Nao tratar sugestao de IA como fato ou decisao aprovada.
3. Registrar mudancas relevantes com data, contexto e evidencia quando houver.
4. Nao inventar informacoes para preencher lacunas: usar `A confirmar` ou `Nao definido`.
5. Decisoes estrategicas, de escopo, prioridade, orcamento ou risco relevante exigem validacao humana.

## Ciclo de trabalho esperado

1. Ler o contexto e identificar fatos, lacunas e estado atual.
2. Analisar sob as perspectivas de negocio, tecnica e critica.
3. Apresentar recomendacao com impactos e, quando necessario, pedir decisao humana.
4. Converter decisoes aprovadas em tarefas objetivas.
5. Atualizar apenas os arquivos afetados: estado do projeto, decisoes, tarefas ou historico.

Toda discussao deve terminar com uma ou mais saidas: decisao, tarefa, pendencia ou nenhuma acao necessaria.

## Convencoes para os projetos

Para iniciar ou atualizar um projeto, use os modelos abaixo:

- `modelos/projeto.md`: estado atual e linha de base.
- `modelos/decisoes.md`: decisoes completas e justificadas.
- `modelos/tarefas.md`: acoes verificaveis, responsaveis e prazos.
- `modelos/historico.md`: fatos que explicam a evolucao do projeto.

Avalie sempre: prazo, escopo, qualidade, recursos, impedimentos e riscos, e resultado. Use `Controlado`, `Atencao` ou `Intervencao` somente com justificativa objetiva.

## Instrucoes para a IA na nuvem

Ao receber uma solicitacao:

1. Consulte primeiro os arquivos relevantes deste repositorio.
2. Declare lacunas e premissas antes de concluir algo incerto.
3. Separe claramente o que e fato do que e recomendacao.
4. Nao altere a linha de base, objetivo, escopo, prioridades ou riscos relevantes sem autorizacao humana explicita.
5. Quando houver autorizacao, registre a alteracao no arquivo correto e indique o que foi atualizado.
6. Termine com proximos passos claros e com a decisao requerida, se houver.

## Retomada do trabalho

Ao continuar este projeto em outro computador, leia este arquivo, `README.md`, `portfolio.md` e os arquivos de `conselho/`. Em seguida, pergunte qual projeto ou demanda deve ser tratado. O Git e a referencia para sincronizar os arquivos entre computadores.
