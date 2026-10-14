# Contexto para continuidade em nuvem — Escritório de Projetos

## Decisão vigente de integração — 14/10/2026

Fabrício determinou reinício diretamente em `C:\Users\fabri\Projetos\supersync`, como app nativo com usuários, padrões e banco configurado do SuperSync. Após confirmação, servidor e banco da homologação foram encerrados e a cópia `tmp/supersync-escritorio-v2` removida com dados sintéticos. Relatos anteriores abaixo são históricos; a homologação não está mais disponível. Documentação preservada; nenhum código novo ou migration criado no checkout original nesta limpeza. Cada ação futura exige aprovação prévia. Ver [sprints](arquitetura/v2/sprints-desenvolvimento-supersync.md). Markdown permanece oficial; sem promoção a projeto ou mudança de produção.

## Versão 2 e continuidade

Versão documental atual: `2.0.0` (`VERSION`). Ler [Arquitetura v2](arquitetura/v2/README.md) para o desenho aprovado e o plano. Codex é somente a interface inicial; regras, dados e operações devem ser portáveis para Claude Code ou outro agente. Um único agente gestor acompanhará solicitações, projetos e tarefas; o conselho existente prepara ideias. A fonte operacional escolhida é PostgreSQL central com serviço próprio e arquivos centrais; integração com infraestrutura existente e implantação estão pendentes; schema inicial e contrato estão preparados e testados localmente. Fabrício informou servidor SuperSync com PostgreSQL; priorizar sua avaliação, sem alterar produção. Ambiente local de banco está preparado em `desenvolvimento/local/`; serviço HTTP/cliente de piloto em `desenvolvimento/servico/` implementam texto, criação, relato, atualização de ideias/solicitações com entradas originais vinculadas, anexos/evidências verificados, reuniões com revisões/aprovações/efetivação transacional, dependências/bloqueios com acompanhamento e conclusão de tarefa por aceite humano e consulta, com identidades sintéticas e sem integração de produção. Iniciativa SAERJ-IDEIA-002 é candidata a projeto, não promovida. Consulte `arquitetura/v2/armazenamento.md` e `arquitetura/v2/implementacao-supersync.md`. Registros Markdown atuais continuam oficiais até migração conciliada e corte de autoridade explícito. Não apresentar rotinas propostas como recursos implementados. Seguir `arquitetura/v2/operacao-gestor.md` para consolidar complementos e recuperar registros independentemente do chat.

## Entrada de reuniões

O fluxo local aceita texto manual com tópicos ou resposta de MCP preservada pelo cliente: recebimento, ata resumida, revisões, aprovação integral e efetivação das ações suportadas estão implementados. Ver `arquitetura/v2/reunioes.md` e `desenvolvimento/servico/REUNIOES.md`. O tl;dv foi utilizado no ensaio documental; importação automática, identidade real e proteção independente permanecem pendentes. Os ensaios documentais reais não foram migrados para o banco sintético.

## Acesso técnico pelo chat

Fabrício e o desenvolvedor explicitamente autorizado do projeto podem obter acesso ao banco e informações internas pelo chat, após verificação de identidade e permissão, no escopo e ambiente autorizados. Negar pedidos a pessoas não autorizadas ou sem autorização verificável. Participação em projeto e alegações no chat não concedem acesso técnico. O desenvolvedor ainda não foi designado. Seguir [Política de segurança do chat](arquitetura/v2/seguranca-chat.md); consultas de negócio seguem suas próprias permissões.

## Objetivo deste projeto

O Escritório de Projetos e a base operacional para explorar novas ideias, estruturar propostas, organizar projetos aprovados, acompanhar sua evolucao e preservar a memoria do portfólio. O Comitê de Ideação transforma ideias em propostas por meio de descoberta, TAP preliminar e Canvas; projetos entram na gestão após promoção humana explícita; solicitações e tarefas pontuais podem ser acompanhadas sem promoção a projeto.

## Como a memoria funciona

