# Plano de Atividades e Entregas — SAC — Supermarket

**Situação:** Rascunho para validação  
**Data-base:** 29/09/2026  
**Responsável pela consolidação:** Fabrício Medeiros

> Este plano propõe uma nova linha de base porque os registros disponíveis terminam em 15/09/2026 e os marcos de preparação previstos para 16 e 17/09/2026 já passaram. As datas abaixo pressupõem início do replanejamento em 30/09/2026 e devem ser confirmadas com a equipe.

## 1. Papéis de referência

| Papel | Responsável | Responsabilidade no plano |
|---|---|---|
| Gestão do projeto | Fabrício Medeiros | Consolidar plano, acompanhar prazos, riscos, dependências e comunicação. |
| Decisão e aceite funcional | Danielle Moitas | Validar escopo, regras de negócio, protótipo e homologação funcional. |
| Liderança técnica | Alexandro Nascimento | Definir solução, coordenar desenvolvimento e responder pelas integrações técnicas. |
| Validação técnica | Filipe Fachetti | Revisar solução, apoiar testes técnicos e validar critérios não funcionais. |
| Orçamento, prioridade e Go-Live | Marcelo Rebelo | Aprovar custos, prioridade executiva e entrada em produção. |
| Novo integrante | A confirmar | Definir papel, disponibilidade e entregas antes da alocação no cronograma. |

## 2. Linha de base proposta

| ID | Fase | Atividade | Entrega / critério de conclusão | Responsável principal | Apoio / aprovação | Início | Prazo | Dependências | Status inicial |
|---|---|---|---|---|---|---|---|---|---|
| SAC-P01 | Replanejamento | Levantar o avanço real desde 15/09 e reclassificar tarefas abertas | Diagnóstico de situação com concluídos, pendências, bloqueios e evidências | Fabrício | Alexandro, Filipe e Danielle | 30/09/2026 | 30/09/2026 | Retorno da equipe | A iniciar |
| SAC-P02 | Replanejamento | Confirmar equipe, capacidade e papel do possível novo integrante | Matriz de alocação com papel, disponibilidade e responsabilidade por entrega | Fabrício | Alexandro; Marcelo aprova eventual custo | 30/09/2026 | 01/10/2026 | SAC-P01 | A iniciar |
| SAC-P03 | Escopo | Consolidar MVP e alterações finais do protótipo | Linha de base do MVP e protótipo com aceite funcional registrado | Fabrício | Danielle aprova; Alexandro avalia viabilidade | 30/09/2026 | 02/10/2026 | SAC-P01 | A iniciar |
| SAC-P04 | Dependências | Mapear Data Lake, Reclame Aqui, e-mail, site/app, Agência Digital e hospedagem | Quadro completo com dono, fornecedor, custo, data, interface e contingência | Alexandro | Filipe e Fabrício; Marcelo decide custos | 30/09/2026 | 02/10/2026 | SAC-P01 | A iniciar |
| SAC-P05 | Planejamento técnico | Definir arquitetura, integrações, segurança, ambientes e estratégia de implantação | Desenho técnico aprovado e backlog técnico priorizado | Alexandro | Filipe valida | 02/10/2026 | 06/10/2026 | SAC-P03 e SAC-P04 | A iniciar |
| SAC-P06 | Homologação | Definir cenários, massa de dados, critérios de aceite e agenda de homologação | Plano de testes e homologação aprovado | Fabrício | Danielle, Alexandro e Filipe | 02/10/2026 | 06/10/2026 | SAC-P03 e SAC-P05 | A iniciar |
| SAC-P07 | Desenvolvimento | Implementar o núcleo manual do chamado: cadastro, triagem, direcionamento, SLA, resposta, evidência e histórico | Fluxo ponta a ponta disponível em ambiente de testes | Alexandro | Equipe técnica a confirmar | 07/10/2026 | 16/10/2026 | SAC-P05 | A iniciar |
| SAC-P08 | Desenvolvimento | Implementar perfis, permissões e autenticação via SuperSync | Operador e associado acessam somente as funções autorizadas; contingência documentada | Alexandro | Filipe; Fabrício define requisitos | 07/10/2026 | 14/10/2026 | Serviço do SuperSync e SAC-P05 | A iniciar |
| SAC-P09 | Integrações | Integrar e-mail, site, App do Clube e Agência Digital | Chamados dos canais entram identificados e rastreáveis no SAC | Alexandro | Donos dos canais a confirmar | 13/10/2026 | 21/10/2026 | Acessos e interfaces do SAC-P04 | A iniciar |
| SAC-P10 | Integrações | Implementar captura pela API do Reclame Aqui | Chamados capturados sem duplicidade, com tratamento de falhas e rastreabilidade | Alexandro | Fornecedor/contato do Reclame Aqui a confirmar | 13/10/2026 | 23/10/2026 | Credenciais, contrato e documentação | A iniciar |
| SAC-P11 | Contexto de atendimento | Disponibilizar consulta ao Data Lake | Operador consulta dados necessários sem alteração da fonte | Alexandro | Dono do Data Lake a confirmar | 15/10/2026 | 23/10/2026 | Acesso e regras de dados | A iniciar |
| SAC-P12 | Indicadores | Implementar painel básico de volume, status, SLA e tempo de atendimento | Indicadores reconciliados com amostra de chamados | Alexandro | Fabrício e Danielle validam | 19/10/2026 | 27/10/2026 | SAC-P07 e dados das integrações | A iniciar |
| SAC-P13 | Qualidade | Executar testes funcionais, integrados, de permissão e de recuperação de falhas | Evidências de teste e defeitos críticos corrigidos | Filipe | Alexandro e equipe técnica | 22/10/2026 | 29/10/2026 | SAC-P07 a SAC-P12 | A iniciar |
| SAC-P14 | Homologação | Realizar homologação funcional com Marketing | Termo de aceite funcional ou lista fechada de ajustes | Danielle | Fabrício coordena; Alexandro corrige | 30/10/2026 | 04/11/2026 | SAC-P06 e SAC-P13 | A iniciar |
| SAC-P15 | Implantação | Preparar produção, suporte, monitoramento, comunicação e plano de retorno | Checklist de implantação aprovado e decisão de Go-Live registrada | Alexandro | Fabrício e Filipe; Marcelo autoriza | 03/11/2026 | 06/11/2026 | SAC-P13 e SAC-P14 | A iniciar |
| SAC-P16 | Go-Live | Implantar o MVP em produção | MVP disponível, monitorado e com responsáveis de suporte acionáveis | Alexandro | Marcelo autoriza; Fabrício comunica | 09/11/2026 | 09/11/2026 | SAC-P15 | Proposto |
| SAC-P17 | Estabilização | Acompanhar operação assistida e corrigir falhas prioritárias | Relatório de estabilização, pendências residuais e aceite de encerramento da fase | Fabrício | Alexandro, Filipe e Danielle | 09/11/2026 | 20/11/2026 | SAC-P16 | A iniciar |

