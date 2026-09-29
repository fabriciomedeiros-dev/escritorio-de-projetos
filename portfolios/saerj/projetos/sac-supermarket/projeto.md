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
**Última atualização:** 29/09/2026

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

### Etapas alinhadas em 29/09/2026

1. **Digitalização de formulários:** levantar infraestrutura, servidores e stack; definir os dados do MVP; levantar as estatísticas desejadas do cliente, inicialmente frequência e tíquete médio.
2. **Integrações com redes sociais:** evoluir os canais de comunicação.
3. **Integrações com os associados.**
4. **Processo interno do associado.**

Esta organização ainda precisa ser reconciliada com o escopo do MVP aprovado em 03/09/2026, especialmente porque redes sociais e workflow interno do associado constam fora do MVP atual. Até essa validação, as etapas 2 a 4 são tratadas como roadmap, não como alteração automática da linha de base.

---

## 4. Estado atual

| Dimensão | Status | Resumo objetivo | Próxima ação |
|---|---|---|---|
| Prazo | 🟡 Atenção | Os marcos de preparação de 16/09 e início de desenvolvimento de 17/09 passaram sem evidência de conclusão neste Escritório; as quatro etapas alinhadas em 29/09 não receberam prazos. | Levantar o avanço real e aprovar um cronograma atualizado. |
| Escopo | 🟡 Atenção | O alinhamento de 29/09 organizou o trabalho em quatro etapas, mas as etapas 2 a 4 podem ampliar o MVP aprovado. | Reconciliar o roadmap com a linha de base e registrar a decisão de escopo. |
| Qualidade | 🟢 Controlado | Critérios de homologação foram identificados. | Formalizar cenários e aceite. |
| Recursos | 🟡 Atenção | A validação de custos e a possível entrada de um novo integrante estavam previstas para 15/09, mas não há resultado registrado no Escritório. | Confirmar custos, participação, papel e disponibilidade do novo integrante. |
| Impedimentos & Riscos | 🟡 Atenção | Dependências externas podem comprometer o início. | Registrar responsável, custo e data de cada dependência. |
| Resultado | 🟢 Controlado | Objetivo do MVP e benefício operacional estão definidos. | Manter foco no núcleo manual do chamado. |

---

## 5. Próximo marco

**Marco:** Replanejamento e validação da primeira etapa

**Data:** A confirmar

**Condição de conclusão:** avanço real levantado; infraestrutura, servidores e stack mapeados; dados do MVP e estatísticas do cliente definidos; roadmap reconciliado com o escopo aprovado.

### Checkpoint anterior — 15/09/2026

A reunião estava prevista com Danielle Moitas e um possível novo integrante do projeto para:

- apresentar e validar as alterações solicitadas no protótipo;
- validar os custos do projeto;
- apresentar e validar o plano de ação e o cronograma;
- avaliar a entrada, o papel e a disponibilidade do possível novo integrante;
- concluir as atividades preparatórias ou registrar explicitamente qualquer pendência antes do início formal do desenvolvimento.

O resultado desse checkpoint ainda não está registrado no Escritório e deve ser apurado na tarefa SAC-009.

## 6. Observação do Escritório de Projetos

O projeto requer replanejamento porque os marcos anteriores passaram sem evidência de conclusão no Escritório. O risco principal é iniciar novas etapas sem reconciliar o roadmap de 29/09 com o MVP aprovado, sem responsáveis, prazos e evidências de infraestrutura e dados.
