# Camada de Desenvolvimento — SuperSync

**Navegação:** [Projeto](projeto.md) · [Módulos](modulos.md) · [Governança](governanca.md) · [Tarefas](tarefas.md) · [Validação de sprint](../../../../modelos/validacao-sprint.md)

## Identificação

**Repositório:** https://github.com/Liencourt/supersync.git  
**Caminho local de referência:** `C:\Users\fabri\Projetos\supersync`  
**Branch principal remota:** `master`  
**Revisão observada:** `origin/master` em `f7ddcb31d8d496a4c36e545c6310700c4af251f1`
**Data da inspeção:** 14/10/2026

O checkout foi atualizado por fast-forward de `8c0478c` para `bba8f83` e validado limpo, com `master` e `origin/master` apontando para o mesmo commit. Foram incorporados 63 commits, com 193 arquivos alterados, 12.849 inserções e 801 remoções. A branch `feature/lojas-inconformidades-ux` foi preservada e permanece sincronizada com seu remoto.

## Stack implementada

| Componente | Tecnologia / versão | Evidência |
|---|---|---|
| Aplicação | Python 3.11+ e Django 5.2.7 | `README.md`; `requirements.txt` |
| API | Django REST Framework 3.16.1 | `requirements.txt` |
| Banco de dados | PostgreSQL; conectores para Cloud SQL e BigQuery | `README.md`; `requirements.txt`; migrations dos apps |
| Processamento assíncrono | Celery 5.6.2 | `AGENTS.md`; `requirements.txt`; `supersync/celery.py` |
| Interface | Templates Django com Bootstrap/Tabler e ativos estáticos | `AGENTS.md`; `templates/`; `static/` |
| Infraestrutura | Dockerfile e serviços Google Cloud | `Dockerfile`; `gcp_services/`; `requirements.txt` |

## Estrutura funcional observada

Foram observados módulos de usuários e autenticação, contratos e acordos comerciais, apuração de contratos e grades, auditoria, envio de dados, relatórios, pricing, social listening, lojas, inconformidades, dashboard, serviços GCP e a Central do Associado. Na Central, a revisão observada contém portal externo, cerca de acesso, gestão de usuários, recuperação de senha, painel SAERJ, lojas, auditoria e justificativas de cobrança, grades e resumo de contratos. A frente específica de ruptura de promoções ainda não possui evidência conclusiva na Central.

## Modelo de dados

O modelo é distribuído entre apps Django e possui migrations versionadas. Foram observados domínios de usuários e associados, contratos e apurações, grades e distribuições, envio de dados, pricing, social listening, lojas, perfis, inconformidades, notificações e relatórios. A referência canônica detalhada são os arquivos `models.py`, pacotes `models/` e migrations do repositório de desenvolvimento.

## Replicação local

| Critério                            | Status         | Evidência / lacuna                                                                                                  |
| ----------------------------------- | -------------- | ------------------------------------------------------------------------------------------------------------------- |
| Dependências versionadas            | 🟡 Atenção     | `requirements.txt` existe, mas contém dependências sem versão fixa e combina conectores alternativos.               |
| Configuração não secreta de exemplo | 🔴 Intervenção | Não foi localizado `.env.example`; o README relata valores sensíveis hardcoded.                                     |
| Banco, migrations e seed            | 🟡 Atenção     | Migrations existem; processo seguro e mínimo de seed não está documentado de forma conclusiva.                      |
| Execução documentada                | 🟡 Atenção     | README e AGENTS possuem comandos, mas o README está desatualizado em relação aos módulos e ao Dockerfile existente. |
| Testes reproduzíveis                | 🟢 Adequado    | `python manage.py test --noinput` executou 551 testes com sucesso em 24/09/2026; `manage.py check` não apontou problemas. |

## Riscos e lacunas

- Arquivos gerados do Celery Beat estão versionados e podem causar ruído ou divergência operacional.
- O README descreve arquitetura e rotas antigas, incompatíveis com a quantidade atual de módulos.
- Existem `.env`, bancos e dumps no diretório local; não foram abertos e seu rastreamento deve permanecer bloqueado.
- A `master` avançou 63 commits desde `8c0478c`; a revisão `bba8f83` passou na suíte automatizada e na validação funcional, restando a aprovação executiva.
- Não há vínculo padronizado entre sprint, requisito, commit, teste e aceite.

## Próximas verificações

