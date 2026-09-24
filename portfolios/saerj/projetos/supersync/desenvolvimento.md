# Camada de Desenvolvimento — SuperSync

**Navegação:** [Projeto](projeto.md) · [Módulos](modulos.md) · [Governança](governanca.md) · [Tarefas](tarefas.md) · [Validação de sprint](../../../../modelos/validacao-sprint.md)

## Identificação

**Repositório:** https://github.com/Liencourt/supersync.git  
**Caminho local de referência:** `C:\Users\fabri\Projetos\supersync`  
**Branch principal remota:** `master`  
**Revisão observada:** `master` em `bba8f83`
**Data da inspeção:** 24/09/2026

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
