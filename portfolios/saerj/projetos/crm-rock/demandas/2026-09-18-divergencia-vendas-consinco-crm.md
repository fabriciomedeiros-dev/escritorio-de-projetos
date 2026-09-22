# Demanda — Divergência de vendas na integração Consinco × CRM

**Data do registro:** 18/09/2026  
**Projeto:** CRM Rock (antiga BNEX)  
**Linha de trabalho:** Novo integrador de vendas via API da Rock  
**Chamado:** `202578`  
**Situação:** Em tratamento — reenvio de vendas agendado para configuração
**Prioridade:** Alta, a validar na triagem  
**Responsável pelo acompanhamento:** A confirmar  
**Período dos dados analisados:** A confirmar

## Contexto

Foi identificada divergência entre as vendas capturadas pela nova integração Consinco × CRM e os dados de referência do data lake. A apuração inicial compara quantidade de vendas e faturamento para três lojas do Cruzeiro do Sul.

O chamado `202578` foi aberto no CRM para investigação e acompanhamento da ocorrência.

## Apuração inicial recebida

| Loja | Quantidade no data lake (GCP) | Quantidade no CRM/Rock | Diferença | Diferença % | Faturamento no data lake (GCP) | Faturamento no CRM/Rock | Diferença de faturamento | Diferença % |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Cruzeiro do Sul — Eden | 30.249 | 20.786 | 9.463 | 31% | R$ 1.547.194,00 | R$ 1.203.382,82 | R$ 343.811,18 | 22% |
| Cruzeiro do Sul — Guadalupe | 28.317 | 21.462 | 6.855 | 24% | R$ 1.768.663,00 | R$ 1.475.971,75 | R$ 292.691,25 | 17% |
| Cruzeiro do Sul — São Matheus | 29.408 | 20.459 | 8.949 | 30% | R$ 1.864.001,00 | R$ 1.455.114,87 | R$ 408.886,13 | 22% |

### Consolidado calculado a partir da apuração

- quantidade no data lake: **87.974**;
- quantidade no CRM/Rock: **62.707**;
- diferença de quantidade: **25.267**, equivalente a aproximadamente **28,7%** do total do data lake;
- faturamento no data lake: **R$ 5.179.858,00**;
- faturamento no CRM/Rock: **R$ 4.134.469,44**;
- diferença de faturamento: **R$ 1.045.388,56**, equivalente a aproximadamente **20,2%** do total do data lake.

Os totais consolidados acima são derivados aritmeticamente dos valores da imagem recebida e devem ser confirmados junto à fonte antes de uso como fechamento oficial.

## Evidência

- imagem recebida: `AnaliseCruzeiro.jpeg`;
- origem informada para os valores de referência: data lake;
- chamado aberto no CRM: `202578`.

A imagem comprova os valores usados na apuração inicial, mas não informa o período analisado, as consultas utilizadas, o horário das cargas nem os identificadores dos lotes processados.

## Impacto observado

Há sub-registro relevante de quantidade e faturamento no CRM/Rock em comparação com o data lake nas três lojas analisadas. O maior desvio percentual de quantidade aparece em Eden (31%); em faturamento, Eden e São Matheus apresentam 22%.

A causa ainda não está confirmada. A divergência não deve ser atribuída à integração, ao ERP, ao CRM ou ao data lake sem análise técnica e conciliação das regras de extração.

## Ações de acompanhamento

1. Confirmar o período e o horário de corte da apuração.
2. Validar se data lake e CRM usam as mesmas regras de negócio, filtros, cancelamentos, devoluções e datas de competência.
3. Identificar os lotes, arquivos ou chamadas de API relacionados às três lojas.
4. Verificar falhas, atrasos, rejeições, duplicidades e reprocessamentos na integração.
5. Conciliar uma amostra transacional entre Consinco, data lake e CRM/Rock.
6. Registrar no chamado `202578` a causa, a correção aplicada e a evidência da revalidação.
7. Avaliar se o monitoramento previsto na tarefa `CRM-005` detectaria automaticamente esta ocorrência.

## Atualização de 22/09/2026

Foi agendada para 22/09/2026, às 15h30, reunião com a equipe do CRM/Rock e Cloves, da TI do Cruzeiro, para configurar o PDV para o reenvio das vendas. Na mesma sessão está prevista a alteração da URL de homologação para produção.

O agendamento representa o início da ação corretiva, mas não encerra a apuração. Ainda será necessário confirmar quais lojas e períodos serão reprocessados, validar o resultado no CRM e realizar nova conciliação com a fonte de referência.

## Condição de encerramento

A demanda poderá ser encerrada quando:

- a causa da divergência estiver identificada e registrada;
- o período afetado e as lojas impactadas estiverem confirmados;
- as vendas faltantes tiverem sido corrigidas ou houver justificativa formal para as diferenças;
- uma nova conciliação entre data lake e CRM/Rock demonstrar o resultado esperado;
- o chamado `202578` contiver a solução e as evidências de validação.

## Informações pendentes

- período exato da apuração;
- solicitante e responsável técnico pelo chamado;
- prazo ou nível de serviço;
- causa raiz;
- demais lojas e períodos potencialmente afetados;
- evidências técnicas da integração e retorno do fornecedor;
- critério de tolerância aceitável para a conciliação.
