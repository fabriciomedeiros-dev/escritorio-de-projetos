# Projeto: SAC — Supermarket

**Navegação:** [Portfólio](../../portfolio.md) · [Decisões](decisoes.md) · [Tarefas](tarefas.md) · [Histórico](historico.md) · [Comunicação](comunicacao.md) · [Dependências](dependencias.md) · [Protótipo](artefatos/prototipo/README.md)

## 1. Identificação

**ID:** SAERJ-SAC

**Portfólio:** saerj

**Visibilidade:** restrita-saerj

**Status geral:** 🟡 Atenção  
**Responsável:** Fabrício Medeiros  
**Área patrocinadora:** Marketing  
**Decisão de escopo:** Danielle Moitas  
**Orçamento e prioridade:** Marcelo Rebelo, CEO interino  
**Início formal do desenvolvimento:** 17/09/2026  
**Go-Live:** A definir após cronograma detalhado  
**Última atualização:** 15/09/2026

**Repositório de entrega:** https://github.com/fabriciomedeiros-dev/SAC  
**Fonte técnica e funcional:** repositório SAC, pasta `gestao/` e documentação Docusaurus.
**Local canônico do protótipo:** [artefatos/prototipo](artefatos/prototipo/README.md); quando hospedado externamente, registrar ali o link e a versão apresentada.

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
- gestão de usuários e autenticação utilizarão o SuperSync, com interface, perfis e contingência ainda a validar;
- Reclame Aqui começa cedo, mas não bloqueia o núcleo manual do chamado;
- custos, fornecedores, responsáveis e datas precisam estar consolidados antes do desenvolvimento.

---

## 4. Estado atual

| Dimensão | Status | Resumo objetivo | Próxima ação |
|---|---|---|---|
| Prazo | 🟡 Atenção | Reunião final de preparação prevista para 15/09; pré-desenvolvimento deve encerrar até 16/09 e desenvolvimento inicia em 17/09. | Apresentar e validar o plano de ação e o cronograma. |
| Escopo | 🟡 Atenção | Alterações solicitadas no protótipo serão apresentadas para validação final com Danielle. | Registrar o aceite ou as pendências remanescentes do protótipo e do MVP. |
| Qualidade | 🟢 Controlado | Critérios de homologação foram identificados. | Formalizar cenários e aceite. |
| Recursos | 🟡 Atenção | Custos serão validados na reunião de 15/09 e há um possível novo integrante a ser apresentado e avaliado para o projeto. | Confirmar custos, participação, papel e disponibilidade do novo integrante. |
| Impedimentos & Riscos | 🟡 Atenção | Dependências externas podem comprometer o início. | Registrar responsável, custo e data de cada dependência. |
| Resultado | 🟢 Controlado | Objetivo do MVP e benefício operacional estão definidos. | Manter foco no núcleo manual do chamado. |

---

## 5. Próximo marco

**Marco:** Prontidão para início do desenvolvimento  
**Data:** 16/09/2026  
**Condição de conclusão:** MVP aprovado, dependências e custos registrados, plano de execução e critérios de homologação definidos.

### Checkpoint imediato — 15/09/2026

Reunião com Danielle Moitas e um possível novo integrante do projeto para:

- apresentar e validar as alterações solicitadas no protótipo;
- validar os custos do projeto;
- apresentar e validar o plano de ação e o cronograma;
- avaliar a entrada, o papel e a disponibilidade do possível novo integrante;
- concluir as atividades preparatórias ou registrar explicitamente qualquer pendência antes do início formal do desenvolvimento.

## 6. Observação do Escritório de Projetos

O projeto está em fase crítica de preparação. O risco principal não é a API Reclame Aqui isoladamente, mas a falta de uma visão consolidada de dependências, custos e responsáveis antes do início formal do desenvolvimento.
