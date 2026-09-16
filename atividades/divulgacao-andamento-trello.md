# Divulgação do andamento dos projetos no Trello

**Início da prática:** 16/09/2026  
**Responsável pela governança:** Escritório de Projetos  
**Situação:** Diretriz registrada; configuração operacional a confirmar

## Objetivo

Usar o Trello como painel simples de divulgação do andamento dos projetos, permitindo que os públicos interessados consultem situação, avanços, próximos passos e pontos de atenção sem substituir os registros oficiais do Escritório de Projetos.

## Papel de cada ferramenta

- O repositório do Escritório de Projetos continua sendo a fonte canônica de linha de base, status, decisões, tarefas, riscos, marcos e histórico.
- O Trello é uma camada de comunicação e visibilidade. Seus cartões resumem informações já registradas e validadas no Escritório.
- Discussões, comentários ou alterações feitas somente no Trello não constituem decisão aprovada nem alteram a linha de base do projeto.
- Quando uma informação relevante surgir no Trello, ela deve ser validada e registrada no arquivo canônico correspondente antes de ser tratada como oficial.

## Organização do quadro

Cada projeto será representado por um cartão no quadro de acompanhamento do portfólio. As listas indicarão a situação gerencial do projeto:

1. **Não iniciado** — projeto aprovado ou em preparação, sem execução iniciada;
2. **Em andamento** — execução ativa e dentro do acompanhamento regular;
3. **Atenção** — existe desvio, risco, impedimento ou decisão pendente que requer acompanhamento;
4. **Concluído** — objetivo ou entrega encerrada e fechamento registrado;
5. **Suspenso** — execução interrompida por decisão registrada.

A mudança de lista deve refletir o estado oficial do projeto no Escritório. O quadro, os membros e as permissões de acesso serão definidos pelo responsável pela governança.

## Conteúdo mínimo de cada cartão

- nome do projeto;
- objetivo resumido;
- responsável pelo projeto;
- situação atual e data de referência;
- fase ou marco atual;
- principais avanços desde a atualização anterior;
- próximos passos;
- riscos, impedimentos ou decisões requeridas;
- link para a página ou pasta canônica do projeto no Escritório, quando o acesso permitir;
- data da próxima atualização.

O cartão não deve conter credenciais, dados pessoais desnecessários, informações comerciais restritas nem conteúdo técnico sensível. Quando uma informação não puder ser divulgada, registrar apenas a indicação apropriada, como `Informação restrita — consultar o responsável`.

## Fluxo de atualização

1. O responsável consulta `projeto.md`, `tarefas.md`, `decisoes.md`, `historico.md` e as evidências aplicáveis.
2. Confere fatos, data de referência, saúde do projeto e mudanças desde a última publicação.
3. Atualiza primeiro os registros canônicos do Escritório, quando necessário.
4. Resume no cartão do Trello apenas informações confirmadas e adequadas ao público do quadro.
5. Registra no cartão a data da atualização e a próxima revisão prevista.
6. Em caso de risco relevante, desvio de marco ou decisão requerida, move o cartão para **Atenção** e comunica o responsável, sem aguardar o ciclo regular.
7. Após decisão ou resolução, atualiza o registro canônico e então ajusta o cartão e sua lista.

## Frequência e responsabilidades

| Atividade | Responsável | Frequência / gatilho | Evidência |
|---|---|---|---|
| Preparar e publicar o resumo do projeto | Responsável pelo projeto | Frequência regular a confirmar | Data da última atualização no cartão |
| Verificar coerência entre Trello e Escritório | Escritório de Projetos | No ciclo de atualização e nas revisões de portfólio | Arquivos do projeto e cartão correspondente |
| Publicar alerta extraordinário | Responsável pelo projeto | Risco relevante, desvio de marco, impedimento ou decisão requerida | Cartão em **Atenção** e comunicação ao responsável |
| Encerrar ou suspender a divulgação | Escritório de Projetos, após decisão aplicável | Conclusão ou suspensão confirmada | Decisão/histórico e mudança de lista |

## Padrão sugerido para a descrição do cartão

```text
Objetivo:
[Resumo do objetivo]

Situação em DD/MM/AAAA:
[Resumo do andamento]

Avanços:
- [Avanço confirmado]

Próximos passos:
- [Ação, responsável e prazo quando conhecidos]

Pontos de atenção / decisões requeridas:
- [Item ou "Nenhum no período"]

Fonte oficial:
[Referência do projeto no Escritório]

Próxima atualização:
[DD/MM/AAAA ou A confirmar]
```

## Pendências para implantação

- definir o nome e o endereço do quadro;
- definir quais públicos terão acesso e seus níveis de permissão;
- confirmar a frequência regular de atualização;
- definir o responsável operacional de cada cartão;
- criar os cartões iniciais com base no portfólio vigente;
- avaliar, após o primeiro ciclo, se etiquetas por saúde, área ou prioridade agregam valor sem duplicar as listas.

