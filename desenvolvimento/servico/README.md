# Serviço mínimo local — Escritório v2

Piloto implementado e testado em 03/10/2026. Usa o PostgreSQL isolado, contrato agnóstico e identidades sintéticas. Não é implantação do SuperSync nem servidor de produção.

## Acesso técnico pelo chat

Aplicar a [política de segurança do chat](../../arquitetura/v2/seguranca-chat.md), inclusive neste piloto: Fabrício e o desenvolvedor explicitamente autorizado do projeto podem receber acesso e informações técnicas após verificação de identidade e permissão. Negar a pessoas não autorizadas ou sem autorização verificável. As identidades sintéticas do piloto não representam automaticamente essas autorizações. A regra está documentada; o controle técnico de divulgação no adaptador e no serviço ainda está pendente. Não publicar credenciais nos documentos ou commits.

## Disponível

- Capturar texto ou anexo verificado como entrada de triagem, preservando conteúdo e origem.
- Preparar, enviar, verificar e baixar originais imutáveis; vincular documentação/evidência com histórico e versão.
- Criar tarefa, solicitação ou ideia em estado inicial, com lacunas explícitas.
- Atualizar título, resultado esperado ou critério de ideia/solicitação aberta e vincular complementos originais, com motivo, versão e histórico; somente gestor.
- Registrar relato em tarefa aberta, com entregue, restante, dificuldade, esforço e prazo proposto.
- Consultar registros por ID, tipo, situação, assunto, origem e período, com paginação assinada.
- Consultar operação por UUID e reconciliar confirmação perdida após commit.

A ficha inclui os textos das entradas originais e complementares vinculadas, permitindo recuperar definições sem conhecer o chat de origem. A resposta contém versão, histórico de origem, fontes, dependências, últimas 25 atualizações e lacunas. Relato não conclui tarefa nem aceita prazo automaticamente. O nome informado do autor do relato é separado do remetente autenticado. ID de registro usa prefixo do portfólio/tipo e UUID; título não é identificador.

Reuniões: recebimento de fonte manual/resposta MCP, ata e tópicos propostos pelo agente, revisão/aprovação por versão e efetivação transacional estão implementados localmente. Consulte [fluxo e comandos de reuniões](REUNIOES.md).

Bloqueios/dependências: registro, acompanhamento e resolução com evidência implementados. Conclusão de tarefa disponível por aceite humano explícito, com critério/evidência e ausência de pendências; ver [limites e comandos](BLOQUEIOS.md).

Indisponível: verificação automática de conclusão, conclusão de solicitação/projeto, promoção a projeto, cronograma, backup independente e interface web/menu do gestor. Comandos correspondentes são rejeitados explicitamente; não confirme seus efeitos em chat.

## Preparação e execução

Pré-requisitos: Python 3.10+ e ferramentas PostgreSQL do ambiente local. A configuração testada usa Python 3.14.3, psycopg 3.3.6, jsonschema 4.26.0 e PostgreSQL local 14.20. A política de versões e a homologação do SuperSync continuam pendentes.

```bash
python3 -m venv .runtime/servico-venv
.runtime/servico-venv/bin/python -m pip install -r desenvolvimento/servico/requirements.txt
.runtime/servico-venv/bin/python desenvolvimento/local/ambiente.py start
.runtime/servico-venv/bin/python desenvolvimento/local/ambiente.py migrate
.runtime/servico-venv/bin/python desenvolvimento/servico/preparar_demo.py
.runtime/servico-venv/bin/python desenvolvimento/servico/http_local.py
```

`preparar_demo` cria apenas `demo_escritorio`, `demo_outro` e quatro identidades fictícias: gestor, executor, consulta e outro. Não cria portfólios SAERJ/pessoal nem importa documentos. Senhas e tokens ficam exclusivamente em `.runtime/servico/`, com permissões restritas, ignorada pelo Git. Não copiar esses arquivos para a documentação ou mensagens.

O serviço escuta somente `127.0.0.1:8765`; PostgreSQL usa socket local próprio. O endereço não permite uso remoto e não altera o servidor existente. A conexão SQL usa papel sem superuser, sem criação de banco/schema e sem DELETE; os scripts de preparação/teste usam credencial administrativa somente no cluster local.

## Cliente de referência

Em outro terminal, sem colocar token na linha de comando:

```bash
.runtime/servico-venv/bin/python desenvolvimento/servico/cliente.py consultar
.runtime/servico-venv/bin/python desenvolvimento/servico/cliente.py executar --pedido desenvolvimento/servico/exemplos/criar_tarefa.json --chave exemplo-tarefa-001
.runtime/servico-venv/bin/python desenvolvimento/servico/cliente.py consultar --perfil consulta
```

