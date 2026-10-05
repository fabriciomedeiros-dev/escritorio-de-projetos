# Replicar o Escritório v2 em outra máquina

Preparado em 04/10/2026. Instalação e restauração verificadas em macOS, Python 3.14 e PostgreSQL 14, em diretórios e clusters distintos. Linux/WSL tem caminhos compatíveis, mas não foi testado. Windows nativo tem instalação preparada; execução nesse sistema ainda pendente.

## Levar os arquivos

Copie os três arquivos de `.runtime/transferencias/`: código `.bundle`, dados `.zip` e checksum `.zip.sha256`. São privados; não versionar nem publicar o pacote de dados. O bundle contém código e documentação versionada. O ZIP contém o banco demonstrativo, objetos originais, revisões locais de reuniões e documentos de negócio ainda não commitados. Não inclui senhas, tokens, venv nem o diretório físico do PostgreSQL.

## Na outra máquina (Windows nativo — opção para Fabrício)

Use PowerShell comum, com Python 3.10 ou posterior e Git disponíveis. Não é necessário WSL. Python, PostgreSQL e ACL ainda precisam ser verificados no Windows real. O Git mantém LF por `.gitattributes`, preservando os checksums das migrações. Use uma pasta local NTFS do seu usuário, fora de OneDrive/pastas compartilhadas, por exemplo `$env:USERPROFILE\Projetos\transferencia-escritorio`, e copie nela os três pacotes.

