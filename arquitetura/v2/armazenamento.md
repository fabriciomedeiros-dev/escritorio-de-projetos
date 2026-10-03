# Avaliação de armazenamento operacional — versão 2

Data da avaliação: 2026-10-03. Fontes oficiais consultadas nessa data. Escopo: escolher a base da primeira versão, preservando documentos e independência de agente. Não houve criação de conta, contratação, migração ou acesso a dados externos nesta avaliação.

## Escolha técnica e fundamento

Escolha técnica desta etapa: PostgreSQL central para dados operacionais, acessado por um serviço do Escritório, com documentos e evidências em armazenamento central de arquivos. Fabrício confirmou que precisa acessar de computadores diferentes desde o início. SQLite foi avaliado e ensaiado, mas não foi escolhido para o modo operacional inicial.

A escolha não implica contratação nem implantação. Hospedagem gerenciada ou interna, versão suportada do motor, destino dos arquivos e da cópia independente continuam pendentes. Não presumir autorização para hospedar dados profissionais externamente.

Nenhuma das alternativas, sozinha, implementa as regras do gestor. Aprovação de reunião, evidência de conclusão, histórico de negócio e identidade do executor precisam ser implementados e testados. Portabilidade pertence ao contrato de operações e à exportação, não apenas ao banco escolhido.

## Comparação

A avaliação de adequação abaixo é julgamento de arquitetura, baseado nos requisitos aprovados e nas capacidades documentadas; não é benchmark nem prova de ausência de recursos em produtos comerciais.

| Critério | Markdown + Git | Trello | Notion | SQLite + operações próprias | PostgreSQL + operações próprias |
|---|---|---|---|---|---|
| Modelo de tarefas, dependências e aprovações | Exige convenções e validadores; dados dispersos | Cartões e ações exigem adaptação ao modelo | Propriedades e relações mais próximas do modelo; exige adaptação | Esquema explícito, relações e restrições | Esquema explícito, relações e restrições |
| Atualização atômica de estado e histórico próprio | Exige mecanismo de gravação do conjunto de arquivos | Não demonstrada para nosso conjunto de objetos; tratar como lacuna | Não demonstrada para nosso conjunto de objetos; tratar como lacuna | Transação implementada no núcleo | Transação implementada no núcleo |
| Repetição e conflito de versão | Camada própria | Adaptador com reconciliação | Adaptador com reconciliação | Chave única e comparação de versão | Chave única e comparação de versão |
| Interface pronta para equipe | Não | Sim, quadro | Sim, páginas e bases | Precisa construir ou integrar | Precisa construir ou integrar |
| Isolamento | Separação de arquivos e controle de acesso | Configuração de quadros e permissões + controle no adaptador | Configuração de acesso + controle no adaptador | Serviço e relações por portfólio; sem autenticação de usuário embutida | Serviço e relações por portfólio; políticas de linha possíveis |
| Recuperação completa | Git cobre somente arquivos incluídos e enviados; anexos externos precisam de cópia | Coletar cartões, ações paginadas e arquivos; restaurar vínculos exige rotina própria | Coletar propriedades, conteúdo, relações paginadas e arquivos; restaurar vínculos exige rotina própria | Snapshot + arquivos + manifesto, com teste próprio | Dump/snapshot + arquivos + manifesto, com teste próprio |
| Independência de agente | Boa com operações portáveis | API acessível por adaptadores | API acessível por adaptadores | Boa com contrato separado do cliente | Boa com contrato separado do cliente |
| Administração inicial | Baixa; manutenção manual cresce | Integração, permissões, limites e cópias externas | Integração, permissões, limites e cópias externas | Baixa no piloto local; exige desenvolvimento | Serviço de banco, credenciais, atualizações, monitoramento e cópias |
| Uso entre computadores | Git não resolve gravação concorrente nem cópia completa por si só | Serviço central | Serviço central | Serviço central possível; não compartilhar arquivo ativo | Desenhado para uso cliente/servidor |

