# Ficha de ideia — Escritório de Projetos IA v2

**ID:** SAERJ-IDEIA-002

**Portfólio pretendido:** saerj, pela relação com equipe e infraestrutura SuperSync

**Estado:** Em estruturação; candidata a projeto, sem promoção

**Proponente:** Fabrício Medeiros

**Entrada e atualização:** 03/10/2026

## Ideia original e problema

Criar auxiliar de gestão de projetos, solicitações e tarefas, com registro de atividades, recuperação de documentação e evidências, planejamento semanal, capacidade e relatórios. Demandas pontuais, projetos futuros e tarefas se acumulam e misturam; a dificuldade central relatada é recuperar informação confiável.

Fabrício confirmou o desenho funcional da v2 e autorizou iniciar a sequência de preparação. Nesta sessão informou que o servidor do SuperSync já possui PostgreSQL, pode receber interfaces com controle de usuários e que deseja validar ambiente local antes de mudanças remotas, a serem implementadas por outra pessoa. Indicou que isso pode se tornar projeto; não autorizou promoção.

## Objetivo e resultados

Primeiro validar o fluxo de um gestor via Codex, preservando portabilidade para outros agentes; depois permitir participação direta de duas pessoas. Recuperar status e fontes, distinguir avanço parcial de entrega completa e sinalizar conflitos de capacidade.

Critérios iniciais: captura recuperável com fontes; aprovação de todos os tópicos de reuniões; conclusão com evidência; consulta em novo chat/cliente; dependências e capacidade explícitas; restauração de registros e arquivos. Linha de base de tempo perdido, frequência de consultas e ganhos: a medir, sem valores presumidos.

## Possibilidades avaliadas

- Manter Markdown/Git como operação: preserva documentação, mas não resolve bem a dispersão operacional relatada.
- Trello/Notion: interfaces possíveis, com controles e recuperação próprios necessários.
- Base própria: PostgreSQL central escolhido para acesso entre computadores; arquivos e contrato do Escritório separados do agente.
- Hospedagem gerenciada: comparação preparada; Supabase era a recomendação antes da informação do servidor existente, sem contratação.
- Aproveitar SuperSync: nova direção prioritária de avaliação, com banco/serviço próprios e identidade/interface compartilháveis.
- Experimento local: infraestrutura PostgreSQL preparada; aplicação e integração ainda pendentes.

## Requisitos e restrições

A fonte funcional detalhada é a [arquitetura v2](../../../../arquitetura/v2/README.md); esta ficha referencia suas decisões sem manter outra especificação concorrente. Dados profissionais e pessoais separados; não mover portfólio pessoal para servidor corporativo sem decisão específica. Ambiente local sem credenciais/dados de produção. Serviço agnóstico, evidências persistentes e proteção independente.

## Riscos e lacunas

Capacidade e versão do servidor desconhecidas; integração de identidade ainda não inspecionada; banco próprio versus schema pendente. Dependência de outro implementador sem nome/prazo confirmado. Compartilhamento de infraestrutura pode afetar consumidores existentes, exigindo análise e homologação. Restauração real e migração permanecem pendentes.

## Próximos passos e portão

Continuar preparação técnica local e passagem conforme [roteiro SuperSync](../../../../arquitetura/v2/implementacao-supersync.md). Definir responsável total, executor, repositório, esforço e meta; preparar TAP antes de submissão à diretoria. O TAP e o Canvas ainda não foram produzidos; a aprovação do desenho v2 não aprova automaticamente os portões do conselho.

**Decisão de promoção:** não registrada. **Saúde de projeto:** não se aplica. Esta ideia não integra o relatório de projetos ativos. A preparação solicitada não autoriza alteração no SuperSync.
