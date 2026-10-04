# Escritório de Projetos IA — versão 2

Data: 2026-10-03. Situação: desenho funcional aprovado por Fabrício nesta sessão; especificação documentada, implementação pendente.

A versão 2 amplia a gestão para ideias, solicitações pontuais, projetos e tarefas. Um agente gestor acompanha o trabalho; o conselho existente prepara ideias antes da promoção humana a projeto. Os papéis do conselho não são agentes operacionais de gestão.

Codex será o cliente inicial, mas a estrutura é agnóstica: Claude Code ou outro agente deve acessar a mesma fonte por operações portáveis, sem migração de memória nem dependência do histórico dos chats.

## Documentos

- [Operação portável do gestor no piloto](operacao-gestor.md)

- [Acesso técnico pelo chat conforme autorização](seguranca-chat.md)

- [Especificação funcional e arquitetura](especificacao.md)
- [Modelo lógico de dados](modelo-dados.md)
- [Interação agnóstica, Codex inicial e colaboração futura](interacao.md)
- [Plano de implementação e validação](plano.md)
- [Comparação e escolha de armazenamento operacional](armazenamento.md)
- [Comparação de hospedagem e custos](hospedagem.md)
- [Preparação e passagem para implementação no SuperSync](implementacao-supersync.md)
- [Ambiente local de testes](../../desenvolvimento/local/README.md)
- [Esquema PostgreSQL e migração inicial](../../desenvolvimento/migrations/README.md)
- [Contrato das operações](../../desenvolvimento/contratos/README.md)
- [Serviço mínimo local e cliente de referência](../../desenvolvimento/servico/README.md)

## Autoridade e transição

Esta pasta é a fonte do desenho da versão 2, não uma base operacional implantada. Os registros existentes continuam oficiais durante a transição. Nenhum prazo, status ou aprovação de projetos existentes é alterado por esta especificação.

Na arquitetura alvo, cada campo operacional terá uma única fonte estruturada oficial; Markdown e arquivos continuam preservando documentação, decisões explicadas e evidências. Visões operacionais em Markdown serão geradas a partir da fonte oficial e identificadas como derivadas. Requisitos e documentação técnica continuam nos repositórios indicados por cada projeto.

A [avaliação de armazenamento](armazenamento.md) escolhe PostgreSQL central com serviço próprio e armazenamento de arquivos, diante do requisito de acesso por vários computadores desde o início. Hospedagem e implantação ainda estão pendentes. Trello e Notion podem ser interfaces complementares, sem duplicar a fonte oficial. A migração exige inventário, conciliação, teste de restauração e declaração explícita do corte de autoridade por conjunto de dados; não haverá duas fontes oficiais concorrentes.

## Identificação da versão

O arquivo raiz `VERSION` identifica esta linha como `2.0.0`. A versão identifica a arquitetura e a documentação do Escritório; não significa que o agente gestor já esteja implementado. O commit desta etapa deve mencionar explicitamente a versão 2. Não há publicação, implantação ou envio externo nesta etapa.
