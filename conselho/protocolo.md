# Protocolo Operacional do Comitê

**Navegação:** [Conselho](README.md) · [Papéis](papeis.md) · [Regras](regras.md) · [Modelos](../modelos/README.md)

## Regra de entrada

Toda nova ideia deve informar, no mínimo:

1. portfólio de destino pretendido;
2. descrição simples da ideia;
3. proponente, quando conhecido.

O Orquestrador cria a pasta `conselho/ideias/<portfolio>/<identificador>/` e inicia a [Ficha de ideia](../modelos/ficha-ideia.md). Nesse momento, a iniciativa ainda não é projeto, não integra o portfólio e não recebe classificação de saúde.

## Ciclo pré-projeto

```text
Ideia inicial
  → Rodada 1: descoberta e brainstorm
  → Portão humano 1
  → Rodada 2: definição e TAP preliminar
  → Portão humano 2
  → Rodada 3: mercado e modelo de negócio
  → Decisão humana final
  → promoção, experimento, reformulação ou arquivamento
```

As rodadas são progressivas. Podem ocorrer em mais de uma sessão, mas não devem ser tratadas como concluídas sem documento, critérios de saída e decisão do respectivo portão.

## Rodada 1 — Descoberta e brainstorm

### Objetivo

Transformar uma ideia simples em uma oportunidade compreensível, explorando problemas, objetivos, públicos, requisitos preliminares, restrições e alternativas sem assumir que a solução original é a única possível.

### Dinâmica

1. Registrar a ideia na forma apresentada pelo proponente.
2. Investigar o problema, o público afetado, a situação atual e o impacto.
3. Formular objetivo e resultados esperados preliminares.
4. Explorar linhas de possibilidade, incluindo não agir, melhorar processo, adquirir, integrar, desenvolver ou experimentar.
5. Identificar requisitos iniciais, restrições, premissas e hipóteses.
6. Registrar perguntas em aberto e evidências necessárias.
7. O Auditor testa premissas e o Orquestrador consolida convergências, divergências e recomendação.

### Resultado obrigatório

[Ficha de ideia](../modelos/ficha-ideia.md).

### Critério de saída

Problema, objetivo, público, possibilidades, requisitos preliminares, restrições e lacunas estão explícitos, mesmo que ainda não estejam confirmados.

### Portão humano 1

`Avançar para definição`, `Investigar`, `Reformular` ou `Arquivar`.

## Rodada 2 — Definição do projeto

### Objetivo

Selecionar uma direção de referência e delimitar uma proposta de projeto, ainda sem autorizar sua execução ou entrada no portfólio.

### Dinâmica

1. Confirmar problema, justificativa e objetivo geral.
2. Definir objetivos específicos e benefícios esperados.
3. Delimitar escopo incluído e excluído.
4. Identificar entregas e requisitos de alto nível.
5. Registrar restrições, premissas, riscos e dependências.
6. Identificar stakeholders, patrocinador e responsável propostos.
7. Definir indicadores de sucesso, marcos, recursos e investimento preliminares.
8. Consolidar pendências e decisões necessárias.

### Resultado obrigatório

[Termo de Abertura Preliminar](../modelos/termo-abertura-preliminar.md).

### Critério de saída

A proposta está delimitada o suficiente para que a análise de clientes, mercado e modelo de negócio possa confirmar, refutar ou ajustar suas bases.

### Portão humano 2

`Avançar para mercado e modelo de negócio`, `Investigar`, `Reformular` ou `Arquivar`.

## Rodada 3 — Mercado e modelo de negócio

### Objetivo

Avaliar para quem a iniciativa gera valor, como esse valor será entregue e se existe um modelo sustentável ou justificável para sua realização.

### Dinâmica

1. Diferenciar clientes, usuários, beneficiários e pagadores.
2. Identificar segmentos, necessidades, alternativas e concorrentes.
3. Formular proposta de valor, canais e relacionamento.
4. Avaliar receitas ou outras formas de geração de valor.
5. Identificar recursos, atividades, parceiros e estrutura de custos.
6. Classificar afirmações como fatos, estimativas ou hipóteses.
7. Definir pesquisas ou experimentos para as hipóteses críticas.
8. Reavaliar problema, objetivo, escopo, requisitos, restrições e resultados do TAP preliminar.
9. Consolidar recomendação e opiniões divergentes.

### Resultado obrigatório

[Canvas de Modelo de Negócio](../modelos/canvas-modelo-negocio.md), incluindo análise de compatibilidade com o TAP preliminar e parecer final.

### Decisão humana final

