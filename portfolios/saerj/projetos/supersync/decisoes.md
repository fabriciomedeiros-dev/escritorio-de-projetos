# Decisões — SuperSync

**Navegação:** [Projeto](projeto.md) · [Governança](governanca.md) · [Módulos](modulos.md) · [Tarefas](tarefas.md) · [Histórico](historico.md)

## 10/09/2026 — Integração ao Escritório e adoção da camada de desenvolvimento

**Status:** Aprovada  
**Decisor:** Fabrício Medeiros  
**Contexto:** O SuperSync possui módulos em produção e desenvolvimento contínuo, mas ainda não fazia parte do Escritório de Projetos.  
**Opções avaliadas:** Manter o acompanhamento somente no repositório de código ou integrar gestão, documentação e desenvolvimento com autoridades distintas.  
**Recomendação do Conselho:** Integrar o projeto e usar o repositório de desenvolvimento como evidência do que foi implementado, sem permitir que o código redefina automaticamente o escopo.  
**Decisão:** O SuperSync será o piloto da camada de desenvolvimento. A validação das sprints comparará planejamento e documentação com uma revisão identificada do código.  
**Impacto:** Exige linha de base gerencial, catálogo de módulos, rastreabilidade de sprint, reprodução local e tratamento dos riscos técnicos encontrados.  
**Ações decorrentes:** SS-001 a SS-006.  
**Evidências / referências:** `projeto.md`; `desenvolvimento.md`; repositório `https://github.com/Liencourt/supersync.git`.

## 11/09/2026 — Governança operacional

**Status:** Aprovada  
**Decisor:** Fabrício Medeiros  
**Decisão:** Marcelo representa a diretoria como sponsor; Fabrício gerencia o projeto; Alexandro responde por desenvolvimento e segurança; Filipe responde por dados; cada módulo terá dono funcional. Demandas passam pela triagem de Fabrício, com exceção de incidentes urgentes. Publicação restrita pode anteceder o aceite; liberação ampla exige dono funcional, Fabrício e Marcelo.  
**Impacto:** Institui acompanhamento semanal, ciclos por módulo, piloto do canal Teams e documento executivo para decisões financeiras.  
**Referência:** [Governança](governanca.md); [modelo de decisão financeira](../../../../modelos/decisao-financeira.md).

## 11/09/2026 — Serviços compartilhados e projetos consumidores

**Status:** Aprovada  
**Decisor:** Fabrício Medeiros  
**Decisão:** Projetos independentes podem consumir capacidades técnicas do SuperSync sem se tornarem iniciativas subordinadas. O SAC utilizará a gestão de usuários e autenticação do SuperSync, mantendo gestão, escopo e aceite próprios.  
**Impacto:** Exige donos nos dois projetos, critérios de aceite, compatibilidade e contingência documentados antes da integração.  
**Referência:** [Serviços compartilhados](servicos-compartilhados.md); [dependências do SAC](../sac-supermarket/dependencias.md).
