# Implementação com infraestrutura do SuperSync — versão 2

Data: 03/10/2026. Direção de avaliação solicitada por Fabrício: aproveitar servidor existente com PostgreSQL e possibilidade de interfaces/controle de usuários no SuperSync, testando localmente antes de qualquer alteração remota. Outra pessoa fará a implementação; nome, aceite, disponibilidade e prazo ainda não definidos.

## Fatos e limites

- Confirmado por relato de Fabrício: há servidor do SuperSync com PostgreSQL; interfaces e controle de usuários podem ser implementados ali. Não houve inspeção do servidor nem do código nesta etapa.
- O repositório registra o SuperSync no portfólio SAERJ e descreve gestão de usuários/autenticação como serviço compartilhado para o SAC. Isso demonstra a direção arquitetural existente, não compatibilidade já validada para o Escritório.
- A arquitetura v2 e a preparação local estão autorizadas. A iniciativa foi capturada como candidata a projeto em [SAERJ-IDEIA-002](../../conselho/ideias/saerj/escritorio-projetos-ia-v2/01-ficha-ideia.md); não há promoção explícita nem autorização de implantação.
- Não foi alterado servidor, repositório de código, tabelas, usuários ou escopo do SuperSync. Não foi enviada mensagem ao implementador.

## Fronteiras propostas

O Escritório mantém gestão, escopo, documentação, responsável total e aceites próprios. SuperSync pode prover hospedagem, identidade e interface. Reutilizar infraestrutura não transforma a documentação do Escritório em um módulo exclusivamente acessível por SuperSync.

Preferência: banco lógico próprio para o Escritório na instância PostgreSQL existente, se capacidade e política permitirem; alternativa é schema dedicado com papéis restritos, a justificar. Nenhuma tabela operacional deve ser misturada às tabelas atuais sem definição de autoridade. Contrato próprio e versionado atende Codex, Claude Code e interface web. Clientes não recebem acesso SQL administrativo.

A identidade do SuperSync será mapeada para uma identidade estável do Escritório, com autorização por portfólio e operação. Administrador técnico, gerente e executor são papéis diferentes. Autenticação do SuperSync não implica automaticamente acesso a todos os dados do Escritório.

Portfólio pessoal permanece fora do servidor corporativo por padrão; sua eventual hospedagem exige decisão específica. Os ensaios locais de separação podem usar dados sintéticos de dois portfólios. Não migrar documentos pessoais para infraestrutura SAERJ apenas porque o modelo suporta múltiplos domínios.

Arquivos originais precisam de armazenamento persistente e recuperável, com permissões, versões, IDs e checksum. O host existente não comprova que isso já exista. Banco e anexos precisam de proteção fora do host principal e procedimento de restauração coordenado.

## Material de passagem ao implementador

| Item | Fonte / ação |
|---|---|
| Regras e escopo funcional | [Especificação v2](especificacao.md) |
| Entidades, estados e integridade | [Modelo de dados](modelo-dados.md) e [schema aplicado localmente](../../desenvolvimento/migrations/README.md) |
| Operações agnósticas do cliente | [Contrato e OpenAPI](../../desenvolvimento/contratos/README.md) — serviço mínimo local implementado; demais comandos pendentes |
| Interação inicial e futura equipe | [Interação](interacao.md) |
| Critérios de validação | [Plano](plano.md) |
| Serviço mínimo HTTP e cliente de referência | [Piloto local](../../desenvolvimento/servico/README.md), sem integração SuperSync |
| Ambiente local inicializado | [Comandos e limites](../../desenvolvimento/local/README.md) |
| Prova sintética de recuperação | [Ensaio PostgreSQL](experimentos/validar_postgresql.py) |
| Dependência de serviços | [Serviços compartilhados SuperSync](../../portfolios/saerj/projetos/supersync/servicos-compartilhados.md) |

## Sequência de implementação proposta

1. Preparar esquema físico e migrations versionadas, contrato de operações e casos sintéticos; definir repositório de código/documentação com o implementador. Os scripts locais deste repositório são preparação, não definição do runtime final.
2. Implementar e validar localmente captura, repetição, consulta, autoria, artefatos, aprovação de reuniões, conclusão e bloqueios. Incluir perfis limitados e comparação de versão. Não usar serviço de autenticação de produção durante ensaio local; usar identidades de teste claramente identificadas.
3. Levantar SuperSync por acesso autorizado: versão PostgreSQL, stack, forma de autenticação, organização de usuários/perfis, capacidade, arquivos, backup, rede, ambientes e processo de publicação. Registrar evidências e lacunas; não adivinhar rotas ou tabelas de autenticação.
4. Definir integração e estimar esforço com o implementador, incluindo impacto nos consumidores atuais. Identificar dono provedor e consumidor; validar responsável total e critérios de aceite.
5. Após decisão de projeto/experimento e autorização de mudança, preparar homologação separada. Migrations não podem ser aplicadas implicitamente pelo chat ou ambiente local.
6. Validar acesso de dois clientes, interface de executor, isolamento, gravação de evidências, conflitos, indisponibilidade e restauração de banco/arquivos em destino novo.
7. Submeter plano de implantação com janela, backup prévio, reversão, credenciais próprias e monitoramento. Somente após aceites e autorizações aplicáveis executar produção.
8. Migrar dados selecionados com conciliação, preservando IDs e fontes; declarar corte de autoridade. Estado atual em Markdown continua oficial até esse marco.

## Pendências

- Nome/aceite do implementador e responsável total pela futura entrega; Fabrício é proponente e decisor da preparação, não designação automática de executor.
- Versão e capacidade reais do PostgreSQL/SuperSync; versão local disponível é 14.20, não homologada como versão final.
- Repositório de desenvolvimento e documentação funcional do Escritório; relação com o código SuperSync a decidir.
- Banco próprio versus schema, interfaces de autenticação, papéis e regras de acesso; sem dependência de comando específico de agente.
- Armazenamento de anexos, destino independente de cópia, frequência e retenção.
- Estimativa do executor, capacidade, meta desejada e previsões; nenhuma data de entrega foi inventada.
- Promoção formal como projeto, ou decisão de experimento, conforme governança existente.
