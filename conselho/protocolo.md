# Protocolo Operacional

**Navegação:** [Conselho](README.md) · [Papéis](papeis.md) · [Regras](regras.md) · [Modelos](../modelos/README.md)

## Ciclo de trabalho

1. **Entrada** — receber uma demanda, atualização, dúvida ou projeto existente.
2. **Diagnóstico** — recuperar o contexto do projeto, identificar fatos, lacunas e estado atual.
3. **Discussão** — analisar sob as perspectivas de negócio, técnica e crítica, envolvendo apenas os papéis necessários.
4. **Recomendação** — consolidar opções, impactos e orientação do Conselho.
5. **Decisão** — obter validação humana quando a regra exigir.
6. **Plano** — transformar a decisão em tarefas objetivas, com responsável e prazo quando conhecidos.
7. **Execução** — a equipe realiza as tarefas e informa evidências.
8. **Acompanhamento** — monitorar prazo, escopo, qualidade, recursos, impedimentos/riscos e resultado.
9. **Registro** — atualizar somente os arquivos afetados: estado, decisão, tarefa ou histórico.

## Validação de entrega de sprint

1. Identificar a linha de base aprovada da sprint e a revisão exata do repositório de desenvolvimento.
2. Relacionar cada item planejado aos requisitos e critérios de aceite correspondentes.
3. Inspecionar código, modelo de dados, migrações, testes, commits, pull requests e evidências de execução.
4. Classificar cada item como `Atendido`, `Parcial`, `Divergente`, `Não implementado` ou `Adicional`.
5. Avaliar impactos das diferenças em prazo, escopo, qualidade, recursos, riscos e resultado.
6. Corrigir defeitos dentro do escopo ou submeter mudanças relevantes à decisão humana.
7. Registrar a validação usando o [modelo de validação de sprint](../modelos/validacao-sprint.md), preservando referências verificáveis.

A revisão do código descreve o estado implementado, mas não substitui a aprovação funcional nem redefine a linha de base.

## Encerramento obrigatório de uma discussão

Toda discussão deve terminar em exatamente uma ou mais destas saídas:

1. decisão;
2. tarefa;
3. pendência;
4. nenhuma ação necessária.

Se não houver saída operacional, não criar documentação adicional.

## Modos de interação

### Consulta

O Conselho responde dúvidas, investiga alternativas ou apresenta sugestões. Não modifica o registro do projeto sem solicitação explícita.

### Atualização operacional

Registra fatos confirmados, andamento de tarefas, impedimentos e alterações já aprovadas, preservando evidências e data.

### Solicitação de mudança

Avalia impacto em escopo, prazo, qualidade, recursos, riscos e resultado. Quando aplicável, apresenta opções e aguarda a decisão humana antes de alterar a linha de base ou o plano.

## Controle do projeto

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

- **Memória do projeto:** registros em sua própria pasta.
- **Memória do portfólio:** padrões e aprendizados reutilizáveis, a serem consolidados quando houver projetos suficientes.
- Conversas e modelos de IA não são fonte oficial. Eles consultam e interpretam a memória registrada.
