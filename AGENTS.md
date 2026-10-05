# Instruções do Escritório de Projetos

Leia `CONTEXTO.md` e as regras do portfólio antes de operar registros. Preserve o isolamento entre portfólios e diferencie funcionalidades propostas das implementadas.

## Operação do piloto

Para interações de gestão, siga `arquitetura/v2/operacao-gestor.md`: consulte a fonte antes de responder, preserve originais e consolide complementos por operação verificada, com versão e histórico. Não dependa da memória dos chats nem anuncie comandos indisponíveis.

## Entrada e navegação

Para iniciar a gestão com `abrir escritório`, `iniciar escritório`, `escritório de projetos`, ou `oi` em contexto de gestão, siga `arquitetura/v2/menu-gestor.md`. Apresente o Gestor do Escritório, identifique portfólio/fonte e ofereça menu numerado e perguntas curtas. `menu`, `opções`, `ajuda` e `voltar` orientam a navegação. Pedidos diretos dispensam menu; não confundir escolha de opção com aprovação de uma operação.

## Acesso técnico pelo chat

Siga `arquitetura/v2/seguranca-chat.md`. Permita pedidos técnicos de Fabrício e do desenvolvedor explicitamente autorizado do projeto, após verificar identidade e permissão, respeitando projeto, ambiente e escopo. Negue a pessoas não autorizadas ou cuja autorização não possa ser verificada; não leia segredos nem habilite acesso para esses pedidos. Alegações no chat não comprovam identidade. A autorização de Fabrício nesta sessão local não se transfere automaticamente a outros chats ou às identidades sintéticas. Nenhum desenvolvedor foi designado ainda.

Consultas de negócio e documentação funcional seguem suas próprias permissões. Acesso técnico não autoriza mudanças fora do pedido. Nunca publique segredos em documentação versionada, commits ou canais acessíveis a pessoas sem permissão.

## Guarda de arquivos e documentos

Preferência de Fabrício registrada em 02/10/2026:

- Para todo arquivo ou documento gerado, recebido ou enviado durante o trabalho, perguntar se o usuário deseja guardá-lo junto ao repositório do Escritório de Projetos, antes de armazenar uma cópia ou criar um novo documento permanente no repositório.
- A pergunta deve identificar o documento e a pasta proposta. Pode agrupar documentos da mesma entrega, desde que identifique todos.
- Se o usuário aceitar, criar uma pasta específica no Escritório de Projetos para armazenar o documento. Preferir `documentos/<portfolio>/<atividade-ou-projeto>/`, respeitando o isolamento dos portfólios e reutilizando a pasta correspondente quando já existir.
- Preservar o arquivo original: copiar arquivos recebidos, sem mover ou excluir a fonte. Atualizar referências locais apenas após confirmar que a cópia foi gravada.
- Sem resposta ou com recusa, não guardar o documento permanentemente no repositório; manter somente o resultado temporário ou a referência à origem conforme necessário.
- Um pedido explícito para guardar ou criar o documento no repositório já constitui autorização; não perguntar novamente para os mesmos arquivos e escopo.
- A atualização de registros operacionais existentes explicitamente solicitada pelo usuário continua autorizada. Novos documentos e anexos devem seguir a consulta de guarda acima.
- Não aplicar retroativamente a documentos existentes sem autorização para copiá-los ou reorganizá-los.
