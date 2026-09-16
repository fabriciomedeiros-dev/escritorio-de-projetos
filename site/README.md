# Portal do Escritório de Projetos

O portal transforma os documentos Markdown canônicos deste repositório em um site Quartz estático e navegável.

## Arquitetura

- **Origem:** repositório privado no GitHub;
- **Gerador:** Quartz v5 fixado no commit `3dff48b5df6d84c9544a5ae19c8f2cbb01dc44e5`;
- **Hospedagem:** Cloudflare Pages;
- **Domínio:** `projetos.redesupermarket.com.br`;
- **Controle de acesso:** Cloudflare Access;
- **Diretório de saída:** `.quartz-build/public`.

O script `site/build.sh` cria uma cópia temporária do Quartz, inclui apenas o conteúdo gerencial aprovado e gera o site. A pasta temporária não é versionada.

## Configuração do Cloudflare Pages

| Campo | Valor |
|---|---|
| Branch de produção | `main` |
| Comando de build | `bash site/build.sh` |
| Diretório de saída | `.quartz-build/public` |
| Versão do Node | 22 ou superior |

## Segurança de publicação

Antes do primeiro envio de conteúdo:

1. criar o projeto Pages sem publicar os documentos;
2. proteger o endereço `*.pages.dev` com Cloudflare Access;
3. criar uma aplicação Access para `projetos.redesupermarket.com.br` com política de negação por padrão;
4. permitir apenas as identidades ou o domínio corporativo aprovados;
5. associar o domínio personalizado ao projeto;
6. executar e validar o primeiro deploy.

O site não deve expor credenciais, arquivos `.env`, configurações locais ou tokens. O script publica somente os arquivos e diretórios explicitamente listados.

