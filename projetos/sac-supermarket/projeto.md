# Projeto: SAC — Supermarket

## 1. Identificação

**Status geral:** 🟡 Atenção  
**Responsável:** Fabrício Medeiros  
**Área patrocinadora:** Marketing  
**Decisão de escopo:** Danielle Moitas  
**Orçamento e prioridade:** Marcelo Rebelo, CEO interino  
**Início formal do desenvolvimento:** 17/09/2026  
**Go-Live:** A definir após cronograma detalhado  
**Última atualização:** 09/09/2026

**Repositório de entrega:** https://github.com/fabriciomedeiros-dev/SAC  
**Fonte técnica e funcional:** repositório SAC, pasta `gestao/` e documentação Docusaurus.

---

## 2. Objetivo

Centralizar reclamações e atendimentos de múltiplos canais em uma plataforma única, oferecendo contexto ao operador, encaminhamento ao associado, controle de SLA, histórico de tratativas e indicadores de acompanhamento.

### Resultado esperado

Reduzir a dependência de e-mail e de controles dispersos, mantendo as tratativas registradas na plataforma e permitindo acompanhamento executivo do atendimento.

---

## 3. Linha de base e escopo

### Incluído no MVP

- Captura via Reclame Aqui por API;
- e-mail, site, App do Clube, telefone e Agência Digital;
- perfil único de Operador de SAC para triagem e telefone;
- encaminhamento ao associado, devolutiva, evidência, SLA, histórico e indicadores básicos;
- Data Lake apenas para consulta e enriquecimento de contexto.

### Não incluído no MVP

- Google Meu Negócio, WhatsApp e BuzzMonitor;
- gestão de usuários pelo associado;
- workflow interno do associado;
- retenção de sandbox para treinamento contínuo.

### Premissas e dependências

- Data Lake, API Reclame Aqui, e-mail, formulários de site/app e ambiente de hospedagem precisam ser mapeados;
- Reclame Aqui começa cedo, mas não bloqueia o núcleo manual do chamado;
- custos, fornecedores, responsáveis e datas precisam estar consolidados antes do desenvolvimento.

---

## 4. Estado atual

| Dimensão | Status | Resumo objetivo | Próxima ação |
|---|---|---|---|
| Prazo | 🟡 Atenção | Pré-desenvolvimento deve encerrar até 16/09; desenvolvimento inicia em 17/09. | Consolidar datas, dependências e critérios de homologação. |
| Escopo | 🟡 Atenção | Definições do MVP registradas, pendente consolidação formal. | Danielle validar MVP consolidado. |
| Qualidade | 🟢 Controlado | Critérios de homologação foram identificados. | Formalizar cenários e aceite. |
| Recursos | 🟡 Atenção | Custos, fornecedor e capacidade ainda precisam ser mapeados. | Alexandro, Filipe e Fabrício consolidarem levantamento. |
| Impedimentos & Riscos | 🟡 Atenção | Dependências externas podem comprometer o início. | Registrar responsável, custo e data de cada dependência. |
| Resultado | 🟢 Controlado | Objetivo do MVP e benefício operacional estão definidos. | Manter foco no núcleo manual do chamado. |

---

## 5. Próximo marco

**Marco:** Prontidão para início do desenvolvimento  
**Data:** 16/09/2026  
**Condição de conclusão:** MVP aprovado, dependências e custos registrados, plano de execução e critérios de homologação definidos.

## 6. Observação do Escritório de Projetos

O projeto está em fase crítica de preparação. O risco principal não é a API Reclame Aqui isoladamente, mas a falta de uma visão consolidada de dependências, custos e responsáveis antes do início formal do desenvolvimento.
