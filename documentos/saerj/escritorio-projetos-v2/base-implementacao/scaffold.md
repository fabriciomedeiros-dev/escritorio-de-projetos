# Esqueleto e estado inicial

## Repositórios e autoridade

Escritório: `C:/Users/fabri/Projetos/Escritorio de Projetos`, documentação v2.0.0 e piloto. SuperSync: `C:/Users/fabri/Projetos/supersync`, aplicação Django existente, HEAD observado `12f6dae`. Manter documentação gerencial no Escritório; código de integração ficará no repositório de desenvolvimento escolhido. Não mover código por esta preparação.

```text
Escritorio de Projetos/
  AGENTS.md, CONTEXTO.md, VERSION
  arquitetura/v2/             # requisitos, modelo, operação e segurança
  portfolios/saerj/           # registros oficiais reais
  portfolios/pessoal/         # domínio separado
  conselho/ideias/            # ideias ainda não promovidas
  desenvolvimento/
    contratos/openapi.json   # contrato atual; nem toda operação desenhada existe
    migrations/001_nucleo.sql
    migrations/002_bloqueios.sql
    local/                   # ambiente, replicação e ensaio legado
    servico/                 # núcleo, servidor local, cliente e casos de uso
    testes/                  # contrato, esquema, serviço e cenários
  .runtime/                  # privado, não versionar
```

```text
supersync/                   # raiz do repositório da aplicação
  manage.py, requirements.txt, Dockerfile, AGENTS.md
  supersync/                 # configuração, URLs e Celery
  usuarios/, accounts/       # módulos observados; mapeamento a confirmar
  central_associado/         # integração a avaliar, sem herança automática de acesso
  acordos_comerciais/, apuracao_contrato/, ...
  templates/, static/
  escritorio/                # PROPOSTO; ainda não criado por esta entrega
```

## Execução atual do piloto Windows

Comandos existentes, na raiz do Escritório, com banco já preparado:

```powershell
$env:ESCRITORIO_PG_BIN="C:\Program Files\PostgreSQL\17\bin"
python desenvolvimento/local/replicar.py diagnosticar
python desenvolvimento/local/replicar.py verificar
python desenvolvimento/local/replicar.py servir
```

A pasta bin deve corresponder à instalação real. API local em loopback; não é página inicial gráfica. Serviço ocupa o terminal. Em outra janela, na mesma raiz:

```powershell
python desenvolvimento/servico/cliente.py consultar --portfolio demo_escritorio
```

A ACL pode impedir o usuário isolado do Codex de ler credenciais: executar no usuário proprietário sem alargar acesso indiscriminadamente. Preparar ambiente vazio somente para demonstração; não executar seed vazio antes de restauração pretendida.

## Ensaio legado

```powershell
.runtime\servico-venv\Scripts\python.exe desenvolvimento/local/ensaiar_legado.py --executar
```

Cada execução cria banco isolado novo, não sincroniza nem atualiza ensaio anterior. Escopo: projetos canônicos, tarefas tabulares e fontes Markdown sob `portfolios/saerj`; inclui históricos/decisões como fontes integrais, sem convertê-los em eventos/aprovações nativos. Verifica contagens, campos e bytes/checksums, mas não constitui restauração completa do ensaio. Ensaio não é exposto automaticamente pelo serviço do piloto.

## Ordem sugerida de implementação

1. Confirmar escopo MVP, arquitetura, repositório de destino e responsável.
2. Provar configuração local mínima do SuperSync sem acessar segredos/serviços de produção.
3. Definir identidade/autorização, contrato de integração e propriedade do schema.
4. Criar app/interface proposta e testes de autorização; preservar núcleo existente.
5. Validar consultas e mutações ponta a ponta, depois anexos/reuniões/bloqueios/aceite.
6. Concluir importador com conciliação de pessoas/estados/IDs, ideias, anexos e fontes.
7. Validar restauração externa, homologação e corte de autoridade aprovado.

Nenhum framework novo foi scaffoldado e nenhum arquivo de implementação do SuperSync foi alterado por estes documentos.

## Fontes e validade

Preparado em 08/10/2026 para o Escritório v2 com integração proposta ao SuperSync. Documento de preparação: não promove a iniciativa a projeto nem autoriza produção.

Fontes no Escritório: `CONTEXTO.md`, `AGENTS.md`, `arquitetura/v2/{especificacao,modelo-dados,implementacao-supersync,operacao-gestor,seguranca-chat}.md`, `desenvolvimento/contratos/openapi.json`, `desenvolvimento/migrations/`, `desenvolvimento/servico/`, `portfolios/saerj/projetos/supersync/desenvolvimento.md`. Fontes de implementação consultadas em `C:/Users/fabri/Projetos/supersync`: `AGENTS.md`, `requirements.txt`, `Dockerfile` e inventário de diretórios; HEAD observado `12f6dae`. Não foram lidos .env, dumps ou segredos, nem validados autenticação, infraestrutura remota ou comportamento do checkout completo. A inspeção documental anterior cita `bba8f83`; não a tratar como HEAD atual.
