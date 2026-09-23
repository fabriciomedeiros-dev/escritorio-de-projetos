# Termo de Abertura Preliminar — Base Centralizada de Histórico Funcional

**ID da ideia:** SAERJ-IDEIA-001

**Portfólio pretendido:** saerj

**Versão:** 0.1 — rascunho para futura rodada 2

**Estado:** Backlog — estruturação preliminar; portão da rodada 1 não aprovado

**Data:** 22/09/2026

> Este documento organiza uma possível proposta de projeto. Ele não autoriza execução, orçamento, tratamento de dados pessoais, integração com sistemas ou entrada no portfólio. Deverá ser revisto após a descoberta e a decisão humana do portão da rodada 1.

## 1. Contexto e justificativa

A SAERJ avalia criar uma capacidade centralizada para consultar, a partir do CPF, informações funcionais mantidas por seus associados em sistemas como Alterdata e TOTVS RM. A visão inicial inclui datas de admissão e desligamento, motivo do desligamento, advertências e eventual histórico de ações judiciais envolvendo trabalhadores e associados.

A situação atual, o volume de consultas, o custo operacional e a qualidade dos registros ainda não foram medidos. A justificativa de negócio é, portanto, uma hipótese: reduzir tempo e retrabalho de consultas legítimas e aumentar consistência e rastreabilidade.

A mesma centralização eleva riscos relevantes. O conjunto proposto permite formar perfis detalhados de trabalhadores e ex-trabalhadores, concentra identificadores e ocorrências funcionais e pode afetar direitos, reputação e acesso ao trabalho caso seja inexato, acessado indevidamente ou usado para finalidade discriminatória. Em especial, a existência de ação judicial não deverá ser convertida em restrição, pontuação ou recomendação sobre contratação, permanência ou desligamento.

## 2. Problema

**Hipótese de problema:** dados de vínculos e ocorrências funcionais estão fragmentados entre associados e plataformas distintas, dificultando consultas autorizadas, atualização, conciliação e auditoria.

**Nível de confiança:** baixo. Há apenas o relato inicial; ainda faltam mapeamento do processo, casos de uso, evidências de demanda, inventário de dados, usuários, sistemas e integrações.

## 3. Objetivo geral

Disponibilizar, se demonstradas viabilidade e legitimidade, uma capacidade segura e auditável de consulta ao histórico funcional mínimo necessário para finalidades específicas e aprovadas, com integração controlada aos sistemas de RH dos associados e proteção efetiva aos direitos dos titulares.

## 4. Objetivos específicos

- Mapear e padronizar fontes, conceitos e regras de qualidade dos dados funcionais aprovados.
- Reduzir o tempo e o esforço de consultas legítimas realizadas por usuários autorizados.
- Informar origem, atualização e confiabilidade de cada registro apresentado.
- Garantir segregação, menor privilégio, justificativa de acesso e trilha de auditoria.
- Definir processos de transparência, acesso, correção, contestação, retenção e descarte.
- Integrar progressivamente sistemas de RH sem pressupor compatibilidade uniforme entre produtos e versões.
- Impedir uso discriminatório, perfilamento indevido ou decisão exclusivamente automatizada.
- Demonstrar conformidade e gestão de riscos antes de operar com dados pessoais reais.

## 5. Benefícios e resultados esperados

| Resultado / benefício | Indicador | Linha de base | Meta | Evidência | Confiança |
|---|---|---|---|---|---|
| Consulta mais ágil | Tempo médio entre solicitação autorizada e resposta | A levantar | A definir após linha de base | Registros do processo atual e futuro | Hipótese |
| Menor esforço manual | Horas de RH por consulta | A levantar | A definir | Apontamento amostral antes/depois | Hipótese |
| Maior qualidade | Percentual de registros completos, conciliados e atualizados | A levantar | A definir | Relatório de qualidade por fonte | Hipótese |
| Rastreabilidade | Percentual de consultas com usuário, finalidade, justificativa e resultado registrados | Inexistente ou A confirmar | 100% das consultas | Logs protegidos e auditoria | Estimativa inicial |
| Proteção dos titulares | Contestações tratadas no prazo; incidentes; acessos indevidos | A levantar | Metas a aprovar | Registros do encarregado, segurança e suporte | Hipótese |
| Cobertura de integração | Associados/fontes integrados e sincronizações bem-sucedidas | 0 no novo serviço | A definir por fase | Monitoramento dos conectores | Hipótese |
| Minimização | Percentual de campos com finalidade, hipótese legal, retenção e perfil de acesso aprovados | Não definido | 100% antes da produção | Inventário e registro das operações de tratamento | Estimativa inicial |