O ZIP atual vem do PostgreSQL 14 e exige ferramentas 14. Se o PostgreSQL existente for de outra versão, instale os binários 14 lado a lado; não altere o serviço ou os bancos existentes. O piloto cria seu próprio cluster e não usa o servidor existente na porta 5432. Referência: [PostgreSQL para Windows](https://www.postgresql.org/download/windows/).

No PowerShell, entre na pasta dos pacotes:

```powershell
$env:ESCRITORIO_PG_BIN = "C:\Program Files\PostgreSQL\14\bin"
python --version
git --version
git clone escritorio-v2-codigo-2026-10-04.bundle escritorio-de-projetos
cd escritorio-de-projetos
python desenvolvimento/local/replicar.py diagnosticar
python desenvolvimento/local/replicar.py preparar --pacote ../escritorio-v2-dados-2026-10-04.zip
python desenvolvimento/local/replicar.py verificar
python desenvolvimento/local/replicar.py servir
```

Ajuste `ESCRITORIO_PG_BIN` para a instalação 14 real. Se o comando disponível for `py -3`, use-o no lugar de `python`. A venv será `.runtime/servico-venv/Scripts/python.exe`; não requer ativação nem mudança da política de execução do PowerShell. Reabra uma sessão e defina novamente `ESCRITORIO_PG_BIN` quando necessário.

O banco escuta somente em `127.0.0.1:55432`, com autenticação SCRAM e credenciais novas. Não abre acesso à rede nem registra serviço do Windows. Se a porta estiver ocupada, a inicialização falha; não pare outro banco para liberar a porta sem identificar seu uso. A preparação restringe a ACL de `.runtime` ao usuário atual e SYSTEM e interrompe se não conseguir aplicá-la. Não copie a pasta física de banco ou a venv do Mac.

Depois de `verificar` passar, mantenha `servir` aberto e abra a pasta no agente de desenvolvimento. Para parar o banco próprio:

```powershell
python desenvolvimento/local/ambiente.py stop
```

Para exportar uma fotografia nova no Windows, com as ferramentas configuradas:

```powershell
.runtime/servico-venv/Scripts/python.exe desenvolvimento/local/transferir.py exportar --pacote ../novo-pacote.zip
```

Fontes técnicas: [conexões PostgreSQL](https://www.postgresql.org/docs/14/runtime-config-connection.html), [Set-Acl](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.security/set-acl). As checagens simuladas e a regressão macOS não substituem `verificar` no computador do trabalho.

## Na outra máquina (Windows com WSL 2)

Roteiro preparado, ainda sem execução em Windows. Escolhemos Ubuntu 22.04 para usar Python 3.10 e PostgreSQL 14 disponíveis nessa distribuição. Requer Windows compatível com WSL 2 e permissão para instalar seus componentes. Se já houver outra distribuição, não remova nem substitua seus dados.

No PowerShell como administrador:

```powershell
wsl --install -d Ubuntu-22.04
```

Reinicie se solicitado, abra Ubuntu 22.04 e crie seu usuário Linux. Confira `wsl -l -v` no PowerShell; a distribuição deve usar versão 2. Referências: [Microsoft — instalar WSL](https://learn.microsoft.com/en-us/windows/wsl/install), [Ubuntu no WSL](https://ubuntu.com/wsl/docs/latest/howto/install-ubuntu-wsl2/), [PostgreSQL 14 no Ubuntu 22.04](https://packages.ubuntu.com/jammy-updates/postgresql-14).

Dentro do terminal Ubuntu:

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git postgresql-14 postgresql-client-14
mkdir -p ~/Projetos/transferencia-escritorio
cd ~/Projetos/transferencia-escritorio
explorer.exe .
```

A janela do Explorer mostra essa pasta Linux. Copie para ela os três arquivos `.bundle`, `.zip` e `.zip.sha256`. Mantenha o projeto no diretório Linux, para conservar permissões dos arquivos privados. Volte ao Ubuntu:

```bash
git clone escritorio-v2-codigo-2026-10-04.bundle escritorio-de-projetos
cd escritorio-de-projetos
python3 desenvolvimento/local/replicar.py diagnosticar
python3 desenvolvimento/local/replicar.py preparar --pacote ../escritorio-v2-dados-2026-10-04.zip
python3 desenvolvimento/local/replicar.py verificar
python3 desenvolvimento/local/replicar.py servir
```

Execute os scripts como usuário comum. O PostgreSQL criado pelo piloto é separado do cluster padrão instalado pelo Ubuntu. O serviço permanece aberto no terminal. Em outro terminal Ubuntu, use o agente para trabalhar nessa pasta; ele precisa executar comandos no WSL, inclusive para acessar o socket do banco. Neste roteiro WSL, execute os scripts dentro do Ubuntu; para Python nativo, use a seção Windows nativo. A integração específica do cliente Codex no Windows deverá ser conferida na máquina; o roteiro de banco/serviço não comprova essa integração.

Se alguma etapa falhar, guarde a saída e não avance às seguintes. `verificar` só confirma a instalação quando todos os testes terminarem com sucesso. Não use `preparar` sem pacote antes da restauração.

## Na outra máquina (macOS)

Instale os pré-requisitos se estiverem ausentes:

```bash
brew install python@3.14 postgresql@14 git
```

Referências oficiais: [Python](https://formulae.brew.sh/formula/python@3.14), [PostgreSQL](https://formulae.brew.sh/formula/postgresql@14). Em Linux/WSL, instale Python e PostgreSQL 14 com suas ferramentas completas; veja [PostgreSQL Ubuntu](https://www.postgresql.org/download/linux/ubuntu/). O pacote exige a mesma versão principal do banco de origem. PostgreSQL 14 é apenas a compatibilidade do piloto atual; a versão de produção ainda precisa ser homologada.

Na pasta que recebeu os três arquivos:

```bash
git clone escritorio-v2-codigo-2026-10-04.bundle escritorio-de-projetos
cd escritorio-de-projetos
python3 desenvolvimento/local/replicar.py diagnosticar
python3 desenvolvimento/local/replicar.py preparar --pacote ../escritorio-v2-dados-2026-10-04.zip
python3 desenvolvimento/local/replicar.py verificar
python3 desenvolvimento/local/replicar.py servir
```

Use um Python 3.10 ou posterior; 3.14 foi validado. Se `python3` não apontar para o instalado, use o executável `python3.14` do Homebrew. A preparação cria a venv, instala as versões fixadas, inicializa o banco local, aplica migrações, restaura e confere o conteúdo. Precisa de internet para instalar dependências. Não execute como root.

Mantenha o último comando aberto: ele serve a API local em `127.0.0.1:8765`. Abra a pasta no Codex ou outro agente e peça para ler `CONTEXTO.md`, `AGENTS.md` e `arquitetura/v2/operacao-gestor.md`. Identidades HTTP continuam sintéticas; documentos Markdown continuam oficiais. Configure os conectores tl;dv/agenda novamente na nova máquina: autenticações não são transportadas.

## Instalação vazia

Para testes novos, execute `preparar` sem `--pacote`. Não faça isso antes de restaurar: a restauração recusa uma base ocupada e não apaga registros. A repetição da preparação preserva o ambiente existente. Uma restauração interrompida pode ser retomada com o mesmo pacote e marcador em `.runtime/replicacao/`; divergências são recusadas.

## Gerar uma fotografia atualizada

Com o banco de origem iniciado e as ferramentas PostgreSQL no PATH:

```bash
.runtime/servico-venv/bin/python desenvolvimento/local/transferir.py exportar --pacote /caminho/novo-pacote.zip
```

Use outro nome: exportações existentes não são sobrescritas. O checksum acompanha o ZIP e deve ser copiado junto. A ferramenta confere hashes, contagens e originais; mantém IDs, versões e histórico e gera credenciais novas no destino. Metadados originais de reuniões podem mencionar caminhos da máquina de origem; as fontes estão preservadas nas pastas relativas restauradas.

Esta transferência é uma fotografia, não sincronização entre bancos locais. Depois da cópia, alterações em cada computador divergem. A operação compartilhada dependerá do serviço central. O pacote no mesmo computador também não comprova proteção independente: copie-o para o destino; backup contínuo e recuperação agendada continuam pendentes.