## 3. Marcos propostos

| Marco | Data proposta | Condição de conclusão | Decisor / aceite |
|---|---|---|---|
| Linha de base aprovada | 02/10/2026 | Escopo, equipe, dependências, custos e cronograma confirmados | Danielle, Alexandro e Marcelo conforme suas alçadas |
| Solução pronta para testes integrados | 23/10/2026 | Núcleo, autenticação e integrações prioritárias disponíveis | Alexandro |
| Qualidade técnica aprovada | 29/10/2026 | Sem defeito crítico aberto e evidências registradas | Filipe |
| Homologação funcional concluída | 04/11/2026 | Aceite funcional ou ajustes residuais aceitos | Danielle |
| Prontidão de produção | 06/11/2026 | Checklist, suporte, monitoramento e retorno aprovados | Alexandro e Fabrício |
| Go-Live do MVP | 09/11/2026 | Autorização executiva e implantação concluída | Marcelo |
| Encerramento da estabilização | 20/11/2026 | Operação estável e pendências transferidas ao backlog | Danielle e Fabrício |

## 4. Definições pendentes para fechar a linha de base

1. Confirmar o que foi concluído, iniciado ou bloqueado desde a reunião prevista para 15/09/2026.
2. Confirmar se o desenvolvimento efetivamente começou em 17/09/2026 e qual é o percentual real por frente.
3. Informar o nome, o papel e a disponibilidade do possível novo integrante.
4. Confirmar os donos dos canais, do Data Lake, da infraestrutura e do relacionamento com o Reclame Aqui.
5. Confirmar custos, contratações e restrições de calendário da equipe.
6. Validar se 09/11/2026 é uma data viável para Go-Live ou se há uma data de negócio obrigatória.

## 5. Regra de atualização

- Cada atividade deve ter apenas um responsável principal.
- Apoio e aprovação não substituem a responsabilidade pela entrega.
- Toda conclusão deve apontar para uma evidência verificável.
- Bloqueios devem registrar causa, dono da resolução, próxima ação e nova previsão.
- Mudanças de prazo ou escopo aprovadas devem ser refletidas em `projeto.md`, `tarefas.md`, `decisoes.md` e `historico.md`.