## 6. Escopo preliminar

### Incluído para descoberta e desenho

- Mapeamento de casos de uso, usuários, decisões apoiadas e fluxo atual.
- Inventário de associados, sistemas, módulos, versões, dados e mecanismos de integração.
- Classificação campo a campo de finalidade, necessidade, origem, qualidade, hipótese legal, acesso e retenção.
- Definição dos papéis da SAERJ e dos associados como agentes de tratamento.
- Comparação entre melhoria de processo, consulta federada e base centralizada.
- Arquitetura conceitual de identidade, autorização, segregação, criptografia, auditoria, integração, reconciliação e descarte.
- Avaliação jurídica, trabalhista, de privacidade e segurança, incluindo necessidade de RIPD e teste de balanceamento quando aplicável.
- Prova de conceito apenas com dados sintéticos, anonimizados de forma efetiva ou ambiente especificamente aprovado.
- Desenho de governança, atendimento ao titular, correção, contestação e resposta a incidentes.

### Incluído em eventual MVP, sujeito a aprovação posterior

- Cadastro dos associados participantes e das fontes autorizadas.
- Resolução de identidade por CPF protegido, sem busca pública ou acesso irrestrito.
- Consulta de vínculos com associado, datas de admissão e desligamento, origem e última atualização.
- Motivo de desligamento somente se sua necessidade for demonstrada e o acesso for especificamente autorizado.
- Advertências somente se sua necessidade for demonstrada, com evidência de origem, acesso restrito e possibilidade de contestação.
- Conectores de um recorte representativo de Alterdata e/ou TOTVS RM, conforme versões efetivamente utilizadas.
- Administração de perfis e acessos, autenticação forte, justificativa de consulta, auditoria e monitoramento.
- Processos de correção, bloqueio, retenção e descarte definidos para o recorte aprovado.

### Não incluído

- Lista de trabalhadores “não recomendados”, blacklist ou ranking de risco.
- Recomendação automática ou decisão exclusivamente automatizada de contratar, manter, advertir ou desligar.
- Consulta aberta por qualquer empregado, associado ou terceiro.
- Coleta indiscriminada de processos judiciais, certidões, dados de saúde, biometria, filiação sindical, origem racial/étnica, religião ou outros dados sem finalidade e hipótese legal específicas.
- Compartilhamento integral das bases de RH dos associados.
- Substituição dos sistemas de RH de origem.
- Inclusão automática de todos os produtos, módulos e versões de Alterdata e TOTVS RM.
- Aquisição, contratação ou adoção de uma solução pronta para substituir o desenvolvimento da capacidade sob governança da SAERJ.
- Uso secundário dos dados para marketing, prospecção, treinamento de modelos ou finalidades incompatíveis.
- Disponibilização de dados reais antes da aprovação jurídica, de privacidade, segurança e governança.

### Item suspenso para validação jurídica

A identificação de ações judiciais ajuizadas por trabalhadores contra associados fica suspensa como capacidade do produto. Se houver necessidade relacionada à defesa de um processo concreto, ela deverá ser tratada em fluxo jurídico específico, com acesso restrito e sem reutilização para recrutamento, permanência, desligamento, retaliação ou compartilhamento em lista. Sua inclusão futura exige decisão humana expressa apoiada por parecer jurídico e de proteção de dados.

