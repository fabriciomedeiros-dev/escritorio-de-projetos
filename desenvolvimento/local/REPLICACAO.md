# Replicar o Escritório v2 em outra máquina

Preparado em 04/10/2026. Instalação e restauração verificadas em macOS, Python 3.14 e PostgreSQL 14, em diretórios e clusters distintos. Linux/WSL tem caminhos compatíveis, mas não foi testado. Windows nativo não é suportado.

## Levar os arquivos

Copie os três arquivos de `.runtime/transferencias/`: código `.bundle`, dados `.zip` e checksum `.zip.sha256`. São privados; não versionar nem publicar o pacote de dados. O bundle contém código e documentação versionada. O ZIP contém o banco demonstrativo, objetos originais, revisões locais de reuniões e documentos de negócio ainda não commitados. Não inclui senhas, tokens, venv nem o diretório físico do PostgreSQL.

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