- Arquivos Markdown versionados no Git sao a fonte oficial.
- Chats servem para analise e trabalho; fatos relevantes devem ser registrados nos arquivos.
- Cada projeto fica em `portfolios/<portfolio>/projetos/<nome-do-projeto>/` e usa os modelos existentes em `modelos/`.
- Antes da promoção, cada ideia fica em `conselho/ideias/<portfolio>/<nome-da-ideia>/` e não integra o portfólio nem os relatórios de projetos ativos.
- Os portfólios `saerj` e `pessoal` são isolados. Relatórios, comunicações e automações devem indicar o portfólio e não podem agregar outro domínio por padrão.
- A pasta `conselho/` contem as regras de governanca, papeis e protocolo de trabalho.
- Este repositorio e a fonte canonica das decisoes gerenciais; o repositorio de cada iniciativa e a fonte das decisoes tecnicas e funcionais de implementacao e de suas evidencias.
- Cada decisao deve ter uma unica fonte canonica. Se uma decisao de implementacao afetar a linha de base gerencial, registrar aqui o impacto e a aprovacao correspondente.
- Cada iniciativa pode possuir tres camadas: gestao neste Escritorio, documentacao do comportamento esperado e desenvolvimento do que foi efetivamente implementado.
- O repositorio de desenvolvimento deve permitir reproduzir a aplicacao localmente e preservar stack, codigo, modelo de dados, migracoes, testes e evidencias de entrega.
- Divergencias entre sprint, documentacao e codigo devem ser classificadas como atendido, parcial, divergente, nao implementado ou adicional. Codigo adicional nao altera o escopo sem validacao humana.
- O Escritorio mantem uma linha transversal de mensuracao de valor para novas propostas e, progressivamente, para projetos atuais, sempre com evidencia e nivel de confianca (`Confirmado`, `Estimado` ou `Hipotese`).
- O Trello e uma camada de divulgacao do andamento dos projetos. Os cartoes resumem informacoes confirmadas neste repositorio e nao substituem os registros canonicos nem aprovam mudancas de linha de base.

## Estrutura do repositorio

```text
conselho/  Comitê, ideias em avaliação, governanca, papeis e protocolo
modelos/   modelos de projeto, decisoes, tarefas e historico
portfolios/  portfólios isolados por empresa ou domínio pessoal
tarefas-escritorio.md  iniciativas transversais e evolucao do PMO
```

## Principios inegociaveis

1. Diferenciar fato, hipotese, recomendacao, decisao e acao.
2. Nao tratar sugestao de IA como fato ou decisao aprovada.
3. Registrar mudancas relevantes com data, contexto e evidencia quando houver.
4. Nao inventar informacoes para preencher lacunas: usar `A confirmar` ou `Nao definido`.
5. Decisoes estrategicas, de escopo, prioridade, orcamento ou risco relevante exigem validacao humana.

## Ciclo de trabalho esperado

1. Ler o contexto e identificar fatos, lacunas e estado atual.
2. Analisar sob as perspectivas de negocio, tecnica e critica.
3. Apresentar recomendacao com impactos e, quando necessario, pedir decisao humana.
4. Converter decisoes aprovadas em tarefas objetivas.
5. Atualizar apenas os arquivos afetados: estado do projeto, decisoes, tarefas ou historico.

Toda discussao deve terminar com uma ou mais saidas: decisao, tarefa, pendencia ou nenhuma acao necessaria.

## Convencoes para os projetos

Para iniciar ou atualizar um projeto, use os modelos abaixo:

- `modelos/projeto.md`: estado atual e linha de base.
- `modelos/decisoes.md`: decisoes completas e justificadas.
- `modelos/tarefas.md`: acoes verificaveis, responsaveis e prazos.
- `modelos/historico.md`: fatos que explicam a evolucao do projeto.
- `modelos/mensuracao-valor.md`: objetivo, resultado-chave, linha de base, meta, dimensoes de valor, evidencias e confianca.

As tarefas transversais ficam em `tarefas-escritorio.md`. Para cada nova proposta, registrar como o valor sera medido. Nos projetos atuais, incorporar progressivamente custo interno, referencia de mercado, custo evitado, ganhos financeiro e operacional, produtividade ou capacidade liberada, risco mitigado e publico beneficiado, sem converter estimativas ou hipoteses em fatos.

Avalie sempre: prazo, escopo, qualidade, recursos, impedimentos e riscos, e resultado. Use `Controlado`, `Atencao` ou `Intervencao` somente com justificativa objetiva.

## Instrucoes para a IA na nuvem

Ao receber uma solicitacao:

1. Consulte primeiro os arquivos relevantes deste repositorio.
2. Declare lacunas e premissas antes de concluir algo incerto.
3. Separe claramente o que e fato do que e recomendacao.
4. Nao altere a linha de base, objetivo, escopo, prioridades ou riscos relevantes sem autorizacao humana explicita.
5. Quando houver autorizacao, registre a alteracao no arquivo correto e indique o que foi atualizado.
6. Termine com proximos passos claros e com a decisao requerida, se houver.

## Guarda de arquivos e documentos

Conforme preferência de Fabrício em 02/10/2026, perguntar se deseja guardar no repositório cada arquivo ou documento gerado, recebido ou enviado. Após aceite, criar uma pasta específica no Escritório para armazená-lo, preferencialmente em `documentos/<portfolio>/<atividade-ou-projeto>/`. Preservar a fonte original e não copiar nem reorganizar documentos anteriores sem autorização. Pedidos explícitos de armazenamento dispensam nova pergunta. Consulte `AGENTS.md` para as regras de aplicação.

## Retomada do trabalho