## 7. Entregas principais

| Entrega | Resultado verificável | Critério inicial de aceite |
|---|---|---|
| Diagnóstico do processo atual | Casos de uso, atores, volumes, tempos, decisões e problemas documentados | RH, jurídico e associados participantes validam o mapa |
| Inventário de dados e sistemas | Fontes, versões, campos, responsáveis, qualidade e integrações catalogados | Cada campo possui origem e responsável identificados |
| Avaliação jurídica e de privacidade | Finalidades, hipóteses legais, agentes, direitos e riscos analisados | Jurídico e encarregado emitem pareceres e condições documentadas |
| RIPD ou avaliação equivalente | Tratamentos, riscos aos titulares e salvaguardas descritos | Documento aprovado antes de dados reais, conforme decisão do controlador |
| Estudo de alternativas | Centralização, federação e melhoria de processo comparadas | Decisor escolhe direção com base em valor, risco e custo |
| Modelo de governança | Matriz de acesso, retenção, correção, contestação, incidentes e auditoria | Donos e procedimentos aprovados |
| Prova técnica | Integração representativa executada com dados seguros | Sincronização, reconciliação, falhas e auditoria demonstradas |
| Proposta de MVP | Recorte, cronograma, custos, critérios de sucesso e condições de go-live | Patrocinador, jurídico, privacidade, segurança e negócio aprovam |

## 8. Requisitos de alto nível

### Negócio e dados

- Cada consulta deve estar vinculada a finalidade aprovada e perfil autorizado.
- Cada atributo deve ter definição, sistema de origem, responsável, atualização, qualidade, hipótese legal e prazo de retenção.
- O sistema deve diferenciar vínculo atual, vínculo encerrado, ocorrência contestada e informação indisponível.
- Registros não comprovados ou opiniões livres não devem ser apresentados como fatos.
- Divergências entre fontes devem ser sinalizadas, sem sobrescrita silenciosa.
- Correções na origem devem propagar-se para a consulta central conforme SLA definido.

### Privacidade, direitos e não discriminação

- Aplicar privacidade desde a concepção e por padrão, minimização e limitação de finalidade.
- Documentar os agentes de tratamento e responsabilidades em cada fluxo.
- Implementar canal e procedimento para acesso, correção, contestação e demais direitos aplicáveis.
- Elaborar RIPD antes do uso de dados reais se a avaliação indicar alto risco, seguindo orientação da ANPD.
- Se legítimo interesse for cogitado, realizar teste de finalidade, necessidade, balanceamento e salvaguardas, sem presumir que essa será a base adequada.
- Não usar histórico de ação judicial como fator negativo de decisão trabalhista ou lista compartilhada.
- Submeter novos campos, fontes e usos a revisão de finalidade e risco antes da ativação.

### Segurança e auditoria

- Autenticação forte e autorização baseada em papéis e contexto.
- Segregação entre associados e menor privilégio.
- Criptografia em trânsito e em repouso; proteção específica do CPF e segredos de integração.
- Logs de consultas, visualizações, exportações, alterações e decisões administrativas protegidos contra adulteração.
- Monitoramento de comportamento anômalo, exportação em massa e tentativas de enumeração de CPF.
- Ambientes separados e proibição de dados pessoais reais em desenvolvimento sem aprovação excepcional.
- Testes de segurança e plano de resposta a incidentes antes da produção.

### Integração e operação

- Conectores desacoplados por produto, módulo, versão e associado.
- Suportar API, arquivo ou outro mecanismo aprovado, com autenticação, idempotência e validação.
- Registrar sincronização, falha, rejeição, atraso e reconciliação.
- Definir fonte autoritativa por atributo e processo de correção.
- Operar com indisponibilidade temporária sem exibir dado antigo como atual.
- Estabelecer SLA, suporte, continuidade, backup e recuperação compatíveis com o risco.

## 9. Restrições

