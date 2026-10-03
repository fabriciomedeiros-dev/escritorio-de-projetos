# Contrato de operações — Escritório v2

Versão 2.0.0, OpenAPI 3.1. [Contrato legível por máquina](openapi.json) e [pedidos ilustrativos](exemplos.json). Este contrato é uma proposta implementável, não um serviço disponível. Nenhum endereço de produção foi presumido.

## Identidade, isolamento e repetição

Bearer token identifica a pessoa por validação no serviço, com mapeamento do provedor SuperSync a `pessoas`/`identidades`. Não aceitar `ator`, papel ou portfólio permitido declarado pelo agente no corpo. Verificar membro ativo e permissão para comando e registro antes de consultar ou escrever; não revelar conteúdo de outro domínio. Credenciais administrativas ficam fora dos clientes.

Toda mutação exige portfólio na rota, UUID de operação e `Idempotency-Key`. Chave é única por portfólio e pessoa. Calcular hash do pedido canônico (incluindo comando e versão do contrato) no serviço. Repetição idêntica retorna o resultado conhecido; chave ou UUID reutilizado com conteúdo diferente retorna 409. Nunca sobrescrever o pedido original. Em falha de rede, consultar a operação antes de reenviar; 202 é pendência, não confirmação de registro.

Atualizações de registros exigem `versao_esperada`; executar comparação atômica na gravação. Em conflito retornar 409 e pedir nova leitura. Versão sobe uma unidade por alteração efetivada. Nova consulta não autoriza automaticamente trocar a meta ou prioridade.

## Semântica dos comandos

| Comando | Regra adicional obrigatória do serviço |
|---|---|
| capturar_entrada | Preservar origem e anexos; classificação sugerida é proposta; lacunas não bloqueiam captura |
| criar_registro | Criar no estado inicial, nunca concluído; projeto exige decisão explícita de promoção verificada; gerar ID estável sem colisão |
| registrar_relato | Separar remetente autenticado de autor informado; preservar relato e fontes; não concluir nem mudar meta implicitamente |
| registrar_dependencia | Verificar entrega e provedor, impedir ciclos; motivo, próxima ação, responsável e acompanhamento obrigatórios |
| resolver_dependencia | Conferir critério e evidência; liberar conclusão apenas quando todas as pendências necessárias estiverem resolvidas |
| preparar_artefato | Gerar chave interna; não aceitar URL remota/caminho arbitrário como arquivo já salvo; preparar upload persistente autorizado |
| verificar_artefato | Ler objeto salvo, calcular tamanho/checksum e comparar; cliente não pode declarar a verificação cumprida |
| propor_topicos_reuniao | Original verificado; apresentar todos os tópicos; revisões imutáveis, sem alterar operação do projeto |
| aprovar_topicos_reuniao | Gestor humano autenticado confirma cada revisão; correção cria revisão nova; itens rejeitados não são efetivados; lote explicitamente enviado é atômico |
| propor_prazo | Executor autorizado propõe; avaliar capacidade, dependências e meta. Sem dados suficientes não aceitar automaticamente. Conflito vira proposta para gestor |
| validar_conclusao | Examinar critério e evidências, dependências e subtarefas; `aceite_humano` exige ato humano autenticado. Modo enviado não é prova de autoridade |
| exportar_portfolio | Gerar pacote aberto com dados, originais, histórico, propostas, vínculos e manifesto; proteção independente tem estado próprio |

Comandos de alteração de meta, prioridade e responsável, promoção de ideias, planejamento de sprint, gestão de usuários e aprovação de prazo em conflito ainda não estão expostos nesta primeira revisão. Não simular essas funções via `registrar_relato`. Devem receber contratos próprios antes de serem oferecidos no menu.

## Transação e concorrência

Antes de qualquer escrita no portfólio, adquirir lock transacional de portfólio, por exemplo `pg_advisory_xact_lock` com chave estável determinada pelo serviço. Todos os escritores autorizados seguem esse protocolo, inclusive verificações de artefatos e dependências. Isso serializa alterações no piloto e evita duas transações aprovarem estados incompatíveis com as validações diferidas. Não conceder escrita direta ao agente. Escalabilidade e locks mais finos podem ser avaliados posteriormente com testes de concorrência.

Dentro da transação, reservar/verificar operação, validar permissões e pré-condições, gravar estado e histórico, aplicar aprovação exata uma vez e confirmar. Após commit, ler resultado e arquivos para verificar. A resposta `verificada` só é emitida após essa leitura. Se houver falha pós-commit, manter estado reconciliável por ID; não confirmar conclusão íntegra nem repetir efeitos.

Banco e objetos não compartilham transação automática. Preparar arquivo imutável, verificar, vincular e marcar estado; recuperação de falha parcial e coleta de objetos órfãos exigem rotina própria. Aprovação de lote sem efeito externo pode ser transacional; upload/exportação usam estado de progresso explícito.

## Consultas e respostas

Consulta paginada por ID, tipo, situação, assunto, origem e período. Resposta de registro deve incluir versão, responsável, prazo/meta, esforço restante, última atualização, evidências e documentos, dependências e lacunas. Esses campos do item de consulta ainda precisam de schema detalhado antes do cliente produtivo; o envelope e comandos já estão especificados.

A paginação deve ser estável, com cursor opaco e filtro autorizado por portfólio. Não há consolidação entre portfólios nesta API inicial. `404` cobre ausência e registro fora do escopo; erros não expõem documentos nem credenciais.

Persistência e proteção são separadas: `estado=verificada` significa gravação conferida; `protecao=pendente` significa que a cópia independente ainda não está confirmada. A validação do JSON não substitui os checks, autorização ou critérios semânticos do serviço.

## Mapeamento e limites

Rotas e nomes não dependem de Codex, Claude Code ou formato de chats. Adaptadores CLI/MCP e interface SuperSync usam o mesmo contrato. Mudanças incompatíveis precisam de versão de API nova; migrações SQL possuem numeração própria e checksum.

Documentação de referência: [OpenAPI 3.1](https://spec.openapis.org/oas/v3.1.0.html). Nesta etapa foram conferidos JSON, referências locais e estrutura do contrato; validação por ferramenta OpenAPI completa e implementação end-to-end permanecem pendentes.
