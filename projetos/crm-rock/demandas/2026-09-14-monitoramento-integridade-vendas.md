# Demanda — Melhorar o monitoramento da integridade das vendas no CRM

**Data da solicitação:** 14/09/2026  
**Solicitante:** Fabrício Medeiros  
**Linha de trabalho:** Monitoramento da integração de vendas  
**Situação:** Aguardando refinamento  
**Prioridade:** Alta, a validar na triagem  
**Dono funcional:** A confirmar

## Contexto e necessidade

O CRM Rock, antiga BNEX, está implantado desde 2021. As vendas são integradas ao CRM e há uma frente em andamento para implantar um novo integrador via API mantido pela Rock, substituindo a integração desenvolvida pela Consinco.

O e-mail atual lista “lojas com poucas vendas” apenas com CNPJ e nome. Sem o período, os valores e a regra usada, o destinatário não consegue determinar se houve uma venda realmente baixa ou se parte das vendas deixou de ser registrada no CRM.

## Objetivo correto do alerta

Detectar possíveis falhas, atrasos ou sub-registros na integração de vendas de cada loja no CRM, permitindo investigação e correção tempestivas.

O alerta não deve, por si só, classificar o desempenho comercial da loja.

## Informações mínimas propostas

- data de venda apurada e data/hora de geração do alerta;
- horário da última carga ou sincronização recebida pelo CRM;
- CNPJ formatado, nome da loja e associado, quando disponível;
- valor registrado no CRM na data apurada;
- valor de referência e origem dessa referência;
- diferença em reais e percentual;
- critério exato que incluiu a loja no alerta;
- situação da integração, quando identificável: completa, parcial, atrasada, sem carga ou indeterminada;
- quantidade de lojas analisadas e quantidade alertada;
- orientação e contato responsável pela investigação.

## Definição necessária da referência

A referência ainda não está definida. No refinamento, avaliar qual evidência permite confirmar completude, preferencialmente nesta ordem:

1. total de controle fornecido pelo ERP/integrador para a mesma loja e data;
2. confirmação técnica de lote, arquivo ou chamada de API processada integralmente;
3. média histórica comparável, somente como indicador de anomalia quando não houver total de controle.

Uma média histórica isolada não comprova falha de integração, pois a loja pode ter vendido menos por razões legítimas.

## Critérios de aceite iniciais

1. O e-mail identifica claramente a data das vendas analisadas e a distingue da data de geração.
2. A regra e a fonte de comparação são apresentadas em linguagem clara.
3. Cada loja mostra valor recebido no CRM, valor de referência, diferença absoluta e variação percentual.
4. O alerta diferencia, quando houver evidência técnica, ausência de carga, carga parcial e venda baixa sem falha comprovada.
5. Dados ainda em processamento são sinalizados como provisórios e não como falha definitiva.
6. Média zero, ausência de histórico ou falta de referência não provocam erro e são exibidas como situação indeterminada.
7. A solução registra evidência suficiente para investigar o evento, como lote, horário da carga ou identificador da integração, sem expor dado sensível.
8. O funcionamento é validado nos integradores atual e novo durante a transição, se ambos permanecerem ativos.
9. O dono funcional aprova uma amostra do alerta antes da liberação ampla.

## Pendências para refinamento

- localizar quem gera e envia o e-mail atual;
- documentar o critério atual e sua origem;
- mapear o fluxo Consinco → CRM e o futuro fluxo pela API da Rock;
- confirmar se existe total de controle por loja e dia no ERP ou integrador;
- definir horário limite da carga, tolerância para atraso e política de reprocessamento;
- definir tratamento de lojas fechadas, feriados, inaugurações e operação parcial;
- confirmar destinatários, frequência, responsáveis pela investigação e escalonamento;
- decidir se o monitoramento fará parte do novo integrador ou de um controle independente.

## Evidência recebida

Captura de e-mail de 14/09/2026 com lista textual no formato `Lojas com poucas Vendas: <CNPJ> <LOJA>` e uma data técnica ao final. A captura comprova o formato atual, mas não revela a regra, a fonte dos dados ou a rotina de envio.
