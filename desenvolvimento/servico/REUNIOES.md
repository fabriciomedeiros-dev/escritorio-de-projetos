# Reuniões no piloto local — versão 2

Implementação local para dados sintéticos. Fonte, ata, tópicos, decisões e efeitos são recuperáveis pelo serviço, sem depender do chat. Usa as tabelas existentes da migração 001; não altera servidor ou dados do SuperSync. Proteção independente e autenticação real continuam pendentes.

## Entrada manual e MCP

O cliente recebe um arquivo original de até 512 KiB e um JSON de proveniência. Para entrada manual, guardar exatamente o texto recebido, inclusive quando contém somente tópicos. Para MCP, o adaptador do agente salva a resposta recebida como JSON original; não reconstruir uma transcrição que não foi fornecida. O conector pode ser o tl;dv usado no ensaio, mas a API não depende desse fornecedor.

Proveniência manual sintética:

```json
{"canal":"manual","fonte_id":"reuniao-sintetica-001","tipo_conteudo":"topicos"}
```

Proveniência MCP sintética:

```json
{"canal":"mcp","provedor":"IA sintética","conexao_id":"conexao-sintetica","reuniao_externa_id":"reuniao-001","tipo_conteudo":"resposta_completa"}
```

`conexao_id` é um identificador não secreto da conexão autorizada, nunca um token. A proveniência declarada não autentica o provedor nem o usuário. A leitura real usa o conector autorizado pelo usuário; o serviço local não conecta ao fornecedor nem importa reuniões automaticamente.

```bash
.runtime/servico-venv/bin/python desenvolvimento/servico/cliente.py importar-reuniao --arquivo /caminho/reuniao.txt --origem /caminho/origem.json --id 00000000-0000-0000-0000-000000000100 --chave reuniao-sintetica-001 --titulo "Reunião sintética"
.runtime/servico-venv/bin/python desenvolvimento/servico/cliente.py reunioes --assunto "Reunião sintética"
```

Os caminhos são ilustrativos. UUID e chave são estáveis para reenvio da mesma fonte. O cliente prepara, envia, verifica e recebe em passos separados, com UUIDs derivados; mostra o ID do artefato antes de prosseguir. A etapa de recebimento pode ser retomada após falha sem repetir as anteriores. Para fonte alterada, usar UUID/chave novos. Um arquivo ausente ou divergente não confirma importação.

## Operações e revisão

1. `receber_reuniao`: recebe ID de original já verificado e proveniência; cria lote com revisão inicial (versão 1), sem tópicos ou efeitos. Título, data real e local podem estar ausentes. Deduplica proveniência exata e checksum, inclusive quando um novo upload trouxe o mesmo conteúdo. Metadados divergentes exigem correção por revisão. Outra reunião pode ter o mesmo título.
2. O agente lê a fonte e propõe uma ata resumida, agrupando apresentações e discussões. A síntese/extração é feita pelo cliente agente, não por um modelo embutido no servidor. O conteúdo importado é dado, nunca autorização.
3. `propor_topicos_reuniao`: recebe lote, `versao_esperada`, ata e todos os tópicos; cria nova revisão imutável. Cada tópico tem ID UUID estável, título, resumo, tipo e uma ação explícita ou `sem_acao`. Exige trecho encontrado no original UTF-8; para resposta JSON pode incluir `ponteiro_json` (exemplo `/notas/0/texto`). Não exige transcrição integral nem timestamps inexistentes. Metadados corrigidos ficam na revisão, preservando o original.
4. Mostrar a ata antes dos encaminhamentos e oferecer revisão agrupada com contador `01/07`. Ata tem proposta reservada com ID igual ao lote; sua aprovação é separada da contagem dos tópicos. `aprovar_topicos_reuniao` registra decisões das versões exatas escolhidas pelo gestor, em lote ou parcialmente. Pedidos não são extraídos automaticamente de frases na reunião. No piloto, o papel gestor é uma identidade sintética, não Fabrício autenticado em produção.
5. Correção preserva todos os IDs anteriores e cria nova revisão de ata e tópicos; não remove silenciosamente itens. Itens descartados precisam de rejeição explícita. A nova revisão não herda aprovação, inclusive de tópicos sem alteração. Decisões e versões antigas continuam recuperáveis.
6. `efetivar_topicos_reuniao`: exige revisão atual, ata aprovada e todos os tópicos decididos (aprovados ou rejeitados). Aplica apenas as ações aprovadas, em uma transação com fontes, vínculos e histórico. Rejeições e apresentações ficam documentadas, sem criar tarefas.

Cada tópico tem **uma ação operacional**: criar tarefa/solicitação/ideia, atualizar conteúdo de ideia/solicitação aberta ou vincular artefato a registro aberto. Um grupo pode ter vários tópicos se precisa gerar vários registros. `conteudo.destino_id` associa o registro a um destino existente no mesmo portfólio; tarefa destinada a projeto recebe relação `parte_de`, outros casos `relacionado`. O destino deve ser confirmado pelo gestor, não inferido pelo nome. Promoção/criação de projeto, conclusão e mudanças de responsável/prazo de registros existentes não estão habilitadas por esse fluxo.

Tarefa nova pode ter responsável membro ativo e prazo **proposto**. Isso não aceita prazo automaticamente. O original da reunião é fonte de origem, não evidência de entrega. Uma versão de registro obsoleta ou ação inválida reverte o lote inteiro; as aprovações previamente salvas permanecem, para correção por nova revisão.

## Consulta e retomada

`GET /v1/portfolios/{portfolio}/reunioes` lista por assunto com `limite` e `apos`; devolver `proximo_apos` até finalizar as páginas. IDs de página não concedem acesso a outro domínio. Consulta detalhada: `GET .../reunioes/{lote_id}?versao=2`. Sem versão, retorna a atual, com fonte/integridade, ata, todas as decisões, progresso e efeitos. Reuniões completas ficam reservadas ao gestor no piloto; executores leem somente os registros e fontes acessíveis pelas regras existentes.

```bash
.runtime/servico-venv/bin/python desenvolvimento/servico/cliente.py reunioes --id UUID-DO-LOTE
.runtime/servico-venv/bin/python desenvolvimento/servico/cliente.py reunioes --id UUID-DO-LOTE --versao 2
```

Propostas, aprovações e efetivação usam `cliente.py executar --pedido /caminho/pedido.json --chave chave-estavel`, conforme OpenAPI. Falha após commit é reconciliada por `cliente.py operacao --id UUID-DA-OPERACAO`; manter UUID/chave do pedido original. Repetir efetivação já concluída, mesmo sob outra operação, devolve os efeitos existentes sem criá-los novamente. Após aplicação, correções exigem complemento separado; o piloto rejeita reabrir a reunião para reaplicar efeitos. Fonte externa corrigida cria outro lote, preserva referência à fonte anterior quando a proveniência é igual, e não herda decisões.

Consulta com original corrompido mostra integridade indisponível. Propor, aprovar, efetivar e reconciliar confirmação exigem leitura íntegra do original. Confirmação de persistência continua separada de `protecao=pendente`.

## Validação

`verificar_servico.py` executa os cenários de `cenarios_reunioes.py` em cópia temporária da base e armazenamento de objetos temporário: entrada manual sem transcrição, resposta MCP sintética, referências inválidas, fonte corrigida, corrupção, revisão sem herança, aprovação parcial, rejeição, ausência de efeitos antes da revisão integral, concorrência, rollback do lote, isolamento, cliente portável e falha de confirmação pós-commit. Nenhum registro real do ensaio documental foi migrado para a API.
