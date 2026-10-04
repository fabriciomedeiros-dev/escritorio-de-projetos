# Esquema físico — Escritório v2

[001_nucleo.sql](001_nucleo.sql) implementa a primeira revisão PostgreSQL do modelo lógico. A migração foi aplicada somente no cluster local `escritorio_test`. Nenhum schema, tabela ou usuário do SuperSync foi alterado.

## Organização

Schema dedicado `escritorio`, acesso público revogado e sem extensões externas. UUIDs identificam operações/artefatos; IDs textuais estáveis identificam registros de trabalho. Toda relação operacional usa chave composta por portfólio, impedindo vínculos acidentais entre domínios. Datas civis usam `date`; instantes usam `timestamptz`; esforço é aproximado e pode permanecer nulo.

| Grupo | Tabelas |
|---|---|
| Identidade e acesso | portfolios, pessoas, identidades, membros |
| Captura e persistência | operacoes, entradas, artefatos |
| Trabalho e documentação | registros, definicoes, vinculos_registros, executores, fontes |
| Reuniões | lotes, propostas, aprovacoes, efetivacoes |
| Andamento e aceite | atualizacoes, dependencias, validacoes, decisoes |
| Planejamento | sprints, itens_sprint, capacidades, previsoes, alertas |
| Auditoria e recuperação | historico, exportacoes, migracoes |

`registros` reúne os campos comuns de ideia, solicitação, projeto e tarefa. `definicoes` guarda objetivo, escopo e referências sem substituir os documentos canônicos. Relação `parte_de` orienta composição da entrega; `originou` preserva solicitação/projeto ou ideia/projeto. Tipos admissíveis e ciclos nas relações são validados pelo serviço.

Propostas são revisões imutáveis. Aprovação aponta a revisão exata, e efetivação só referencia uma aprovação positiva. Correção de tópico cria revisão nova; não reescreve aprovação. O serviço verifica que a revisão aprovada é a revisada/atual e registra sua efetivação atômica.

## Garantias no banco e no serviço

No banco: chaves compostas, estados básicos, esforço não negativo, reserva dentro da capacidade, checksum no formato correto, revisão de aprovação, imutabilidade de propostas/aceites/histórico e incremento de versão de registros. Constraint triggers diferidas conferem o estado final da transação: tarefa concluída exige responsável, critério, validação da versão atual, evidência marcada verificada e ausência de dependências/subtarefas necessárias pendentes. Remover a evidência depois de concluir também é rejeitado.

No serviço: autenticar e autorizar, verificar membro ativo, comparar versão esperada, manter estado e histórico na mesma transação, impedir ciclos e promoção não autorizada, avaliar evidência semanticamente e verificar bytes reais, aprovar prazos e metas conforme governança. Escrever `verificado` no banco não prova que o arquivo existe; só o serviço pode produzir essa confirmação. Solicitações concluídas e projetos encerrados exigem critérios próprios no serviço, além do que o trigger implementa para tarefas.

O schema não cria usuários de produção, permissões finais ou políticas RLS. O acesso público revogado é uma base, não autenticação da aplicação. A execução local é administrativa; não valida limites de um executor. Antes de implantação, definir owner separado de papel de aplicação/backup e autorização no serviço. Se RLS for adicionada, testar explicitamente seus efeitos e bypasses.

Escritores devem seguir o lock transacional de portfólio do [contrato](../contratos/README.md); o trigger sozinho não garante coerência de validações agregadas diante de escritores concorrentes. A função de conclusão varre tarefas concluídas como solução inicial; medir e restringir sua abrangência em evolução antes de volume elevado.

## Aplicação local e mudança de versão

```bash
python3 desenvolvimento/local/ambiente.py start
python3 desenvolvimento/local/ambiente.py migrate
python3 desenvolvimento/testes/verificar_esquema.py
python3 desenvolvimento/local/ambiente.py stop
```

O comando aceita apenas o banco local criado pelo próprio ambiente. Aplicação é transacional e serializada por advisory lock. A segunda execução confere o checksum e não reaplica. Alteração de uma migração aplicada é rejeitada pelo runner; evolução exige arquivo numerado novo. O runner percorre migrações em ordem e confere cada checksum. A migração [002_bloqueios.sql](002_bloqueios.sql) acrescenta indicação explícita de impedimento de avanço e preservação do estado anterior da tarefa.

Nenhum portfólio, pessoa ou trabalho real é semeado. Testes usam dados sintéticos e rollback; também exportam/restauram o schema real em outra base temporária e repetem os testes nela. A base de restauração gerada é removida ao terminar, sem remover o cluster persistente. O schema persiste vazio, exceto o registro de migração. Não há função de reset destrutivo. Rollback de implantação futura exige plano específico e exportação prévia; não remover schema para desfazer uma mudança com dados reais.

Fontes técnicas consultadas: [CREATE TABLE](https://www.postgresql.org/docs/14/sql-createtable.html), [constraint triggers](https://www.postgresql.org/docs/14/sql-createtrigger.html). A compatibilidade de sintaxe foi exercitada no PostgreSQL local 14.20; a versão de homologação deve ser alinhada ao servidor e à política de suporte antes da implantação.
