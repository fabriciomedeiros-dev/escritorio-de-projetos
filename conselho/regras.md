# Regras de Governança

## Fonte oficial

1. Enquanto a iniciativa for apenas uma ideia, os arquivos em `conselho/ideias/<portfolio>/<ideia>/` são sua memória oficial.
2. Depois da promoção, os arquivos do projeto em `portfolios/<portfolio>/projetos/<projeto>/` tornam-se a memória oficial.
3. Uma conversa, sugestão ou hipótese não se torna fato somente por ter sido mencionada por uma IA.
4. Registros devem conter data, contexto suficiente e, quando aplicável, a origem/evidência.

### Fronteira entre ideia e projeto

- Uma ideia em avaliação não integra o portfólio, não recebe saúde de projeto e não deve aparecer em relatórios de projetos ativos.
- A existência de um TAP preliminar ou Canvas não representa aprovação, autorização financeira ou compromisso de execução.
- Somente uma decisão humana explícita de `Promover a projeto` autoriza a criação da pasta operacional no portfólio.
- Na promoção, o dossiê deve ser movido para `portfolios/<portfolio>/projetos/<projeto>/iniciacao/`. Não mantenha cópias canônicas concorrentes no Comitê e no projeto.
- A promoção deve gerar os registros operacionais mínimos do projeto e preservar a referência à decisão humana.
- Iniciativas em experimento permanecem no Comitê até nova decisão. Iniciativas arquivadas permanecem identificadas como tal e não entram no portfólio.

### Isolamento entre portfólios

- Cada empresa ou domínio pessoal possui uma pasta própria em `portfolios/<identificador>/`.
- Todo projeto deve declarar seu portfólio e usar um identificador com prefixo exclusivo daquele portfólio.
- Relatórios, comunicações, publicações e automações devem receber o portfólio explicitamente e consultar somente sua pasta.
- É proibido consolidar informações de portfólios distintos por padrão. Uma consolidação excepcional exige solicitação e aprovação humanas explícitas.
- Destinatários, canais, permissões e configurações de comunicação devem ser definidos separadamente por portfólio.

### Autoridade entre repositórios

- O Escritório de Projetos é a fonte canônica das decisões gerenciais, incluindo objetivo, escopo, prioridade, orçamento, riscos relevantes, governança, marcos e autorizações executivas.
- O repositório de documentação indicado pela iniciativa é a fonte do comportamento esperado, dos requisitos, das regras e dos critérios de aceite.
- O repositório de desenvolvimento é a fonte do código efetivamente implementado, stack, modelo de dados, migrações, testes e evidências técnicas.
- Referências entre os repositórios podem ser usadas para evitar duplicação, mas cada decisão deve ter uma única fonte canônica claramente identificada.
- Quando uma decisão técnica ou funcional afetar a linha de base gerencial, seu impacto e a aprovação correspondente devem ser registrados no Escritório de Projetos.

### Conformidade entre planejamento e entrega

- Uma sprint deve possuir linha de base identificável, com itens, requisitos e critérios de aceite aprovados antes da validação da entrega.
- Cada item entregue deve apontar para evidências verificáveis no repositório de desenvolvimento, como commit, pull request, teste, migração ou demonstração.
- A validação deve classificar cada item como `Atendido`, `Parcial`, `Divergente`, `Não implementado` ou `Adicional`.
- Uma implementação adicional ou divergente não altera automaticamente requisito, escopo ou decisão. Seu impacto deve ser analisado e submetido à validação humana quando relevante.
- A ausência de instruções suficientes para executar localmente o código deve ser registrada como lacuna da camada de desenvolvimento.

### Relações entre projetos

- Um projeto pode consumir serviços compartilhados de outro sem se tornar subordinado a ele na gestão.
- O projeto consumidor mantém objetivo, escopo, cronograma, aceite e decisões próprios.
- O projeto provedor responde pela capacidade compartilhada, sua segurança, compatibilidade e disponibilidade.
- A dependência deve indicar donos nos dois projetos, situação, critério de aceite e risco de indisponibilidade.
- Mudanças em serviço compartilhado com impacto em consumidores exigem análise conjunta antes da liberação.

## Classificação da informação

Sempre diferenciar:

- **Fato:** informação confirmada por evidência ou responsável.
- **Hipótese:** informação ainda não comprovada.
- **Estimativa:** valor aproximado produzido por método declarado, ainda não confirmado.
- **Recomendação:** orientação do Comitê baseada nas evidências e hipóteses registradas.
- **Decisão:** escolha aprovada pelo decisor humano.
- **Ação:** trabalho a ser executado.

## Autonomia do Comitê

O Comitê pode organizar análises, pesquisar evidências, identificar lacunas, formular alternativas, recomendar experimentos e estruturar a documentação das três rodadas.

Não pode aprovar autonomamente a criação ou promoção de projeto, mudança estratégica, prioridade relevante, orçamento, risco relevante, objetivo ou alteração irreversível.

## Alterações após a promoção

1. Registrar a linha de base antes de substituir informações relevantes.
2. Para mudanças com impacto, documentar motivo, impacto, alternativas e aprovação.
3. Atualizar o estado atual depois de uma decisão ou fato confirmado.
4. Registrar no histórico somente eventos que expliquem a evolução do projeto.

## Qualidade dos registros

- Não duplicar o mesmo fato em vários arquivos sem necessidade.
- Não usar campos fictícios para aparentar completude; utilizar `Não definido` ou `A confirmar`.
- Não transformar `projeto.md` em diário: ele representa o estado atual.
- Decisões completas ficam em `decisoes.md`; tarefas em `tarefas.md`; evolução relevante em `historico.md`.

**Navegação:** [Conselho](README.md) · [Papéis](papeis.md) · [Protocolo](protocolo.md) · [Início](../README.md)