`Promover a projeto`, `Realizar experimento`, `Reformular` ou `Arquivar`.

## Promoção ao Escritório de Projetos

Quando houver decisão humana explícita de promoção:

1. criar `portfolios/<portfolio>/projetos/<projeto>/`;
2. mover o dossiê da ideia para `portfolios/<portfolio>/projetos/<projeto>/iniciacao/`;
3. criar os registros operacionais do projeto usando os modelos de projeto, decisões, tarefas e histórico;
4. registrar no projeto a decisão de promoção, o decisor, a data e as condições;
5. adicionar o projeto ao `portfolio.md` correspondente;
6. remover a iniciativa da relação de ideias ativas do Comitê.

O conteúdo não deve ser copiado e mantido como fonte oficial em dois lugares.

## Sessão de cada rodada

Cada sessão segue uma sequência curta:

1. **Contexto:** portfólio, ideia, rodada, objetivo e documentos consultados.
2. **Contribuições:** pareceres dos papéis convocados, distinguindo evidência de hipótese.
3. **Contestação:** o Auditor questiona premissas e os demais papéis respondem.
4. **Síntese:** o Orquestrador registra convergências, divergências, lacunas e recomendação.
5. **Documentação:** o Documentador atualiza somente o documento da rodada e suas referências.
6. **Portão:** o decisor humano escolhe o próximo estado.

## Após a promoção: validação de entrega de sprint

Esta atividade pertence à gestão operacional do Escritório de Projetos, não às rodadas de ideação. O Comitê pode ser reconvocado se uma mudança alterar substancialmente o problema, objetivo, proposta de valor ou modelo de negócio.

1. Identificar a linha de base aprovada da sprint e a revisão exata do repositório de desenvolvimento.
2. Relacionar cada item planejado aos requisitos e critérios de aceite correspondentes.
3. Inspecionar código, modelo de dados, migrações, testes, commits, pull requests e evidências de execução.
4. Classificar cada item como `Atendido`, `Parcial`, `Divergente`, `Não implementado` ou `Adicional`.
5. Avaliar impactos das diferenças em prazo, escopo, qualidade, recursos, riscos e resultado.
6. Corrigir defeitos dentro do escopo ou submeter mudanças relevantes à decisão humana.
7. Registrar a validação usando o [modelo de validação de sprint](../modelos/validacao-sprint.md), preservando referências verificáveis.

A revisão do código descreve o estado implementado, mas não substitui a aprovação funcional nem redefine a linha de base.

## Encerramento obrigatório de uma sessão

Toda sessão deve terminar em exatamente uma ou mais destas saídas:

1. decisão;
2. tarefa;
3. pendência;
4. nenhuma ação necessária.

Se não houver saída operacional, não criar documentação adicional.

## Modos de interação

### Consulta

O Comitê responde dúvidas, investiga alternativas ou apresenta sugestões. Não altera o estado da ideia nem registra decisão humana sem manifestação explícita.

### Atualização da ideia

Registra novas evidências, respostas, hipóteses invalidadas e decisões já aprovadas, preservando fonte e data.

### Retorno de iniciativa promovida

Quando um projeto ativo sofrer mudança substancial de problema, objetivo, público, proposta de valor ou modelo de negócio, o Escritório pode reconvocar o Comitê. O Comitê avalia impactos e recomenda ajustes; não altera autonomamente a linha de base do projeto.

## Após a promoção: controle do projeto

Cada projeto é acompanhado em seis dimensões:

| Dimensão | Pergunta de controle |
|---|---|
| Prazo | Estamos entregando no prazo previsto? |
| Escopo | O objetivo e os limites permanecem adequados e compreendidos? |
| Qualidade | A entrega atende ao padrão e aos critérios de aceite? |
| Recursos | A capacidade disponível viabiliza o plano? |
| Impedimentos & Riscos | Há algo bloqueando ou ameaçando o avanço? |
| Resultado | A entrega continua resolvendo o problema e gerando o benefício esperado? |

Use `🟢 Controlado`, `🟡 Atenção` ou `🔴 Intervenção` em cada dimensão. Um impedimento sem próxima ação definida deve ser tratado como risco ativo.

## Memória

- **Memória da ideia:** dossiê em `conselho/ideias/<portfolio>/<ideia>/` enquanto estiver no Comitê.
- **Memória do projeto:** registros em sua própria pasta.
- **Memória do portfólio:** padrões e aprendizados reutilizáveis, a serem consolidados quando houver projetos suficientes.
- Conversas e modelos de IA não são fonte oficial. Eles consultam e interpretam a memória registrada.
