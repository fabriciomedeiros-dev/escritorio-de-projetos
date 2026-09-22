# Projeto: CRM Rock (antiga BNEX)

**Navegação:** [Portfólio](../../portfolio.md) · [Decisões](decisoes.md) · [Tarefas](tarefas.md) · [Histórico](historico.md) · [Reunião — integração no Torre](reunioes/2026-09-21-configuracao-integracao-torre.md) · [Reunião — reenvio e URL de produção](reunioes/2026-09-22-reenvio-vendas-url-producao.md) · [Demanda de monitoramento](demandas/2026-09-14-monitoramento-integridade-vendas.md) · [Divergência de vendas — chamado 202578](demandas/2026-09-18-divergencia-vendas-consinco-crm.md) · [Referências técnicas](referencias/README.md)

## 1. Identificação

**ID:** SAERJ-CRM-ROCK

**Portfólio:** saerj

**Visibilidade:** restrita-saerj

**Status geral:** 🟡 Atenção  
**Responsável:** A confirmar  
**Sponsor:** A confirmar  
**Fase:** Operação e evolução contínua  
**Implantação original:** 2021  
**Previsão de conclusão:** Evolução contínua  
**Última atualização:** 22/09/2026

### Fontes canônicas relacionadas

**Fornecedor:** Rock (antiga BNEX)  
**Documentação funcional e técnica:** [Documentação TOTVS da integração PDV](referencias/tecnicas/totvs-documentacao-integracao-pdv.pdf) e [resumo com checklist](referencias/tecnicas/resumo-integracao-pdv.md); demais documentos a confirmar  
**Contratos e análises:** A confirmar

---

## 2. Objetivo

Manter e evoluir o CRM e seu aplicativo, assegurando continuidade operacional, integridade dos dados de vendas, modernização da integração e viabilidade técnica e contratual da plataforma.

### Fato confirmado

O CRM está implantado desde 2021. A integração atual de vendas foi desenvolvida pela Consinco, fornecedora do ERP, e há iniciativas de evolução com participação da Rock.

### Resultado esperado

CRM operando com integração de vendas confiável e monitorada, infraestrutura sustentável e novas capacidades priorizadas e implantadas conforme validação de negócio.

---

## 3. Linhas de trabalho

| Frente | Situação atual | Resultado pretendido | Próximo ponto de controle |
|---|---|---|---|
| Novo integrador de vendas via API da Rock | Um PDV foi configurado com sucesso no Torre e está identificando e enviando vendas ao CRM. O teste de preço 2 está pendente do levantamento da regra de incentivo do Cruzeiro. Para 22/09/2026 às 15h30, foi agendada reunião com CRM/Rock e Cloves, da TI do Cruzeiro, para configurar o reenvio de vendas e alterar a URL para produção. | Substituir a integração desenvolvida pela Consinco pela integração mantida pela Rock, com integridade comprovada dos dados | Executar e validar o reenvio das vendas e a troca da URL; levantar a regra de incentivo do Cruzeiro, orientar o Torre e testar o preço 2 |
| Migração do servidor do CRM para SaaS da Rock | Em análise, elaboração de contrato e avaliação de viabilidade técnica | Definir se a migração é técnica, operacional e financeiramente viável | Concluir análise comparativa, riscos, contrato e recomendação para decisão |
| Carteira digital no aplicativo do CRM | Implantação prevista; estágio a confirmar | Disponibilizar carteira digital no aplicativo | Definir requisitos, dependências, responsável, prazo e critérios de aceite |
| Monitoramento da integração de vendas | Melhoria solicitada em 14/09/2026 | Identificar lojas cujas vendas não foram registradas corretamente no CRM | Confirmar regra atual, fonte do alerta e conteúdo do novo e-mail |

## 4. Linha de base e escopo

### Incluído

- operação e evolução do CRM Rock;
- integração de vendas com o ERP e a nova API da Rock;
- análise da migração da infraestrutura para SaaS;
- carteira digital no aplicativo;
- controles de completude e integridade das vendas recebidas pelo CRM.

### Não incluído

- uso do alerta para avaliação de desempenho comercial das lojas;
- alterações nos sistemas do ERP ou da Rock sem definição formal de responsabilidade;
- demais evoluções do CRM ainda não registradas.

### Grau de confiança

| Aspecto | Nível | Observação |
|---|---|---|
| Objetivo | Médio | Contexto e frentes foram informados; benefícios e indicadores ainda precisam ser consolidados. |
| Requisitos | Baixo | Apenas a demanda de monitoramento possui detalhamento inicial. |
| Solução | Baixo | Arquitetura, contratos, ambientes, integrações e responsáveis ainda não foram documentados. |

### Pontos ainda desconhecidos

- sponsor, gerente do projeto, donos funcionais e responsáveis técnicos;
- situação, cronograma, orçamento e prioridade relativa de cada frente;
- arquitetura atual e futura da integração de vendas;
- origem, consulta e critério do alerta existente;
- indicadores operacionais e níveis de serviço acordados com Rock e Consinco.

---

## 5. Estado atual

| Dimensão | Status | Resumo objetivo | Próxima ação |
|---|---|---|---|
| Prazo | 🟡 Atenção | Não há cronograma consolidado para as quatro frentes. | Levantar marcos e prazos por frente. |
| Escopo | 🟡 Atenção | Frentes principais identificadas, ainda sem requisitos e limites completos. | Refinar e priorizar cada frente. |
| Qualidade | 🟡 Atenção | O PDV configurado no Torre já envia vendas ao CRM, mas o preço 2 não foi testado. O chamado `202578` continua exigindo reenvio e reconciliação das vendas afetadas. | Levantar a regra de incentivo do Cruzeiro, testar o preço 2, executar o reenvio e reconciliar os dados. |
| Recursos | 🟡 Atenção | Responsáveis da Rede, Rock e Consinco não estão consolidados. | Montar matriz de responsabilidades. |
| Impedimentos & Riscos | 🟡 Atenção | A URL de produção ainda não foi validada, o reenvio das vendas está pendente e o cenário de preço 2 depende da regra de incentivo usada pelo Cruzeiro. | Tratar URL e reenvio na reunião de 22/09 às 15h30 e concluir o levantamento necessário ao teste do preço 2. |
| Resultado | 🟡 Atenção | O CRM está implantado, mas não há indicadores consolidados das evoluções. | Definir indicadores por frente. |

## 6. Próximo marco

**Marco:** Configurar o reenvio de vendas e alterar a integração para a URL de produção

**Data:** 22/09/2026, às 15h30

**Condição de conclusão:** PDV configurado para reenvio, vendas reprocessadas ou plano formalizado, URL de produção aplicada e transação validada no CRM.

## 7. Observação do Escritório de Projetos

O alerta de “poucas vendas” deve ser tratado como controle de completude da integração: seu objetivo é detectar possível ausência ou sub-registro de vendas no CRM. A regra precisa diferenciar uma falha de integração de um dia comercialmente fraco para evitar falsos alertas e decisões incorretas.
