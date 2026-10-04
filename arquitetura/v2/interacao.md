# Interação — versão 2

Comportamento proposto; nenhuma skill, serviço ou interface nova está implantada por este documento.

## Conversas na interface inicial

Um chat de rotina por portfólio recebe solicitações pontuais e atualizações. Chats dedicados servem aos projetos ativos, ideias e análises extensas. Uma solicitação não exige um novo chat; seu identificador é independente da conversa. Abrir um chat específico quando solicitado pelo usuário, sem depender dele para preservar memória.

Ao receber oi, identificar o portfólio e consultar registros antes de mostrar um resumo curto: entregas vencidas, bloqueios, ausência de prazo, aprovações pendentes e riscos. Oferecer registrar demanda, consultar andamento, planejar semana, revisar reunião, gerar relatório e avaliar ideia. Não inventar contagens nem consultar outro domínio para preencher o resumo. Pedidos diretos dispensam menu.

Respostas iniciais em texto, tabelas e links. Confirmação de registro indica ID, resumo do salvo, lacunas e pendência de proteção, quando houver. Consultas de status mostram atualização, fonte, evidência, restante e dependências. Nenhum chat presume possuir dados atualizados sem consultar a fonte.

## Pedidos de acesso técnico

Aplicar a [política de acesso técnico pelo chat](seguranca-chat.md): permitir a Fabrício e ao desenvolvedor designado do projeto após verificar identidade e autorização, respeitando projeto e ambiente. Negar a usuários não autorizados ou sem autorização verificável. Participar de um projeto não concede acesso técnico. Consultas de negócio seguem suas próprias permissões.

## Portabilidade

Codex é o primeiro cliente; Claude Code ou outro agente pode substituí-lo. O fluxo de resumo, captura, consulta e aprovação é comum e não exige comandos exclusivos de um produto. Skills e arquivos de configuração específicos são adaptadores das instruções comuns, não a fonte das regras de negócio.

Abertura automática de chats e apresentação visual dependem das capacidades do cliente. Quando não disponíveis, orientar o usuário a abrir a conversa e recuperar o contexto pelo identificador do registro. O histórico de conversas não é necessário para a continuidade. Anexos precisam ser persistidos fora do armazenamento exclusivo do chat.

## Conselho

O pedido avaliar ideia encaminha ao fluxo do conselho existente. Fabrício autoriza a preparação; o conselho apresenta síntese, divergências e decisões necessárias. Não é preciso invocar cada papel individualmente. Preparar proposta não autoriza promoção nem execução.

## Entrada de reuniões

Receber por MCP de um serviço de IA de transcrição ou por texto enviado pelo usuário com tópicos, inclusive sem transcrição integral. Ambos seguem o [fluxo comum de reuniões](reunioes.md). Preservar proveniência e lacunas; tópicos externos também são propostas pendentes. Guardar e verificar o original; extrair tópicos; agrupar por projeto/solicitação; mostrar todos para revisão. Permitir aprovar lote, corrigir ou rejeitar itens. Pendências ficam recuperáveis. Depois da aprovação, aplicar operações autorizadas e confirmar seus IDs; falha parcial exige recuperação visível sem reaplicar itens concluídos.

## Participação da equipe

Etapa inicial: Fabrício encaminha relatos com origem informada. Etapa posterior: identidade individual autenticada, lista minhas tarefas, atualização por formulário e chat opcional. Registrar entregue, restante, dificuldade, prazo, esforço e anexos na mesma fonte operacional consultada por qualquer cliente autorizado.

Executores atualizam tarefas autorizadas e propõem prazos; mudanças de escopo, responsável total, prioridade e meta seguem aprovação gerencial. Permissões devem ser verificadas no serviço. Chat compartilhado é opcional; conversas individuais podem alimentar os mesmos registros.

## Exemplos ilustrativos

- Registre a solicitação do relatório de faturamento do terceiro trimestre: capturar como solicitação, perguntar responsável/prazo ausentes e sugerir tarefas.
- Minha parte terminou, mas falta API: preservar evidência do avanço e manter entrega pendente com dependência e próxima ação.
- Quanto falta no inventário: mostrar tarefas restantes, esforço informado, dependências e previsão; se faltarem dados, declarar a lacuna.
- Onde ficou definido o escopo: localizar a decisão aprovada e abrir a documentação canônica, sem usar uma fala não aprovada como decisão.