## Evidências oficiais

### SQLite

A documentação caracteriza SQLite como armazenamento local simples e permite uso atrás de um servidor de aplicação. Existe um escritor por vez; compartilhar o arquivo diretamente entre computadores por filesystem de rede é desaconselhado. Isso favorece um piloto individual e não impede três usuários atrás de um único serviço. [Usos apropriados](https://sqlite.org/whentouse.html).

A API de backup gera um snapshot consistente da base ativa. Banco e arquivos precisam compor uma exportação coordenada; copiar apenas o arquivo ativo não é o procedimento de backup definido aqui. [Backup](https://sqlite.org/backup.html).

### PostgreSQL

Transações agrupam mudanças em uma unidade atômica; políticas de linha podem reforçar isolamento. Superusuários e determinados papéis contornam essas políticas, portanto credenciais da aplicação e da cópia precisam ser distintas e verificadas. [Transações](https://www.postgresql.org/docs/current/tutorial-transactions.html), [segurança por linha](https://www.postgresql.org/docs/current/ddl-rowsecurity.html).

Dump e restauração são mecanismos disponíveis, mas não incluem automaticamente os arquivos externos da aplicação. [Dump SQL](https://www.postgresql.org/docs/current/backup-dump.html).

### Trello

O modelo documentado é baseado em quadros, listas, cartões e ações, com API e webhooks. Ações e coleções extensas exigem paginação; a leitura de uma única página não prova captura completa. A nossa conclusão de que dependências e aprovações exigem adaptação deriva da diferença entre esse modelo e o modelo do Escritório. [Introdução à API](https://developer.atlassian.com/cloud/trello/guides/rest-api/api-introduction/).

Há endpoints próprios para anexos e comentários. Exportar só títulos e descrições não satisfaz nossa recuperação de evidências. [Cartões e anexos](https://developer.atlassian.com/cloud/trello/rest/api-group-cards/).

### Notion

Bases oferecem propriedades e relações. Recuperar uma página não recupera seu conteúdo; conteúdo exige consulta de blocos. Relações extensas podem vir incompletas na resposta da página, exigindo paginação específica. [Propriedades](https://developers.notion.com/reference/property-object), [recuperação de página](https://developers.notion.com/reference/retrieve-a-page).

A API documenta limites de requisição e falhas nas quais a gravação já ocorreu apesar da resposta de erro. Uma integração precisa verificar antes de repetir. [Limites e repetição de requisições](https://developers.notion.com/reference/request-limits). Originais precisam ser coletados e verificados junto dos dados. [Arquivos e mídia](https://developers.notion.com/guides/data-apis/working-with-files-and-media).

Não foi feita prova de restauração real nem de histórico completo por API no Trello ou Notion. Essas lacunas não significam impossibilidade, mas impedem tratar tais soluções como já aprovadas nos critérios eliminatórios.

## Custos e manutenção

SQLite não exige servidor de banco separado no piloto. PostgreSQL implica administrar um serviço ou contratar hospedagem. Os motores têm licenças permissivas; não é necessário adquirir uma licença paga do motor para esse desenho. [SQLite](https://sqlite.org/copyright.html), [PostgreSQL](https://www.postgresql.org/about/licence/).

Isso não torna uma aplicação própria gratuita: desenvolvimento, suporte, autenticação futura, armazenamento de arquivos e proteção independente têm custo. SaaS reduz o trabalho da interface, mas mantém custos de integração, governança e recuperação. Preços de planos não foram cotados, pois não há contratação proposta nem necessidade de escolher um plano nesta etapa. Levantar preços e custo total antes de contratar qualquer serviço.

## Prova prática

Script reproduzível: [experimentos/validar_sqlite.py](experimentos/validar_sqlite.py). Execução local em Python 3.14.3 / SQLite 3.51.2. Todos os dados são sintéticos e criados em pasta temporária.

Verificado: operação repetida não duplica registros; falha reverte o lote; relação de outro portfólio é rejeitada; versão antiga não sobrescreve estado novo; snapshot é restaurável em nova pasta; histórico e evidência são recuperados; alteração do anexo é detectada por checksum. O experimento passa sem dependências adicionais.

Limites: não é implementação operacional nem prova de autenticação, autorização, conclusão por evidência, cópia externa, concorrência intensa, durabilidade após queda de energia ou migração de registros reais. A pasta restaurada está no mesmo dispositivo; não constitui proteção independente. Notion e Trello não foram testados praticamente. O piloto completo continua obrigatório.

### Ensaio PostgreSQL

Script reproduzível: [experimentos/validar_postgresql.py](experimentos/validar_postgresql.py). Executado com os binários locais PostgreSQL 14.20 já disponíveis, em cluster temporário isolado, com somente socket local e sem conexão a banco existente. O cluster foi encerrado e removido ao final. A versão instalada serviu ao ensaio; a versão de produção ainda será escolhida entre versões suportadas.

Passou: transação com rollback, restrição única para chave de operação, relação composta por portfólio, rejeição de atualização com versão obsoleta, dump e restauração em outra base, recuperação de histórico e metadados de anexo, verificação de manifesto e detecção de alteração de arquivo. A chave única é um mecanismo necessário, mas ainda não prova todo o fluxo de repetição do serviço.

Não valida autenticação da equipe, políticas de linha, hospedagem, durabilidade após queda de energia ou cópia externa. Os arquivos do pacote ficaram no mesmo dispositivo; a restauração validou banco e referência/checksum do arquivo, não um plano de desastre em infraestrutura independente.

## Desenho recomendado para a base própria

1. Dados operacionais em esquema relacional; histórico, aprovações e operações gravados na mesma transação quando aplicável.
2. Arquivos originais em armazenamento persistente por portfólio, com ID, versão imutável, caminho relativo e checksum. Markdown permanece documentação; visões derivadas recebem fonte e data.
3. Serviço central autenticado expõe contrato versionado e verifica regras antes da gravação. Clientes Codex, Claude Code e futuros formulários usam API, com adaptadores CLI/MCP quando necessário. O agente não recebe acesso SQL irrestrito como fluxo normal. Cada identidade só acessa os portfólios e operações autorizados. Credenciais do banco ficam no serviço, fora dos documentos e chats.
4. Importação de anexos usa preparação, verificação e confirmação com recuperação de falha parcial. Banco e filesystem não formam uma transação única automaticamente.
5. Banco ativo não é sincronizado por Git, pasta de nuvem ou compartilhamento entre máquinas. Versionar código, esquema, migrações e documentação; manter snapshots consistentes e cópias independentes separadas.
6. Exportação inclui banco/snapshot, representação aberta dos registros, Markdown necessário, originais, vínculos e manifesto. Restauração verifica completude e integridade, inclusive propostas pendentes.
7. Proteção independente exige destino escolhido, retenção e teste de recuperação. Até sua configuração, mostrar proteção pendente; nenhuma garantia de perda zero.

## Alternativas e revisão futura

SQLite atenderia um piloto local ou um serviço pequeno em host único. Não foi descartado por incapacidade de atender três usuários; PostgreSQL foi preferido como base central desde o início, com evolução da equipe e serviço independente dos clientes. A decisão é arquitetural, não resultado de benchmark. Revisá-la somente se os requisitos de implantação mudarem.

Trello pode continuar como divulgação e Notion como interface/documentação complementar, somente com autoridade claramente definida e sem estado oficial duplicado. Não construir integração bidirecional antes de validar o núcleo.

## Próxima entrega

Comparar hospedagem interna e gerenciada conforme a preferência de Fabrício. Definir banco, serviço autenticado, arquivos e cópia independente, custos e responsabilidade de operação. Depois criar esquema físico e operações mínimas. Não migrar registros atuais antes do ensaio de migração e do corte de autoridade.
