# Camada de Desenvolvimento — SuperSync

**Navegação:** [Projeto](projeto.md) · [Módulos](modulos.md) · [Governança](governanca.md) · [Tarefas](tarefas.md) · [Validação de sprint](../../modelos/validacao-sprint.md)

## Identificação

**Repositório:** https://github.com/Liencourt/supersync.git  
**Caminho local de referência:** `C:\Users\fabri\Projetos\supersync`  
**Branch principal remota:** `master`  
**Revisão observada:** `master` em `8c0478c`
**Data da inspeção:** 16/09/2026

O checkout foi atualizado por fast-forward e validado limpo, com `master` e `origin/master` apontando para o mesmo commit. A branch `feature/lojas-inconformidades-ux` foi preservada e permanece sincronizada com seu remoto.

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

Foram observados módulos de usuários e autenticação, contratos e acordos comerciais, apuração de contratos e grades, auditoria, envio de dados, relatórios, pricing, social listening, lojas, inconformidades, dashboard, serviços GCP e a nova Central do Associado. Na Central, a revisão observada contém portal externo, cerca de acesso, gestão de usuários, painel SAERJ, lojas e auditoria de contratos. Grades estão preparadas nas permissões, mas registradas no próprio código como fase futura.

## Modelo de dados

O modelo é distribuído entre apps Django e possui migrations versionadas. Foram observados domínios de usuários e associados, contratos e apurações, grades e distribuições, envio de dados, pricing, social listening, lojas, perfis, inconformidades, notificações e relatórios. A referência canônica detalhada são os arquivos `models.py`, pacotes `models/` e migrations do repositório de desenvolvimento.

## Replicação local

| Critério                            | Status         | Evidência / lacuna                                                                                                  |
| ----------------------------------- | -------------- | ------------------------------------------------------------------------------------------------------------------- |
| Dependências versionadas            | 🟡 Atenção     | `requirements.txt` existe, mas contém dependências sem versão fixa e combina conectores alternativos.               |
| Configuração não secreta de exemplo | 🔴 Intervenção | Não foi localizado `.env.example`; o README relata valores sensíveis hardcoded.                                     |
| Banco, migrations e seed            | 🟡 Atenção     | Migrations existem; processo seguro e mínimo de seed não está documentado de forma conclusiva.                      |
| Execução documentada                | 🟡 Atenção     | README e AGENTS possuem comandos, mas o README está desatualizado em relação aos módulos e ao Dockerfile existente. |
| Testes reproduzíveis                | 🟡 Atenção     | A Central possui 106 testes automatizados identificados estaticamente; a suíte não foi executada nesta inspeção.    |
| Segredos fora do Git                | 🔴 Intervenção | `gcp_credencials.json` está versionado; validade e exposição não foram verificadas.                                 |

## Riscos e lacunas

- Possível exposição de credencial versionada; não se presume que ainda esteja válida.
- Arquivos gerados do Celery Beat estão versionados e podem causar ruído ou divergência operacional.
- O README descreve arquitetura e rotas antigas, incompatíveis com a quantidade atual de módulos.
- Existem `.env`, bancos e dumps no diretório local; não foram abertos e seu rastreamento deve permanecer bloqueado.
- A `master` contém 130 commits incorporados desde a revisão local anterior; a nova linha de base candidata é `8c0478c`, ainda pendente de validação formal.
- Não há vínculo padronizado entre sprint, requisito, commit, teste e aceite.

## Próximas verificações

- confirmar e tratar credenciais potencialmente expostas;
- confirmar `8c0478c` ou uma revisão posterior como baseline inicial;
- executar instalação, migrations, aplicação e testes em ambiente limpo;
- criar configuração de exemplo sem segredos e instruções atuais de reprodução;
- inventariar módulos em produção e desenvolvimento;
- identificar a sprint atual e aplicar `modelos/validacao-sprint.md`.
