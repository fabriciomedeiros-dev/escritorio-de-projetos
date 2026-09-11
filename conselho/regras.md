# Regras de Governança

## Fonte oficial

1. Os arquivos Markdown do projeto são a memória oficial.
2. Uma conversa, sugestão ou hipótese não se torna fato somente por ter sido mencionada por uma IA.
3. Registros devem conter data, contexto suficiente e, quando aplicável, a origem/evidência.

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

## Classificação da informação

Sempre diferenciar:

- **Fato:** informação confirmada por evidência ou responsável.
- **Hipótese:** informação ainda não comprovada.
- **Recomendação:** orientação do Conselho.
- **Decisão:** escolha aprovada pelo decisor humano.
- **Ação:** trabalho a ser executado.

## Autonomia do Conselho

O Conselho pode organizar análises, identificar lacunas, propor tarefas, estruturar documentação e acompanhar o plano.

Não pode aprovar autonomamente mudança estratégica, prioridade relevante, orçamento, risco relevante, objetivo ou alteração irreversível.

## Alterações de projeto

1. Registrar a linha de base antes de substituir informações relevantes.
2. Para mudanças com impacto, documentar motivo, impacto, alternativas e aprovação.
3. Atualizar o estado atual depois de uma decisão ou fato confirmado.
4. Registrar no histórico somente eventos que expliquem a evolução do projeto.

## Qualidade dos registros

- Não duplicar o mesmo fato em vários arquivos sem necessidade.
- Não usar campos fictícios para aparentar completude; utilizar `Não definido` ou `A confirmar`.
- Não transformar `projeto.md` em diário: ele representa o estado atual.
- Decisões completas ficam em `decisoes.md`; tarefas em `tarefas.md`; evolução relevante em `historico.md`.