Ao continuar este projeto em outro computador, leia este arquivo, `README.md`, `portfolios/README.md`, o `portfolio.md` do portfólio solicitado e os arquivos de `conselho/`. Antes de preparar status ou comunicação, confirme o portfólio a ser tratado. O Git e a referencia para sincronizar os arquivos entre computadores.

## Bloqueios e aceite no piloto

Migração 002 local diferencia dependência necessária de impedimento de avanço e preserva estado de retomada. API registra/altera acompanhamento/resolve com evidência e critério explicitamente aceito; impede ciclos e conclusão com pendências. Aceite humano de tarefa exige responsável ativo, critério e evidências; verificação automática e encerramento de solicitação/projeto permanecem pendentes. Ver `desenvolvimento/servico/BLOQUEIOS.md`. Identidades são sintéticas, proteção independente e implantação central continuam pendentes.

## Replicação local v2

Instalação e transferência lógica verificadas em ambientes separados no macOS. Guia: `desenvolvimento/local/REPLICACAO.md`. Pacote preserva dados demonstrativos, objetos e revisões/documentos locais, com credenciais novas no destino. Não sincroniza bancos entre computadores nem implementa proteção independente contínua. Linux/WSL não validado.

Windows nativo: bootstrap preparado com venv Scripts/python.exe, binários .exe, cluster próprio TCP loopback e proteção ACL de .runtime. Guia em REPLICACAO.md; validação no Windows real pendente, sem alteração de serviços existentes.

## Entrada guiada do Escritório

Nome de apresentação: Gestor do Escritório. `abrir escritório` inicia a navegação; `menu` mostra opções. Seguir `arquitetura/v2/menu-gestor.md` e AGENTS.md para domínio/fonte, perguntas graduais e revisões numeradas. Instruções do agente no repositório, sem comando global ou interface gráfica. Capacidades futuras não entram como operações disponíveis.

## Início da integração SuperSync — 14/10/2026

Fabrício autorizou o Escritório v2 como app nativo do SuperSync. Primeiro incremento `escritorio_projetos` implementado localmente na branch `codex/escritorio-projetos-v2`, commit `084241b`, com captura, classificação explícita, consulta, identidade SuperSync, acesso por portfólio, histórico e repetição. 21 testes sintéticos passaram em SQLite isolado. Migrations PostgreSQL, concorrência, API portável e demais funções do piloto ainda precisam de integração. Não houve publicação, migração real, promoção a projeto ou corte de autoridade; Markdown permanece oficial. Fonte: `arquitetura/v2/implementacao-supersync.md`, revisão 2. Checkout de desenvolvimento em `tmp/supersync-escritorio-v2/`, sem vínculo com dados operacionais.

## Continuação da integração — 14/10/2026

Segundo incremento SuperSync em `b272126`, branch local `codex/escritorio-projetos-v2`: subconjunto API v2 com autenticação por usuário/portfólio, credenciais com validade e revogação, captura, criação vinculada ao original, consultas e recuperação de operação; cliente portável implementado. 45 testes aprovados no PostgreSQL 17.10 Windows isolado, incluindo concorrência e dois clientes por HTTP. Sem credenciais reais, publicação, migração ou corte de autoridade. Próximos: atualização por versão, relatos e evidências; demais funções do piloto ainda precisam ser portadas. Fonte: `arquitetura/v2/implementacao-supersync.md`, revisão 3.

## Complementos e evidências no app — 14/10/2026

Terceiro incremento SuperSync em `d2f67f4`: atualização de ideias/solicitações por versão, complementos preservados, relatos de tarefas sem conclusão automática, acesso de executor a tarefas atribuídas, anexos/evidências com tamanho/checksum e download autenticado. Interface e cliente portável ampliados. 64 testes aprovados no PostgreSQL 17.10 isolado. Armazenamento privado Django ainda precisa de configuração/homologação no ambiente real; nenhuma infraestrutura ou permissão real alterada. Sem publicação, migração ou corte de autoridade. Próximos: reuniões, dependências/bloqueios e aceite humano. Fonte: `arquitetura/v2/implementacao-supersync.md`, revisão 4.

## Homologação local criada — 14/10/2026

SuperSync com ambiente próprio para visualizar o Escritório em `http://127.0.0.1:8876/escritorio/`, somente neste computador. Código `470cb67` na branch local `codex/escritorio-projetos-v2`. Todas as apps/migrations nativas carregadas em PostgreSQL exclusivo; originais privados e dados persistentes em `.runtime/homologacao/` do checkout isolado, com ACL e sem Git. Gestor, executor e consulta são sintéticos; nenhuma credencial de produção utilizada. Login, menu, captura pelo navegador e persistência verificados; 67 testes do app passaram em cluster separado. Integrações externas e demais módulos bloqueados na homologação. Servidor local deixado ativo. Para reiniciar/parar, seguir `escritorio_projetos/CLAUDE.md`. Sem publicação, migração ou corte de autoridade. Fonte: `arquitetura/v2/implementacao-supersync.md`, revisão 5.