- A LGPD e as regras trabalhistas aplicáveis condicionam o desenho e podem tornar certos usos inviáveis.
- A SAERJ e os associados ainda não definiram finalidades, hipóteses legais nem responsabilidades como agentes de tratamento.
- Integrações variam conforme produto, módulo, versão, contratação e configuração de Alterdata, TOTVS RM e outros sistemas.
- Dados históricos podem conter códigos locais, texto livre, erros ou registros sem documentação suficiente.
- Prazo, orçamento, equipe, infraestrutura, associados-piloto e patrocinador não estão definidos.
- Nenhum dado pessoal real deverá ser carregado apenas para “testar” a ideia sem controles e aprovações prévios.

## 10. Premissas

- RH, jurídico, encarregado, segurança e representantes de associados participarão da descoberta.
- Será possível obter layouts, dicionários e amostras sintéticas ou efetivamente anonimizadas.
- Os associados informarão versões e mecanismos de integração contratados nos sistemas de origem.
- Existirão casos de uso legítimos que possam ser atendidos com conjunto mínimo de dados.
- A governança terá autoridade para bloquear usos incompatíveis e tratar contestações.

## 11. Riscos iniciais

| Risco | Probabilidade | Impacto | Resposta inicial | Dono proposto |
|---|---|---|---|---|
| Uso discriminatório de ações judiciais ou histórico funcional | Alta | Muito alto | Suspender a capacidade; parecer jurídico; controles antidiscriminação; proibir ranking e decisão automática | Jurídico e Compliance — a confirmar |
| Finalidade ampla ou incompatível entre associados | Alta | Alto | Definir casos de uso e base legal por finalidade; bloquear uso secundário | Encarregado/Jurídico — a confirmar |
| Vazamento ou consulta indevida por CPF | Média | Muito alto | Menor privilégio, MFA, justificativa, rate limit, monitoramento, criptografia e auditoria | Segurança — a confirmar |
| Informação incorreta prejudicar trabalhador | Alta | Alto | Fonte e atualização visíveis; validação; contestação; correção; não automatizar decisões | RH/Governança de dados — a confirmar |
| Centralização exceder o necessário | Alta | Alto | Comparar federação e processo; minimização campo a campo; revisão arquitetural | Negócio, Privacidade e Arquitetura |
| Integrações não suportadas ou divergentes | Alta | Médio/Alto | Inventariar versões e contratos; piloto com conectores representativos | TI/Integração — a confirmar |
| Associado compartilhar dados sem papel e obrigação definidos | Média | Alto | Acordos, matriz de responsabilidades e aprovação prévia ao onboarding | Jurídico — a confirmar |
| Retenção indefinida ampliar danos | Alta | Alto | Tabela de temporalidade por finalidade e descarte verificável | Jurídico, RH e Privacidade |
| Escopo crescer para dados sensíveis ou perfilamento | Média | Muito alto | Lista negativa de dados/usos; gate de privacidade para mudanças | Comitê de governança — a confirmar |
| Baixa adesão dos associados | Média | Médio/Alto | Validar valor, custo e capacidade com grupo piloto antes do investimento | Patrocinador — a confirmar |

## 12. Stakeholders e governança proposta

| Papel | Pessoa / área | Responsabilidade | Confirmado? |
|---|---|---|---|
| Proponente | A confirmar | Apresentar problema e defender o caso de negócio | Não |
| Patrocinador | A confirmar | Autorizar direção, recursos e riscos residuais | Não |
| Responsável pelo produto | A confirmar | Priorizar casos de uso e critérios de sucesso | Não |
| RH da SAERJ/associados | A confirmar | Validar processo, conceitos, qualidade e operação | Não |
| Jurídico trabalhista | A confirmar | Avaliar finalidade, discriminação, compartilhamento e uso processual | Não |
| Encarregado/DPO | A confirmar | Orientar LGPD, direitos dos titulares, RIPD e governança | Não |
| Segurança da informação | A confirmar | Definir e validar controles e resposta a incidentes | Não |
| Arquitetura/Integrações | A confirmar | Inventariar fontes e avaliar alternativas técnicas | Não |
| Fornecedores Alterdata/TOTVS | A confirmar | Esclarecer interfaces, contratos, limites e suporte | Não |
| Representantes dos trabalhadores | A confirmar | Contribuir sobre transparência, impactos e mecanismos de contestação | Não |
| Decisor do portfólio | A confirmar | Decidir portões e eventual promoção | Não |