O exemplo é sintético e contém ID fixo: executar novamente devolve a mesma operação, não cria outra tarefa. Para novo trabalho, preparar novo UUID e nova chave; para repetir o mesmo pedido, manter ambos. O cliente lê credenciais do arquivo local e envia Bearer token; qualquer agente pode usar esse cliente ou o mesmo contrato HTTP, sem acesso SQL administrativo.

Para atualização pelo executor, criar tarefa com `responsavel_total` correspondente à identidade sintética; ler seu UUID localmente, sem publicar o arquivo de credenciais. O cliente aceita pedido JSON do contrato. Não há autoatribuição de pessoas reais neste piloto.

`Ctrl+C` encerra o serviço HTTP. Depois:

```bash
.runtime/servico-venv/bin/python desenvolvimento/local/ambiente.py stop
```

O serviço pode permanecer ativo durante o teste interativo. Dados do ambiente e credenciais sintéticas persistem para uso posterior; encerrar o serviço não apaga os registros.

## Autorização e verificabilidade

Tokens aleatórios locais identificam pessoas; o servidor mantém hashes dos tokens, e o cliente guarda os valores em arquivo restrito. Esse mecanismo é exclusivo do piloto; não integra o login do SuperSync e ainda não oferece expiração/rotação/revogação gerenciada. Não reutilizar esses tokens em produção.

Gestor captura/cria e acompanha seu portfólio; executor consulta/atualiza apenas tarefas de que é responsável ou executor atribuído; consulta só lê. Operações de outro autor só são consultáveis pelo gestor, respeitando o domínio. Membros inativos são bloqueados por consulta ao banco em cada requisição. O corpo não aceita identidade ou papel declarados pelo agente.

Mutação serializada por portfólio, SQL parametrizado, estado e histórico na mesma transação; repetição identifica pedido, pessoa, chave e UUID. Conteúdo divergente retorna 409. Após commit, outra conexão verifica registros/histórico e entrada antes de marcar `verificada`. Falha depois de salvar é reconciliada por consulta da operação. A resposta preserva `protecao=pendente`: nenhuma cópia independente está configurada.

O serviço rejeita campos desconhecidos e valida tipos, datas, UUIDs e demais restrições do JSON Schema do contrato. Paginação vincula cursor ao portfólio, identidade e filtros. Resultados são ordenados por ID imutável; não é snapshot global da busca, e inserções posteriores podem exigir uma nova consulta para uma visão atualizada.

## Testes

Com PostgreSQL iniciado e demo preparada:

```bash
.runtime/servico-venv/bin/python desenvolvimento/testes/verificar_servico.py
.runtime/servico-venv/bin/python desenvolvimento/testes/verificar_contrato.py
```

O teste HTTP restaura uma cópia da base local em banco temporário, usa porta de loopback alocada dinamicamente e remove somente o banco de teste ao terminar. Verifica fluxo HTTP → banco, autorização/perfis/domínios, executor atribuído, estados e prazos preservados, histórico, conflito de versão, repetição simultânea, recuperação após falha simulada pós-commit, filtros com texto adverso, paginação, validação de respostas e rejeição de funções indisponíveis.

O ensaio usa pg_dump/restauração em base temporária e preserva conexões existentes, inclusive do DBeaver. A cópia inclui a demonstração local; não usar este runner para dados reais. O script não aponta para servidor externo e não depende de conexão do SuperSync. A validade estrutural das partes JSON Schema foi testada; validação integral da especificação OpenAPI por ferramenta especializada continua pendente.

## Limites para passagem ao implementador

