# Envio de status no Windows com ZeptoMail

O script `Enviar-StatusProjeto.ps1` lê o estado atual de um projeto e prepara um e-mail de status. Relatórios aprovados devem seguir `modelos/relatorio-status.md`; o Markdown é convertido em HTML antes do envio pelo ZeptoMail. Por padrão o script apenas exibe uma prévia; o envio real exige `-Enviar` e a configuração da API do ZeptoMail.

## Configuração local

Copie `config/comunicacao.example.json` para `config/comunicacao.local.json` e preencha remetente e destinatários. O arquivo local é ignorado pelo Git. Os grupos devem corresponder aos públicos aprovados em `portfolios/<portfolio>/projetos/<projeto>/comunicacao.md`. As configurações são separadas por portfólio para impedir mistura de destinatários.

```powershell
Copy-Item .\config\comunicacao.example.json .\config\comunicacao.local.json
notepad .\config\comunicacao.local.json
```

Grave a Send API key como variável do usuário do Windows. Execute este comando diretamente em seu PowerShell, sem publicar o token em conversas ou no Git:

```powershell
[Environment]::SetEnvironmentVariable("PMO_ZEPTOMAIL_TOKEN", "COLE_A_SEND_API_KEY", "User")
```

O valor deve conter somente a Send API key, sem o prefixo `Zoho-enczapikey`. O remetente deve pertencer a um domínio validado no Agent do ZeptoMail.

### Execução pelo chat do Codex no Windows

O processo isolado usado pelo chat pode não enxergar variáveis gravadas no perfil do usuário do Windows. Nesse caso, crie `config/zeptomail.token.local`, cole somente a Send API key em uma única linha e salve. Esse arquivo é ignorado pelo Git e não deve ser aberto, exibido ou incluído em logs durante as operações do Escritório.

```powershell
notepad .\config\zeptomail.token.local
```

## Pré-visualização

```powershell
.\scripts\Enviar-StatusProjeto.ps1 -Portfolio saerj -Projeto sac-supermarket
```

Para revisar um relatório criado a partir do modelo:

```powershell
.\scripts\Enviar-StatusProjeto.ps1 -Portfolio saerj -Projeto sac-supermarket -ArquivoRelatorio ".\portfolios\saerj\projetos\sac-supermarket\comunicacoes\2026-09-10-status.md"
```

Também é possível informar destinatários apenas para validar a composição, sem enviar:

```powershell
.\scripts\Enviar-StatusProjeto.ps1 -Portfolio saerj -Projeto sac-supermarket -Para "pessoa@exemplo.com"
```

## Envio

O envio exige confirmação explícita depois da revisão da prévia:

```powershell
.\scripts\Enviar-StatusProjeto.ps1 -Portfolio saerj -Projeto sac-supermarket -ArquivoRelatorio ".\portfolios\saerj\projetos\sac-supermarket\comunicacoes\2026-09-10-status.md" -Enviar -Confirmacao APROVADO
```

O script envia uma requisição HTTPS para `https://api.zeptomail.com/v1.1/email`, usando o cabeçalho `Authorization: Zoho-enczapikey <Send API key>`. Ele interrompe o envio se faltar configuração, destinatário, confirmação explícita, portfólio ou projeto. O parâmetro `-Portfolio` é obrigatório e restringe a leitura à pasta correspondente. O token é usado somente em memória durante a execução.

## Fluxo pelo chat

1. Solicite: “Prepare o status do SAC para envio”.
2. O Escritório cria o relatório a partir de `modelos/relatorio-status.md`, consultando os dados oficiais, e exibe destinatários e conteúdo integral.
3. Revise o conteúdo e responda: “Aprovado, enviar”.
4. Somente após essa aprovação o Escritório envia exatamente o arquivo revisado com `-Enviar -Confirmacao APROVADO` e informa o resultado da API.
