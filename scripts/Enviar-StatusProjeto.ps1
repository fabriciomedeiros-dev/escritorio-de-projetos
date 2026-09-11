[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [Parameter(Mandatory = $true)]
    [ValidatePattern('^[a-z0-9][a-z0-9-]*$')]
    [string]$Projeto,

    [string[]]$Para,
    [string[]]$Cc,
    [string]$Assunto,
    [string]$Evento = 'status-executivo',
    [string]$ArquivoRelatorio,
    [switch]$Enviar,
    [ValidateSet('APROVADO')]
    [string]$Confirmacao
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function ConvertTo-AddressList {
    param([string[]]$Values)

    $addresses = foreach ($value in $Values) {
        if ([string]::IsNullOrWhiteSpace($value)) { continue }
        $value -split ';' | ForEach-Object { $_.Trim() } | Where-Object { $_ }
    }

    return @($addresses | Select-Object -Unique)
}

function Get-MarkdownValue {
    param(
        [string]$Content,
        [string]$Label
    )

    $escapedLabel = [regex]::Escape($Label)
    $match = [regex]::Match($Content, "(?m)^\*\*${escapedLabel}:\*\*\s*(.+?)\s*$")
    if ($match.Success) { return $match.Groups[1].Value.Trim() }
    return 'Não definido'
}

$repositoryRoot = Split-Path -Parent $PSScriptRoot
$projectPath = Join-Path $repositoryRoot "projetos\$Projeto\projeto.md"
$tasksPath = Join-Path $repositoryRoot "projetos\$Projeto\tarefas.md"
$localConfigPath = Join-Path $repositoryRoot 'config\comunicacao.local.json'
$localTokenPath = Join-Path $repositoryRoot 'config\zeptomail.token.local'

$localConfig = $null
if (Test-Path -LiteralPath $localConfigPath -PathType Leaf) {
    $localConfig = Get-Content -Raw -LiteralPath $localConfigPath -Encoding UTF8 | ConvertFrom-Json
}

if (-not (Test-Path -LiteralPath $projectPath -PathType Leaf)) {
    throw "Projeto '$Projeto' não encontrado em '$projectPath'."
}

$projectContent = Get-Content -Raw -LiteralPath $projectPath -Encoding UTF8
$tasksContent = if (Test-Path -LiteralPath $tasksPath -PathType Leaf) {
    Get-Content -Raw -LiteralPath $tasksPath -Encoding UTF8
} else {
    'Nenhum arquivo de tarefas encontrado.'
}

$titleMatch = [regex]::Match($projectContent, '(?m)^# Projeto:\s*(.+?)\s*$')
$projectName = if ($titleMatch.Success) { $titleMatch.Groups[1].Value.Trim() } else { $Projeto }
$generalStatus = Get-MarkdownValue -Content $projectContent -Label 'Status geral'
$responsible = Get-MarkdownValue -Content $projectContent -Label 'Responsável'
$lastUpdate = Get-MarkdownValue -Content $projectContent -Label 'Última atualização'
$milestone = Get-MarkdownValue -Content $projectContent -Label 'Marco'
$milestoneDate = Get-MarkdownValue -Content $projectContent -Label 'Data'
$milestoneCondition = Get-MarkdownValue -Content $projectContent -Label 'Condição de conclusão'

$stateSection = [regex]::Match(
    $projectContent,
    '(?ms)^## 4\. Estado atual\s*(.+?)(?=^---\s*$|^##\s)'
)
$stateSummary = if ($stateSection.Success) { $stateSection.Groups[1].Value.Trim() } else { 'Não definido' }

$taskRows = @([regex]::Matches($tasksContent, '(?m)^\|\s*(SAC-\d+|T-\d+)\s*\|.*$') | ForEach-Object { $_.Value.Trim() })
$taskSummary = if ($taskRows.Count -gt 0) { $taskRows -join [Environment]::NewLine } else { 'Nenhuma tarefa registrada.' }

$referenceDate = Get-Date -Format 'dd/MM/yyyy'
if ([string]::IsNullOrWhiteSpace($Assunto)) {
    $Assunto = "Status do projeto - $projectName - $referenceDate"
}

$body = @"
STATUS DO PROJETO — $projectName
Data de referência: $referenceDate
Última atualização registrada: $lastUpdate

SAÚDE GERAL
$generalStatus

RESPONSÁVEL
$responsible

ESTADO ATUAL
$stateSummary

TAREFAS REGISTRADAS
$taskSummary

PRÓXIMO MARCO
$milestone
Data: $milestoneDate
Condição de conclusão: $milestoneCondition

Fonte: Escritório de Projetos — projetos/$Projeto/projeto.md
"@

if (-not [string]::IsNullOrWhiteSpace($ArquivoRelatorio)) {
    $reportPath = if ([System.IO.Path]::IsPathRooted($ArquivoRelatorio)) {
        $ArquivoRelatorio
    } else {
        Join-Path $repositoryRoot $ArquivoRelatorio
    }
    if (-not (Test-Path -LiteralPath $reportPath -PathType Leaf)) {
        throw "Relatório aprovado não encontrado em '$reportPath'."
    }
    $body = Get-Content -Raw -LiteralPath $reportPath -Encoding UTF8
}

$renderedMarkdown = ConvertFrom-Markdown -InputObject $body
$htmlBody = @"
<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<style>
body { font-family: Arial, Helvetica, sans-serif; color: #24292f; line-height: 1.55; max-width: 860px; margin: 24px auto; padding: 0 20px; }
h1 { font-size: 26px; border-bottom: 1px solid #d8dee4; padding-bottom: 10px; }
h2 { font-size: 20px; margin-top: 28px; }
li { margin: 6px 0; }
table { border-collapse: collapse; width: 100%; margin: 16px 0; }
th, td { border: 1px solid #d8dee4; padding: 8px; text-align: left; vertical-align: top; }
th { background: #f6f8fa; }
blockquote { border-left: 4px solid #d8dee4; color: #57606a; margin-left: 0; padding-left: 16px; }
</style>
</head>
<body>
$($renderedMarkdown.Html)
</body>
</html>
"@

$configuredTo = @()
$configuredCc = @()
$configuredFrom = $null
$configuredFromName = $null
if ($null -ne $localConfig) {
    $configuredFrom = $localConfig.zeptomail.fromAddress
    $configuredFromName = $localConfig.zeptomail.fromName
    $projectConfig = $localConfig.projects.$Projeto
    if ($null -ne $projectConfig) {
        $eventConfig = $projectConfig.$Evento
        if ($null -ne $eventConfig) {
            $configuredTo = @($eventConfig.to)
            $configuredCc = @($eventConfig.cc)
        }
    }
}

$toAddresses = @(ConvertTo-AddressList -Values $(if ($PSBoundParameters.ContainsKey('Para')) { $Para } elseif ($configuredTo.Count -gt 0) { $configuredTo } else { @($env:PMO_STATUS_TO) }))
$ccAddresses = @(ConvertTo-AddressList -Values $(if ($PSBoundParameters.ContainsKey('Cc')) { $Cc } elseif ($configuredCc.Count -gt 0) { $configuredCc } else { @($env:PMO_STATUS_CC) }))

if (-not $Enviar) {
    Write-Output "Assunto: $Assunto"
    Write-Output "Para: $($toAddresses -join '; ')"
    Write-Output "Cc: $($ccAddresses -join '; ')"
    Write-Output ''
    Write-Output $body
    Write-Output ''
    Write-Output 'Prévia concluída. Use -Enviar somente após validar conteúdo, destinatários e configuração do ZeptoMail.'
    return
}

if ($Confirmacao -ne 'APROVADO') {
    throw "Envio não autorizado. Depois de aprovar a prévia, execute novamente com -Enviar -Confirmacao APROVADO."
}

$zeptoToken = $env:PMO_ZEPTOMAIL_TOKEN
if ([string]::IsNullOrWhiteSpace($zeptoToken)) {
    $zeptoToken = [Environment]::GetEnvironmentVariable('PMO_ZEPTOMAIL_TOKEN', 'User')
}
if ([string]::IsNullOrWhiteSpace($zeptoToken) -and (Test-Path -LiteralPath $localTokenPath -PathType Leaf)) {
    $zeptoToken = (Get-Content -Raw -LiteralPath $localTokenPath -Encoding UTF8).Trim()
}
$zeptoFrom = if (-not [string]::IsNullOrWhiteSpace($env:PMO_ZEPTOMAIL_FROM)) { $env:PMO_ZEPTOMAIL_FROM } else { $configuredFrom }

$requiredSettings = @{
    PMO_ZEPTOMAIL_TOKEN = $zeptoToken
    PMO_ZEPTOMAIL_FROM = $zeptoFrom
}
$missingSettings = @($requiredSettings.GetEnumerator() | Where-Object { [string]::IsNullOrWhiteSpace([string]$_.Value) } | ForEach-Object { $_.Key })
if ($missingSettings.Count -gt 0) {
    throw "Configuração do ZeptoMail incompleta. Variáveis ausentes: $($missingSettings -join ', ')."
}
if ($toAddresses.Count -eq 0) {
    throw 'Nenhum destinatário informado. Use -Para ou PMO_STATUS_TO.'
}

$fromName = if (-not [string]::IsNullOrWhiteSpace($env:PMO_ZEPTOMAIL_FROM_NAME)) {
    $env:PMO_ZEPTOMAIL_FROM_NAME
} elseif (-not [string]::IsNullOrWhiteSpace($configuredFromName)) {
    $configuredFromName
} else {
    'Escritório de Projetos'
}

$payload = @{
    from = @{
        address = $zeptoFrom
        name = $fromName
    }
    to = @($toAddresses | ForEach-Object {
        @{ email_address = @{ address = $_ } }
    })
    subject = $Assunto
    htmlbody = $htmlBody
    track_clicks = $false
    track_opens = $false
}
if ($ccAddresses.Count -gt 0) {
    $payload.cc = @($ccAddresses | ForEach-Object {
        @{ email_address = @{ address = $_ } }
    })
}

$headers = @{
    Accept = 'application/json'
    Authorization = "Zoho-enczapikey $zeptoToken"
}
$endpoint = 'https://api.zeptomail.com/v1.1/email'

if ($PSCmdlet.ShouldProcess(($toAddresses -join '; '), "Enviar '$Assunto' pelo ZeptoMail")) {
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    $jsonBody = $payload | ConvertTo-Json -Depth 8
    $response = Invoke-RestMethod -Uri $endpoint -Method Post -Headers $headers -ContentType 'application/json; charset=utf-8' -Body ([Text.Encoding]::UTF8.GetBytes($jsonBody))
    Write-Output "Status enviado com sucesso pelo ZeptoMail para $($toAddresses -join '; ')."
    if ($null -ne $response) {
        $response | ConvertTo-Json -Depth 8
    }
}