- registrar `bba8f83` ou uma revisão posterior como baseline apresentada à aprovação executiva;
- repetir instalação, migrations e testes em ambiente limpo; a execução atual usou o ambiente local existente;
- criar configuração de exemplo sem segredos e instruções atuais de reprodução;
- inventariar módulos em produção e desenvolvimento;
- registrar a aprovação de Marcelo Rebelo e abrir o ciclo seguinte para as melhorias sugeridas.

## Atualização técnica — 14/10/2026 (versão 2 da inspeção)

Pedido original: “atualizar o supersync com as ultimas atualização do git”. Fonte: remoto `origin/master`, confirmado por `git ls-remote` e atualizado por `git fetch origin master`; revisão `f7ddcb3`, de 14/10/2026 às 09h51 (America/Sao_Paulo). Inspeção do histórico, diferenças e arquivos versionados, sem alteração de produção ou aplicação de migrations. O checkout local permanece em `12f6dae`; a inspeção usou diretamente os objetos de `origin/master`.

Desde a baseline `bba8f83`, há 78 commits (incluindo merges), 1.849 arquivos alterados, 12.674 inserções e 87.120 remoções. A contagem inclui a retirada de ativos de bibliotecas sem uso; não representa quantidade de funcionalidades entregues. A descrição de fast-forward e dos 551 testes acima é evidência histórica de 24/09, não validação desta revisão.

| Frente | Implementação observada | Evidência no repositório SuperSync |
|---|---|---|
| Evasão e cobrança | Justificativa e decisão por produto da nota; filtros múltiplos e detalhamento por loja/produto; cinco abas de cobrança com níveis próprios; análise e decisão sem recarregar a página | `central_associado/services/burlas.py`, `views/cobrancas.py`, testes de auditoria/burlas; commits `e5a7b7b`, `11a41ad`, `d51d50a` |
| Competência mensal | Prazo de justificativa, fechamento/reabertura com histórico, lembretes, acesso de comprador, apuração agendada e processamento em segundo plano | `central_associado/services/fechamento.py`, migrations `0011` e `0012`, `tests/test_fechamento.py`; commits `81be1a5`, `e2ee0b9` |
| Visão do gestor | Consulta de progresso, equipe, devolutivas e pendências, com os filtros da evasão | `central_associado/views/visao_gestor.py`, `services/visao_gestor.py`, `tests/test_visao_gestor.py`; commit `2f4220c` |
| Grades e contratos | Espelho da grade, observação e filtro do comprador, busca/paginação; impostos e aniversário no resumo de contratos | Serviços, views e testes de grades/resumo; commits `5b64863`, `8432069`, `a8e01d7`, `de43b13` |
| Acordos e apuração | Distribuidor autorizado tratado separadamente dos ofensores; notas com aniversário/venda de dados e consideração em lote | Migration `0026_distribuidor_autorizado`, services e testes de acordos/apuração; commits `c1ebeb9`, `c83d571`, `b91e7bc` |
| Envio de Dados | API autenticada por chave, gestão de clientes/chaves e documentação; exigência de login nas telas internas | `envio_dados/api/`, `views_clientes_api.py`, migration `0010_api_dados`, testes; commits `80fea92`, `042416d` |
| Relatórios | Compras por fornecedor, concentração de associados por fornecedor, quantidade/valor por produto, atributos mercadológicos e ajustes de estoque; inclusão do Cruzeiro do Sul na concentração e evasão | `relatorios/relatorios_sqls.py`, testes, `auditoria_contratos/sqls.py`; commits `d732a61`, `c1beda1`, `8f92236`, `300a37c`, `fd9d88a`, `82f8bc3`, `7d6908d` |
| Interface e ativos | Menu Gestão SAERJ, ativos com hash e retirada de bibliotecas sem uso | Templates e storage; commits `db03944`, `b34758f`, `7e010eb` |

Limites: testes novos estão versionados, mas a suíte da revisão `f7ddcb3` não foi executada nesta inspeção. Homologação, aplicação das migrations, configuração do agendamento e publicação dessas evoluções em produção não foram verificadas. Preservada a aprovação da Central em 28/09; ela não concede automaticamente aceite às mudanças posteriores. A presença de código de análise e relatórios não conclui SS-016 a SS-019.

Próxima verificação: executar a suíte desta revisão em ambiente isolado, validar migrations e serviços assíncronos e conciliar as melhorias com SS-013 antes de registrar homologação/publicação.