`http.server` é um servidor de desenvolvimento local, sem TLS, hardening ou adequação produtiva. Escolher runtime de produção, autenticação SuperSync, papéis SQL/isolamento, pool, limites/monitoramento e deploy somente na etapa de integração. A biblioteca padrão documenta esse limite. [HTTP local](https://docs.python.org/3/library/http.server.html).

Originais e vínculos de evidências estão implementados localmente. Revisão/aprovação de reuniões, dependências/bloqueios e conclusão de tarefa por aceite humano estão implementados no piloto. Não migrar dados reais antes de proteger/restaurar banco e arquivos e declarar o corte de autoridade.

Referências técnicas: [parâmetros psycopg](https://www.psycopg.org/psycopg3/docs/basic/params.html), [JSON Schema](https://python-jsonschema.readthedocs.io/en/stable/validate/), [contrato](../contratos/README.md).

## Complementos e consultas de ideias

Siga as [instruções portáveis do gestor](../../arquitetura/v2/operacao-gestor.md). `atualizar_registro` permite conteúdo e vínculo de entrada em ideia/solicitação aberta, com histórico e conflito de versão. A busca por assunto cobre título e resultado esperado. Exemplo de consulta:

```bash
.runtime/servico-venv/bin/python desenvolvimento/servico/cliente.py consultar --tipo ideia --assunto intranet
```

Os testes exercitam reatribuição indevida de entrada, isolamento, campo não permitido, original preservado, rollback de falha pré-commit e recuperação independente do chat. Nenhuma migração SQL é necessária nesta entrega: referências de entradas usam o campo `origem`, validadas pelo serviço.

## Originais e evidências — piloto local

Limite de 512 KiB por arquivo. O cliente calcula tamanho e SHA-256, prepara metadados por operação, envia os bytes em base64 e o serviço relê o objeto salvo antes de confirmar. `verificar_artefato` revalida o objeto existente. Nome e tipo de mídia são metadados informados; não significam análise do conteúdo ou detecção automática de formato. O servidor gera a chave interna e não aceita caminho/URL remoto como original salvo.

Objetos ficam em `.runtime/servico/objetos/`, fora do Git, com arquivos criados com permissão restrita. Não são anexos guardados apenas no chat. Upload usa arquivo temporário, fsync e publicação sem sobrescrita. Se o banco reverter após a gravação física, o original pode permanecer no armazenamento: repetir o mesmo pedido reconcilia seus bytes; não há coleta automática de órfãos. Essa persistência é local, sem cópia independente e sem acesso de outro computador.

Preparação de metadados não confirma recebimento do arquivo: a resposta informa envio/verificação pendentes. Captura de entrada, vínculo ou relato só aceita artefato verificado e relido. Arquivo ausente, checksum divergente e symlink são recusados. Consultas de fichas sinalizam `integridade=indisponivel_ou_divergente` quando o arquivo original não está íntegro. A consulta de operação de envio revalida o arquivo antes de repetir uma confirmação antiga.

Somente gestor prepara/envia/verifica/vincula no piloto. Executor pode referenciar evidência já acessível em relato da tarefa atribuída. Download exige membro ativo: gestor acessa o portfólio; demais perfis acessam originais próprios ou vinculados a registros que podem consultar. Perfil consulta segue a permissão de leitura do portfólio já existente; autenticação real e participação por projeto no SuperSync ainda precisam de implementação. Downloads são binários, como anexo, sem renderização de HTML/script no servidor e sem divulgar caminho interno.

O cliente possui `anexar` e `baixar`. Para anexar, fornecer `--arquivo`, `--id` com UUID estável do envio e `--chave` estável. Para vincular na mesma sequência, fornecer também `--registro`, `--versao` e `--finalidade` (`documentacao`, `evidencia` ou `origem`). O cliente mostra o ID preparado antes de enviar e confirma envio e vínculo separadamente. Repetir a mesma chamada com o mesmo arquivo/UUID/chave reconcilia as etapas sem duplicar. Alterar conteúdo sob a mesma operação gera conflito.

Em `baixar`, `--id` é o UUID do artefato e `--arquivo` é o destino local, que não será sobrescrito. `--porta` permite ensaio em outra porta, sempre em 127.0.0.1. Não utilizar esses comandos para anexar segredos a registros de negócio.

Não há nova migração de tabelas. Execute novamente `preparar_demo.py` para conferir os grants mínimos de INSERT em artefatos/fontes e UPDATE em artefatos, preservando as credenciais existentes. Reinicie apenas o serviço HTTP para carregar esta implementação. O usuário do serviço continua sem DELETE, superuser, criação de banco ou schema.

Testes com arquivos sintéticos incluem checksum/tamanho, reenvio, falha entre arquivo e commit, corrupção, symlink, download sem permissão, isolamento, cliente portável e evidência de entrega parcial. Evidência registrada não conclui a tarefa. Restauração conjunta de arquivos e banco, proteção independente, quotas totais, retenção, varredura de conteúdo e armazenamento central são pendências para produção.

## Incremento de reuniões — 04/10/2026

Recebimento, ata agrupada, revisões, decisões e aplicação transacional implementados em [REUNIOES.md](REUNIOES.md), com consultas e cliente portável. Executar `preparar_demo.py` confere os privilégios mínimos de INSERT nas tabelas existentes de reuniões/vínculos sem trocar credenciais. Nenhuma migração SQL nova; reiniciar somente o HTTP para carregar o código. Identidades reais, proteção independente e uso central continuam pendentes.

## Incremento de bloqueios e aceite humano

Aplicar a migração 002 com `ambiente.py migrate` e conferir privilégios locais com `preparar_demo.py`; reiniciar somente o HTTP para carregar o código. Registro, acompanhamento e resolução de dependências/bloqueios e aceite humano de tarefas implementados, conforme [BLOQUEIOS.md](BLOQUEIOS.md). Identidade real, planejamento e proteção continuam pendentes.

## Windows nativo

Use a preparação de `../local/REPLICACAO.md`. Nos exemplos acima, substitua `.runtime/servico-venv/bin/python` por `.runtime/servico-venv/Scripts/python.exe`. Defina `ESCRITORIO_PG_BIN` com o caminho dos binários locais. Execução em Windows real ainda pendente.
