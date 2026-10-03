# Modelo lógico de dados — versão 2

Modelo independente de tecnologia. Campos obrigatórios para acompanhamento podem estar ausentes na captura, mas devem gerar lacunas explícitas. Nunca preencher responsável, prazo ou esforço fictício.

## Convenções comuns

Identificador imutável com prefixo de portfólio e tipo; título não é chave. Exemplos de formato: `SAERJ-SOL-000001`, `SAERJ-TAR-000001`. O mecanismo de alocação deve evitar colisões em acesso concorrente. Datas de prazo distinguem data civil de instante; instantes preservam fuso e autoria. Fuso inicial: America/Sao_Paulo.

Registros possuem `id`, `portfolio_id`, título, criação, atualização, autor e situação. Eventos possuem ator, origem, instante e operação. Relações entre portfólios não são permitidas por padrão. A pessoa que encaminha um relato e o autor alegado do relato são campos diferentes; entrada indireta não equivale a autenticação do executor.

## Entidades e campos

| Entidade | Campos específicos e relações |
|---|---|
| Portfólio | Identificador, nome, permissões, calendário e configurações próprias |
| Pessoa | Identificador, nome, identidade autenticada quando disponível, papéis e portfólios autorizados |
| Entrada | Conteúdo recebido ou referência ao original, remetente, origem, recebimento, chave de repetição, classificação proposta/confirmada, destino e pendências |
| Ideia | Problema, valor esperado, ficha, autorização de preparação, TAP, fase do conselho e decisão de promoção |
| Solicitação | Solicitante/origem, resultado esperado, urgência, impacto, meta desejada, responsável total e tarefas vinculadas; projeto opcional |
| Projeto | Objetivo, escopo aprovado, responsável total, meta, decisão de promoção, documentação canônica e tarefas; requisitos vinculados à sua fonte oficial |
| Tarefa | Resultado esperado, critérios de conclusão, responsável total, executores, projeto/solicitação opcional, tarefa pai opcional, prazo proposto/aceito, esforço restante, estado e evidências |
| Atualização | Tarefa, relato de avanço, entregue, restante, dificuldades, esforço estimado, prazo proposto, autor, remetente e fontes |
| Dependência | Entrega afetada, tarefa/terceiro provedor, responsável pelo acompanhamento, motivo, próxima ação, data de acompanhamento, situação e critério de resolução |
| Artefato | Nome, tipo, localização preservada, checksum, tamanho, autor/origem, recebimento, versão e relações com registros |
| Proposta extraída | Artefato, localização na fonte, conteúdo, tipo, destinos sugeridos, lacunas, lote e estado de aprovação |
| Aprovação | Lote/itens, versão examinada, decisor, instante, resultado, correções e registros efetivados |
| Decisão | Assunto, justificativa, alternativas/impactos, decisor, data, fonte documental e registros afetados |
| Sprint | Portfólio, período, itens aprovados, linha de base e alterações autorizadas |
| Capacidade | Pessoa, sprint, horas disponíveis, reserva, ausências e fonte da informação |
| Previsão | Entrega, data calculada, método, esforço/capacidade/dependências utilizados, lacunas e instante do cálculo |
| Alerta | Tipo, registros afetados, causa, gravidade justificada, primeira/última ocorrência, tratamento e estado |
| Evento de histórico | Registro, ação, valores anteriores/novos ou referência à versão, ator, motivo, fonte e aprovação aplicável |
| Operação de registro | Identificador, entradas recebidas, resultados, estado de persistência/verificação/proteção, falhas e tentativa de recuperação |
| Exportação/cópia | Manifesto de IDs e artefatos, checksums, destino independente, instante, estado e último teste de restauração |

## Relações

Uma solicitação gera várias tarefas e pode originar projeto sem perder sua origem. Projetos possuem várias tarefas. Uma tarefa pode existir sem projeto nem solicitação, ter subtarefas e múltiplas dependências; a responsabilidade total é singular. Artefatos podem sustentar várias atualizações ou decisões. Aprovações referenciam a versão exata revisada; edição posterior exige nova revisão do conteúdo afetado.

## Estados

- Entrada: recebida → persistida/verificada → triagem pendente ou vinculada. Proteção é um estado separado.
- Proposta de reunião: pendente → aprovada, corrigida ou rejeitada. Aprovação aplica a versão revisada uma única vez; falha de aplicação fica explícita.
- Tarefa: capturada, planejada, em andamento, bloqueada, conclusão informada aguardando validação, concluída ou cancelada. Entrega parcial aparece nas atualizações/subtarefas, sem concluir a tarefa pai. Reabertura preserva motivo e histórico.
- Solicitação: capturada, em triagem, planejada, em andamento, aguardando validação, concluída ou cancelada. Conclusão verifica resultado e tarefas necessárias.
- Ideias seguem as fases do conselho existente. Status de projeto distingue fase do ciclo de vida de saúde executiva.

## Invariantes

1. Cada dado operacional possui uma fonte oficial; documentos derivados indicam origem e data de geração.
2. Nenhuma tarefa conclui sem evidência e verificação do critério ou validação humana registrada; dependências necessárias precisam estar resolvidas.
3. Atualização de prazo preserva valor anterior, autor, motivo e aprovação quando exigida.
4. Toda proposta extraída de reunião exige aprovação antes de criar ou alterar registros operacionais.
5. Nenhuma operação confirma sucesso sem leitura de verificação e integridade dos anexos; repetição não duplica seus efeitos.
6. Exclusão lógica/cancelamento preserva histórico; remoção definitiva de originais exige decisão específica.
7. Filtros e permissões de portfólio são aplicados na camada de operações, não apenas no texto do agente.
8. Relatos divergentes e lacunas são consultáveis; ausência de esforço não é esforço zero.
9. Exportação permite reconstruir IDs, vínculos, autoria, aprovações e arquivos sem depender do histórico dos chats.
10. Mudanças concorrentes verificam a versão do registro para evitar sobrescrever atualização não examinada.

## Autoridade dos campos

Estado, prazo, responsável, esforço e dependências: fonte operacional futura. Narrativa de decisões e documentos gerenciais: Markdown vinculado, com índices operacionais. Requisitos funcionais: repositório de documentação indicado. Código e evidências técnicas: repositório de desenvolvimento. Metadados locais apontam para essas fontes, sem redefini-las.
