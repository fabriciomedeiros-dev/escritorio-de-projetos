"""Caminhos e proteção do runtime local em POSIX e Windows nativo."""
import os
import base64
from pathlib import Path
import shutil
import subprocess

WINDOWS = os.name == 'nt'


def venv_python(directory, windows=WINDOWS):
    return Path(directory) / ('Scripts/python.exe' if windows else 'bin/python')


def pg_directory():
    configured = os.environ.get('ESCRITORIO_PG_BIN')
    if configured:
        result = Path(configured)
        if not (result / ('initdb.exe' if WINDOWS else 'initdb')).is_file():
            raise RuntimeError('ESCRITORIO_PG_BIN não contém initdb; indique a pasta bin do PostgreSQL.')
        return result
    found = shutil.which('initdb')
    if found:
        return Path(found).parent
    candidates = [Path(p) for p in ('/opt/homebrew/opt/postgresql@14/bin', '/usr/local/opt/postgresql@14/bin', '/usr/lib/postgresql/14/bin')]
    if WINDOWS:
        candidates = [Path(os.environ.get('ProgramFiles', 'C:/Program Files')) / 'PostgreSQL/14/bin']
    for path in candidates:
        if (path / ('initdb.exe' if WINDOWS else 'initdb')).is_file():
            return path
    raise RuntimeError('Ferramentas PostgreSQL ausentes. Defina ESCRITORIO_PG_BIN; consulte REPLICACAO.md.')


def protect_runtime(root):
    """Protege somente .runtime deste repositório, antes de criar segredos."""
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True, mode=0o700)
    if not WINDOWS:
        os.chmod(root, 0o700)
        return
    # Define ACL explícita só para usuário atual e SYSTEM. Falha impede a preparação.
    command = "$p='" + str(root).replace("'", "''") + "'; $sid=[System.Security.Principal.WindowsIdentity]::GetCurrent().User; $current=Get-Acl -LiteralPath $p -ErrorAction Stop; if($current.GetOwner([System.Security.Principal.SecurityIdentifier]).Value -ne $sid.Value){ throw 'A pasta runtime pertence a outro usuario; propriedade deve ser corrigida antes de preparar.' }; $dir=New-Object System.IO.DirectoryInfo($p); $acl=$dir.GetAccessControl([System.Security.AccessControl.AccessControlSections]::Access); $acl.SetAccessRuleProtection($true,$false); foreach($existing in @($acl.Access)){ [void]$acl.RemoveAccessRuleSpecific($existing) };  foreach($s in @($sid,(New-Object System.Security.Principal.SecurityIdentifier('S-1-5-18')))){ $r=New-Object System.Security.AccessControl.FileSystemAccessRule($s,'FullControl','ContainerInherit,ObjectInherit','None','Allow'); $acl.AddAccessRule($r) }; $dir.SetAccessControl($acl)"
    result = subprocess.run(['powershell.exe', '-NoProfile', '-NonInteractive', '-OutputFormat', 'Text', '-EncodedCommand', base64.b64encode(command.encode('utf-16le')).decode('ascii')], capture_output=True, text=True)
    if result.returncode:
        detail = result.stderr.strip() if isinstance(result.stderr, str) else ''
        raise RuntimeError('Não foi possível restringir a ACL de .runtime no Windows; preparação interrompida.' + ('\n' + detail if detail else ''))
