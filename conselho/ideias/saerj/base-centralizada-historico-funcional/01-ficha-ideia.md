# Ficha de Ideia — Base Centralizada de Histórico Funcional

**ID da ideia:** SAERJ-IDEIA-001

**Portfólio pretendido:** saerj

**Estado:** Backlog — em descoberta

**Proponente:** A confirmar

**Data de entrada:** 22/09/2026

**Última atualização:** 24/09/2026

**Divulgação no Trello:** [SAERJ-IDEIA-001 — Base Centralizada de Histórico Funcional](https://trello.com/c/f3leMAGM)

**Resumo executivo:** [Documento Word](artefatos/resumo-executivo-base-centralizada-historico-funcional.docx)

> Esta iniciativa está no Comitê de Ideação. Não é projeto ativo, não possui autorização de execução e não integra a visão executiva do portfólio SAERJ.

## 1. Ideia original

Criar uma base centralizada de funcionários que permita consultar uma pessoa pelo CPF e localizar dados de sua relação de trabalho com os associados da SAERJ, incluindo datas de admissão e desligamento, motivo do desligamento e registros funcionais relevantes, como advertências.

A ideia original também considera identificar a existência de ações judiciais envolvendo o trabalhador e associados. Esse uso não está aprovado como requisito: ele apresenta risco elevado de privacidade e discriminação e deverá passar por avaliação jurídica, trabalhista e de proteção de dados antes de qualquer coleta, compartilhamento, consulta ou uso decisório.

O termo “mini dossiê” descreve informalmente a visão apresentada, mas não será adotado como conceito do produto. A direção recomendada é uma base de histórico funcional com finalidade delimitada, dados estritamente necessários, governança, rastreabilidade e direitos do titular.

## 2. Problema percebido

**Problema:** informações sobre vínculos e ocorrências funcionais estão potencialmente distribuídas entre associados e diferentes sistemas de RH, o que dificulta consultas legítimas, consistentes e auditáveis.

**Público afetado:** áreas de RH, jurídico, compliance e gestores autorizados dos associados; trabalhadores e ex-trabalhadores são os titulares diretamente impactados pelo tratamento.

**Situação atual:** A confirmar. É necessário mapear como cada associado registra e consulta admissões, desligamentos, advertências e demandas judiciais, quais sistemas utiliza e se existe compartilhamento atual entre associados.

**Impacto:** hipótese de retrabalho, demora na obtenção de informações, divergências cadastrais e baixa rastreabilidade. Em contrapartida, uma centralização mal desenhada pode ampliar exposição, uso discriminatório, inexatidão e vazamento de dados pessoais.

**Evidências disponíveis:** relato inicial do solicitante. Não foram apresentados inventário de sistemas, volumes, casos de uso documentados, base legal, fluxo atual, parecer jurídico ou indicadores de tempo e qualidade.

## 3. Objetivo inicial

**Objetivo:** avaliar a viabilidade de oferecer uma consulta centralizada, segura e auditável ao histórico funcional estritamente necessário para finalidades legítimas e previamente aprovadas, integrando dados autorizados dos sistemas de RH dos associados.

**Resultado esperado:** usuários autorizados encontram informações confiáveis sobre vínculos de trabalho sem depender de consultas manuais dispersas, enquanto o tratamento respeita finalidade, necessidade, transparência, qualidade dos dados, segurança, prevenção, não discriminação e responsabilização.

**Indicadores possíveis:**

- tempo médio de resposta a uma consulta autorizada;
- percentual de associados e sistemas integrados;
- percentual de registros conciliados e atualizados;
- percentual de acessos com justificativa e trilha de auditoria;
- quantidade de divergências, contestações e correções de titulares;
- incidentes de segurança ou acesso indevido;
- usos bloqueados por ausência de finalidade, permissão ou base legal;
- redução do esforço manual do RH em consultas legítimas.

## 4. Linhas de possibilidade

| Possibilidade | Como funcionaria | Benefício potencial | Limitação / risco | Evidência necessária |
|---|---|---|---|---|
| Não agir | Manter registros apenas nos sistemas de cada associado | Evita novo compartilhamento e concentração de dados | Mantém fragmentação e retrabalho, se confirmados | Medir frequência, tempo e custo das consultas atuais |
| Melhorar o processo existente | Padronizar um protocolo de consulta e resposta entre RHs, sem criar uma base única | Menor exposição e implantação mais simples | Resposta mais lenta e dependente de pessoas | Mapear volume e urgência dos casos de uso |
| Consulta federada | A SAERJ orquestra consultas autorizadas, mas o dado permanece na origem | Reduz cópias e favorece atualização | Maior complexidade e dependência de disponibilidade das origens | Avaliar APIs, latência, identidade e capacidade dos associados |
| Base centralizada mínima | Replicar somente vínculos e atributos aprovados, com segregação e auditoria | Consulta rápida e padronizada | Concentra risco e exige governança rigorosa | Inventário de dados, RIPD, base legal, segurança e retenção |
| Prova de conceito | Integrar dados sintéticos ou anonimizados de poucos associados | Testa compatibilidade sem expor dados reais | Não comprova toda a operação e governança | Cenários representativos e critérios de sucesso |

## 5. Requisitos preliminares

- Consultar pessoa por CPF somente por usuário autorizado, com justificativa e finalidade registrada.
- Não exibir CPF integral fora de fluxos que realmente o exijam; aplicar mascaramento e proteção criptográfica conforme desenho de segurança.
- Consolidar vínculos por associado, com datas de admissão e desligamento, origem, data de atualização e grau de confiabilidade.
- Tratar motivo de desligamento e advertências como informações de acesso restrito, com vocabulário padronizado, evidência de origem e mecanismo de contestação/correção.
- Separar fatos documentados de alegações, observações e classificações internas.
- Preservar histórico de alterações, consultas, exportações e decisões de acesso.
- Integrar inicialmente por APIs, arquivos ou conectores aprovados para Alterdata e TOTVS RM, sem pressupor que todas as versões dos produtos ofereçam a mesma interface.
- Desenvolver a capacidade sob governança da SAERJ; a aquisição ou contratação de uma solução pronta não faz parte das possibilidades desta iniciativa.
- Definir reconciliação de duplicidades, conflito entre fontes, atualização, indisponibilidade e desligamento de um associado.
- Implementar segregação entre associados e perfis de menor privilégio.
- Proibir pontuação, recomendação automática de contratação ou desligamento e qualquer decisão exclusivamente automatizada no escopo inicial.
- Prever atendimento aos direitos dos titulares, retenção, bloqueio, correção, eliminação quando aplicável e resposta a incidentes.
- Condicionar qualquer dado sobre ações judiciais a parecer jurídico documentado e aprovação específica de finalidade, necessidade, hipótese legal, fontes, retenção, acesso e salvaguardas antidiscriminatórias.

## 6. Restrições conhecidas

| Tipo | Restrição | Fonte / responsável | Situação |
|---|---|---|---|
| Jurídica / Privacidade | O tratamento deverá observar a LGPD, inclusive finalidade, adequação, necessidade, qualidade, transparência, segurança, prevenção, não discriminação e prestação de contas | LGPD, art. 6º; validação pelo jurídico e encarregado a confirmar | Confirmada como obrigação; aplicação concreta a definir |
| Trabalhista / Antidiscriminação | Informações sobre ajuizamento de ações não podem sustentar lista restritiva ou prática discriminatória de acesso/manutenção do trabalho | Lei nº 9.029/1995 e orientação institucional do MPT; parecer jurídico necessário | Risco confirmado; uso pretendido a reavaliar |
| Governança | Associados podem atuar como controladores independentes ou conjuntos, ou em outras configurações; papéis e responsabilidades ainda não foram definidos | Jurídico/privacidade | A confirmar |
| Técnica | Alterdata e TOTVS RM possuem produtos, módulos, versões e formas de integração distintas | TI dos associados e fornecedores | A confirmar por associado |
| Segurança | A concentração de CPF e histórico funcional aumenta o impacto de acesso indevido ou incidente | Segurança da informação | A confirmar por análise de risco |
| Qualidade | Motivos de desligamento e advertências podem estar incompletos, não padronizados, desatualizados ou contestados | RH dos associados | A confirmar |
| Operacional | Não existe ainda processo aprovado para correção, contestação, auditoria, retenção e descarte | RH, jurídico, privacidade e TI | A confirmar |

## 7. Premissas e hipóteses

| Item | Classificação | Como validar |
|---|---|---|
| Existe demanda recorrente e legítima por consulta entre associados | Hipótese | Entrevistas, amostra de solicitações e medição de volume/tempo |
| A centralização é melhor que uma consulta federada ou melhoria de processo | Hipótese | Comparar risco, custo, atualização e experiência das alternativas |
| Os associados podem compartilhar parte do histórico funcional com a SAERJ e entre si | Hipótese crítica | Mapear finalidade e fluxo; obter parecer jurídico e definir agentes de tratamento |
| Dados de Alterdata e TOTVS RM podem ser extraídos com qualidade e frequência adequadas | Hipótese | Inventário de versões, APIs, layouts e prova técnica com dados seguros |
| Motivo de desligamento e advertências são necessários para todos os casos de uso | Hipótese crítica | Teste de necessidade por finalidade e minimização campo a campo |
| O uso de informação sobre ações judiciais seria legítimo e não discriminatório | Hipótese crítica, não presumida | Parecer trabalhista/LGPD, teste de balanceamento quando aplicável e avaliação de alternativas menos invasivas |
| A SAERJ dispõe de estrutura para governar acessos e responder aos titulares | Premissa | Avaliar encarregado, segurança, suporte, processos e capacidade operacional |

## 8. Perguntas em aberto

- Qual decisão ou processo legítimo cada tipo de consulta pretende apoiar?
- Quem é o proponente, patrocinador potencial, decisor e dono de negócio?
- A base atenderá empregados atuais, ex-empregados, candidatos ou todos? Por quanto tempo?
- Quais associados participarão e quais versões/módulos de Alterdata, TOTVS RM ou outros sistemas utilizam?
- A SAERJ será controladora, operadora ou controladora conjunta em cada fluxo?
- Qual hipótese legal se aplica a cada finalidade e a cada categoria de dado?
- Quais dados são realmente necessários, e quais devem ser excluídos já no desenho?
- Existe norma coletiva, obrigação legal/regulatória ou política setorial relevante?
- Como o titular será informado e poderá acessar, corrigir ou contestar registros?
- Quem poderá ver advertências e motivos de desligamento, e em quais condições?
- Há necessidade legítima de armazenar processos judiciais, ou esse item deve ser excluído?
- Se alguma informação judicial for mantida para defesa em processo específico, como impedir seu reaproveitamento para recrutamento ou retaliação?
- Quais critérios de retenção, descarte, pseudonimização, criptografia, segregação e auditoria serão exigidos?
- Quais linhas de base permitirão medir tempo, custo, qualidade e risco antes/depois?

## 9. Síntese do Comitê

**Pontos de convergência:** há uma oportunidade de reduzir fragmentação e melhorar rastreabilidade de consultas legítimas. A arquitetura e o conjunto de dados devem ser consequência das finalidades aprovadas, não o ponto de partida.

**Divergências relevantes:** ainda não está demonstrado que uma base centralizada seja preferível a consulta federada ou protocolo entre RHs. O registro de ações judiciais apresenta risco elevado de uso discriminatório e pode inviabilizar ou exigir remoção dessa capacidade.

**Recomendação:** Investigar antes de avançar para definição. Conduzir descoberta com RH, jurídico, encarregado, segurança e representantes dos associados; inventariar sistemas e dados; documentar casos de uso; e comparar alternativas de processo, federação e centralização.

**Justificativa:** o problema e os benefícios foram apresentados apenas em nível inicial, enquanto finalidade, necessidade, papéis dos agentes, hipótese legal, qualidade das fontes, capacidade de integração e salvaguardas ainda não foram demonstrados.

## 10. Portão da rodada 1

**Decisor:** A confirmar

**Decisão:** Aguardando

**Data:** A confirmar

**Condições ou observações:** a ideia permanece no backlog. O rascunho de TAP existente no dossiê é material de estruturação e não significa que a rodada 1 foi aprovada ou que a iniciativa avançou de fase.

## 11. Referências oficiais consultadas

- [Lei Geral de Proteção de Dados Pessoais — Lei nº 13.709/2018](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709compilado.htm).
- [Guia Orientativo da ANPD sobre Legítimo Interesse](https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/guia_orientativo_hipoteses_legais_tratamento_de_dados_pessoais_legitimo_interesse).
- [Orientações da ANPD sobre Relatório de Impacto à Proteção de Dados Pessoais](https://www.gov.br/anpd/pt-br/canais_atendimento/agente-de-tratamento/relatorio-de-impacto-a-protecao-de-dados-pessoais-ripd).
- [Lei nº 9.029/1995 — práticas discriminatórias na relação de trabalho](https://planalto.gov.br/ccivil_03/leis/l9029.htm).
- [Resolução CSMPT nº 210/2023, tema 6.1.2.4 — lista discriminatória](https://midia-ext.mpt.mp.br/pgt/csmpt/resolucoes/resolu210.pdf).
