# Fundamentos do domínio e configuração

## Domínio

Portfólios isolados: `saerj` e `pessoal`; `demo_escritorio`/`demo_outro` são sintéticos. Ideias em conselho não são projetos; promoção exige decisão humana. Solicitações e tarefas podem existir sem projeto. Título não é ID; origem informada não é autenticação. Fuso: `America/Sao_Paulo`; datas civis de prazo e instantes de eventos têm semânticas distintas.

Fonte oficial atual: Markdown. Fonte futura dos campos operacionais: PostgreSQL após corte aprovado. Documentação permanece no repositório; anexos em armazenamento persistente com ID, hash, tamanho e vínculo. Não sincronizar arquivos físicos do PostgreSQL pelo Git ou por pasta compartilhada.

## Regras inegociáveis

Conclusão requer responsável total, critério, evidência e aceite; dependências necessárias pendentes impedem conclusão. Impedimento de avanço difere de dependência de entrega. Remover o último impedimento restaura estado anterior sem concluir. Aprovação refere-se à revisão exata; mudança exige revisão nova. Repetição não duplica efeito; divergência de conteúdo/versão exige conflito. Ausência de esforço não equivale a zero. Relatos divergentes permanecem registrados, sem escolher a versão recente automaticamente.

## Credenciais exclusivamente simuladas

Exemplos abaixo são fictícios e não funcionam no piloto instalado. Não reutilizar em produção.

| Perfil de fixture | Login fictício | Senha fictícia |
|---|---|---|
| Gestor | gestor@example.test | TESTE-SIMULADO-GESTOR |
| Executor | executor@example.test | TESTE-SIMULADO-EXECUTOR |
| Consulta | consulta@example.test | TESTE-SIMULADO-CONSULTA |

O piloto real usa tokens aleatórios por perfil, não estes logins. Integração com usuários SuperSync ainda não implementada. Não copiar valores de `.runtime` ou `.env` para documentação.

## Configuração existente

- Piloto: `ESCRITORIO_PG_BIN` aponta para binários PostgreSQL; venv própria em `.runtime/servico-venv`. Configuração/segredos são gerados em `.runtime`, ignorados pelo Git e protegidos por ACL.
- SuperSync: `SECRET_KEY`, `DJANGO_DEBUG`, `DATABASE_URL`, `USAR_POSTGRES_LOCAL`, `GOOGLE_APPLICATION_CREDENTIALS` são nomes documentados em seu AGENTS.md. Necessidade e interpretação devem ser conferidas no settings para o ambiente alvo; não definir caminhos de credenciais GCP por suposição.

## Configuração proposta para integração (a implementar)

```dotenv
SECRET_KEY=SUBSTITUIR_POR_VALOR_LOCAL_ALEATORIO
DJANGO_DEBUG=true
DATABASE_URL=postgresql://USUARIO_SIMULADO:SENHA_SIMULADA@127.0.0.1:5432/BANCO_HOMOLOGACAO
ESCRITORIO_API_URL=http://127.0.0.1:8765
ESCRITORIO_STORAGE_ROOT=CAMINHO_LOCAL_PRIVADO
```

Esse bloco é modelo, não arquivo executável nem conexão existente. `ESCRITORIO_API_URL`/`ESCRITORIO_STORAGE_ROOT` não são variáveis já reconhecidas pelo piloto; dependem do adaptador proposto. Segredo para autenticação serviço-a-serviço será definido no desenho de integração, sem valor versionado.

## Pendências de decisão

Banco próprio ou schema, integração de identidade, runtime homologado, owner de migrations, hospedagem de anexos, destino/retenção de backup, executor e cronograma. O banco de ensaio identificado nesta sessão não deve ser conexão padrão do serviço operacional. Não há garantia de proteção independente instalada.

## Fontes e validade

Preparado em 08/10/2026 para o Escritório v2 com integração proposta ao SuperSync. Documento de preparação: não promove a iniciativa a projeto nem autoriza produção.

Fontes no Escritório: `CONTEXTO.md`, `AGENTS.md`, `arquitetura/v2/{especificacao,modelo-dados,implementacao-supersync,operacao-gestor,seguranca-chat}.md`, `desenvolvimento/contratos/openapi.json`, `desenvolvimento/migrations/`, `desenvolvimento/servico/`, `portfolios/saerj/projetos/supersync/desenvolvimento.md`. Fontes de implementação consultadas em `C:/Users/fabri/Projetos/supersync`: `AGENTS.md`, `requirements.txt`, `Dockerfile` e inventário de diretórios; HEAD observado `12f6dae`. Não foram lidos .env, dumps ou segredos, nem validados autenticação, infraestrutura remota ou comportamento do checkout completo. A inspeção documental anterior cita `bba8f83`; não a tratar como HEAD atual.