## 13. Marcos preliminares

| Marco | Previsão | Condição de conclusão |
|---|---|---|
| Nomeação dos responsáveis | A confirmar | Proponente, decisor, jurídico, DPO, segurança e TI identificados |
| Descoberta dos casos de uso | A confirmar | Finalidades, usuários, decisões e volumes documentados |
| Inventário de dados e integrações | A confirmar | Associados, sistemas, versões, campos e mecanismos mapeados |
| Triagem jurídica e de privacidade | A confirmar | Usos proibidos, condicionados e admissíveis classificados |
| Portão da rodada 1 | A confirmar | Decisor escolhe avançar, investigar, reformular ou arquivar |
| Estudo de alternativas | A confirmar | Processo, federação e centralização comparados |
| Prova de conceito segura | A confirmar | Fluxo representativo validado sem exposição indevida |
| TAP revisado e portão da rodada 2 | A confirmar | Escopo, riscos, recursos e condições aprovados ou devolvidos |

## 14. Recursos e investimento

A confirmar. A estimativa deverá separar descoberta, assessoria jurídica e privacidade, arquitetura, conectores por sistema/versão, governança de dados, segurança, infraestrutura, licenças, implantação, suporte, auditoria e atendimento aos titulares. Este rascunho não representa autorização financeira.

## 15. Pendências para decisão

- Nomear proponente, decisor, patrocinador potencial e responsáveis de RH, jurídico, privacidade, segurança e TI.
- Documentar os casos de uso e decisões que a consulta pretende apoiar.
- Obter amostra quantitativa de volume, tempo, custo, erros e urgência do processo atual.
- Inventariar associados, sistemas, módulos, versões, contratos, APIs e layouts.
- Mapear todos os campos propostos e eliminar os que não forem necessários.
- Emitir avaliação jurídica específica sobre compartilhamento entre associados e informação sobre ações judiciais.
- Definir agentes de tratamento e responsabilidades contratuais e operacionais.
- Avaliar necessidade de RIPD e elaborar o documento antes de tratamento de alto risco com dados reais.
- Comparar base centralizada, consulta federada e protocolo de resposta entre RHs.
- Selecionar associado e fonte para eventual prova de conceito com dados seguros.
- Definir linha de base, metas, custo preliminar e critérios de interrupção.

## 16. Portão da rodada 2

**Decisor:** A confirmar

**Decisão:** Aguardando — rodada 2 ainda não iniciada

**Data:** A confirmar

**Condições ou observações:** este rascunho existe para antecipar os pontos críticos da futura TAP. A iniciativa permanece no backlog e só poderá avançar após decisão humana explícita no portão da rodada 1.

## 17. Referências oficiais consultadas

- [Lei Geral de Proteção de Dados Pessoais — Lei nº 13.709/2018](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709compilado.htm).
- [Guia Orientativo da ANPD sobre Legítimo Interesse](https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/guia_orientativo_hipoteses_legais_tratamento_de_dados_pessoais_legitimo_interesse).
- [Orientações da ANPD sobre Relatório de Impacto à Proteção de Dados Pessoais](https://www.gov.br/anpd/pt-br/canais_atendimento/agente-de-tratamento/relatorio-de-impacto-a-protecao-de-dados-pessoais-ripd).
- [Lei nº 9.029/1995 — práticas discriminatórias na relação de trabalho](https://planalto.gov.br/ccivil_03/leis/l9029.htm).
- [Resolução CSMPT nº 210/2023, tema 6.1.2.4 — lista discriminatória](https://midia-ext.mpt.mp.br/pgt/csmpt/resolucoes/resolu210.pdf).
