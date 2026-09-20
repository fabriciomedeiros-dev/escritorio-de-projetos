# Projeto: SuperSync — Intranet Rede Supermarket

**Navegação:** [Portfólio](../../portfolio.md) · [Governança](governanca.md) · [Módulos](modulos.md) · [Desenvolvimento](desenvolvimento.md) · [Serviços compartilhados](servicos-compartilhados.md) · [Decisões](decisoes.md) · [Tarefas](tarefas.md) · [Histórico](historico.md) · [Reunião de 15/09/2026](reunioes/2026-09-15-alinhamento-marcelo.md) · [Cronograma da Central do Associado](cronogramas/central-do-associado.md)

## 1. Identificação

**ID:** SAERJ-SUPERSYNC

**Portfólio:** saerj

**Visibilidade:** restrita-saerj

**Status geral:** 🔴 Intervenção  
**Responsável:** Fabrício Medeiros  
**Sponsor:** Diretoria da Rede Supermarket, representada por Marcelo Rebelo  
**Fase:** Operação e evolução contínua  
**Início:** A confirmar  
**Previsão de conclusão:** Evolução contínua  
**Última atualização:** 16/09/2026

### Fontes canônicas relacionadas

**Repositório de documentação:** A confirmar  
**Repositório de desenvolvimento:** https://github.com/Liencourt/supersync.git  
**Caminho local observado:** `C:\Users\fabri\Projetos\supersync`  
**Revisão observada:** branch `master`, commit `8c0478c`

---

## 2. Objetivo

### Fato confirmado

O SuperSync é a intranet da Rede Supermarket, possui diversos módulos em produção e permanece em desenvolvimento contínuo.

### Resultado esperado

A confirmar durante a consolidação da linha de base gerencial, incluindo benefícios, públicos atendidos e indicadores de resultado.

---

## 3. Linha de base e escopo

### Incluído

- Operação e evolução dos módulos existentes da intranet;
- validação das entregas de sprint por comparação entre planejamento, documentação e código;
- capacidade de reproduzir a aplicação em ambiente local de desenvolvimento.

### Não incluído

- A confirmar.

### Grau de confiança

| Aspecto | Nível | Observação |
|---|---|---|
| Objetivo | Médio | Finalidade geral confirmada; benefícios e métricas ainda não consolidados. |
| Requisitos | Baixo | Não foi identificada uma linha de base única de requisitos e sprints. |
| Solução | Médio | Código, stack e módulos existem; reprodução local e documentação apresentam lacunas. |

### Pontos ainda desconhecidos

- catálogo oficial de módulos e respectivos estados em produção;
- repositório canônico da documentação funcional;
- cadência, linha de base e critérios de aceite das sprints;
- arquitetura de ambientes, processo de implantação e indicadores operacionais;
- capacidade da equipe, roadmap e prioridades atuais.

---

## 4. Estado atual

| Dimensão | Status | Resumo objetivo | Próxima ação |
|---|---|---|---|
| Prazo | 🟡 Atenção | A Central do Associado avançou além da sequência prevista, com três fases implementadas entre 15 e 16/09; o avanço ainda precisa ser conciliado com o cronograma gerencial e a homologação. | Validar com a equipe o progresso real de cada frente e registrar aceite ou pendências. |
| Escopo | 🟡 Atenção | A `master` já contém portal e permissionamento, gestão de usuários, lojas e auditoria de contratos; grades, contratos ativos e ruptura de promoções ainda não aparecem concluídos como frentes próprias. | Atualizar a linha de base da Central e manter rastreabilidade entre frente, commit, teste e aceite. |
| Qualidade | 🟡 Atenção | Foram identificados 106 testes automatizados da Central do Associado, mas não há evidência consolidada de execução e homologação nesta inspeção. | Executar a suíte na revisão `8c0478c` e registrar resultado e evidências de homologação. |
| Recursos | 🟡 Atenção | Papéis centrais foram definidos; capacidade e responsáveis por módulo ainda precisam ser confirmados. | Mapear donos funcionais e capacidade por módulo. |
| Impedimentos & Riscos | 🔴 Intervenção | Há artefato de credencial versionado e documentação que relata práticas inseguras; a validade e a exposição precisam ser avaliadas. | Fazer triagem de segredos, revogar se necessário e retirar artefatos do histórico conforme plano aprovado. |
| Resultado | 🟡 Atenção | O uso em produção foi confirmado, mas benefícios e indicadores ainda não estão registrados por módulo. | Fornecer evidências do Acordos Comerciais à atividade transversal de mensuração de ganhos e valoração da TI. |

---

## 5. Próximo marco

**Marco:** Validar a primeira entrega da Central do Associado e reconciliar código, cronograma e homologação
**Data:** 21/09/2026
**Condição de conclusão:** fases implementadas classificadas por frente gerencial, suíte executada na revisão `8c0478c`, responsáveis confirmados e aceite ou pendências do módulo de permissionamento registrados.

## 6. Observação do Escritório de Projetos

O SuperSync é o projeto piloto para integrar gestão, documentação e desenvolvimento. A Central do Associado apresenta implementação avançada, mas o estado gerencial permanece em intervenção até que segurança, reprodução, testes executados e homologação estejam formalmente evidenciados.
