<#
.SYNOPSIS
    Cria um ambiente virtual Python, instala dependências e valida a instalação.
    Funciona em qualquer máquina (Windows, Linux, macOS com PowerShell) sem snapshot.
    Leia

.EXAMPLE
    .\setup-env.ps1
    .\setup-env.ps1 -PythonVersion 3.12 -VenvName .iaenv -Recreate
    .\setup-env.ps1 -Torch cpu
    .\setup-env.ps1 -Torch cu128 -TorchVersion 2.8.0
    .\setup-env.ps1 -Torch none
#>
[CmdletBinding()]
param(
    # Versão do Python (major.minor). Se não existir, o script avisa.
    [string]$PythonVersion = "3.12",
    # Nome da pasta do ambiente virtual
    [string]$VenvName = ".venv",
    # Arquivo de dependências
    [string]$Requirements = "requirements.txt",
    # "auto" = detecta GPU NVIDIA e escolhe o build; "cpu"; "none" = não instala torch;
    # ou uma tag explícita, ex.: "cu128"
    [string]$Torch = "auto",
    # Versão exata do torch (opcional). Vazio = mais recente do índice escolhido
    [string]$TorchVersion = "",
    # Também instala torchvision e torchaudio
    [switch]$WithTorchExtras,
    # Apaga o ambiente existente e recria do zero
    [switch]$Recreate
)

$ErrorActionPreference = "Stop"

# Acentos corretos no console e na saída do Python
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch {}
$env:PYTHONUTF8       = "1"
$env:PYTHONIOENCODING = "utf-8"

$IsWin       = ($env:OS -eq "Windows_NT")
$IsMac       = (-not $IsWin) -and ((uname) -eq "Darwin")
$ProjectRoot = if ($PSScriptRoot) { $PSScriptRoot } else { (Get-Location).Path }
$VenvPath    = Join-Path $ProjectRoot $VenvName
$ReqPath     = Join-Path $ProjectRoot $Requirements
$PythonExe   = if ($IsWin) { Join-Path $VenvPath "Scripts\python.exe" } else { Join-Path $VenvPath "bin/python" }

# Isola o pip de configurações globais da máquina
$env:PIP_DISABLE_PIP_VERSION_CHECK = "1"
foreach ($v in "PIP_INDEX_URL","PIP_EXTRA_INDEX_URL","PIP_EXTRA_INDEX_URLS","PIP_TRUSTED_HOST","PIP_CONFIG_FILE") {
    Remove-Item "Env:$v" -ErrorAction SilentlyContinue
}

function Write-Step($Message) { Write-Host "`n==> $Message" -ForegroundColor Cyan }
function Stop-Setup($Message) { Write-Host "`nERRO: $Message" -ForegroundColor Red; exit 1 }
function Assert-Ok($Message)  { if ($LASTEXITCODE -ne 0) { Stop-Setup $Message } }

Set-Location $ProjectRoot

# ------------------------------------------------------------
# 1. Localiza o Python
# ------------------------------------------------------------
Write-Step "Procurando Python $PythonVersion"

$PyExe  = $null
$PyArgs = @()
$candidates = @(
    @{ Exe = "py";                     Args = @("-$PythonVersion") },
    @{ Exe = "python$PythonVersion";   Args = @() },
    @{ Exe = "python3";                Args = @() },
    @{ Exe = "python";                 Args = @() }
)
foreach ($c in $candidates) {
    if (-not (Get-Command $c.Exe -ErrorAction SilentlyContinue)) { continue }
    $ver = & $c.Exe @($c.Args) -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>$null
    if ($LASTEXITCODE -eq 0 -and "$ver".Trim() -eq $PythonVersion) {
        $PyExe = $c.Exe; $PyArgs = $c.Args; break
    }
}
if (-not $PyExe) {
    Stop-Setup "Python $PythonVersion não encontrado. Instale-o ou use -PythonVersion com a versão disponível."
}
Write-Host "Python selecionado: $PyExe $($PyArgs -join ' ')"

# ------------------------------------------------------------
# 2. Cria o ambiente virtual
# ------------------------------------------------------------
Write-Step "Preparando ambiente virtual ($VenvName)"

if (Test-Path $VenvPath) {
    if ($Recreate) {
        try { Remove-Item $VenvPath -Recurse -Force }
        catch { Stop-Setup "Não foi possível remover $VenvName. Feche terminais/VS Code que o usam. $($_.Exception.Message)" }
    } else {
        Write-Host "Ambiente já existe, será reutilizado (use -Recreate para recriar)."
    }
}
if (-not (Test-Path $PythonExe)) {
    & $PyExe @PyArgs -m venv $VenvPath
    Assert-Ok "Falha ao criar o ambiente virtual."
}
Write-Host "Python no venv: $(& $PythonExe --version)"

Write-Step "Atualizando pip"
& $PythonExe -m pip --isolated install --upgrade pip
Assert-Ok "Falha ao atualizar o pip. Verifique a conexão."

# ------------------------------------------------------------
# 3. Instala PyTorch (se pedido)
# ------------------------------------------------------------
function Get-DriverCuda {
    if (-not (Get-Command nvidia-smi -ErrorAction SilentlyContinue)) { return $null }
    $out = (& nvidia-smi 2>$null | Out-String)
    if ($out -match 'CUDA Version:\s*(\d+)\.(\d+)') { return [version]"$($Matches[1]).$($Matches[2])" }
    return $null
}

function Test-IndexExists($Url) {
    try {
        $r = Invoke-WebRequest -Uri "$Url/torch/" -Method Head -UseBasicParsing -TimeoutSec 15
        return ($r.StatusCode -eq 200)
    } catch { return $false }
}

$TorchBackend = $Torch.ToLower()
$TorchIndex   = $null   # $null = PyPI padrão

if ($TorchBackend -ne "none") {
    Write-Step "Definindo build do PyTorch"

    if ($TorchBackend -eq "auto") {
        $driverCuda = Get-DriverCuda
        if ($driverCuda) {
            Write-Host "GPU NVIDIA detectada (driver suporta até CUDA $driverCuda)."
            $known = "13.2","13.0","12.9","12.8","12.6","12.4","12.1","11.8"
            $TorchBackend = "cpu"
            foreach ($k in $known) {
                if ([version]$k -gt $driverCuda) { continue }
                $tag = "cu" + ($k -replace '\.', '')
                if (Test-IndexExists "https://download.pytorch.org/whl/$tag") { $TorchBackend = $tag; break }
            }
        } else {
            Write-Host "Nenhuma GPU NVIDIA/driver detectada, usando build CPU."
            $TorchBackend = "cpu"
        }
    }

    if ($TorchBackend -eq "cpu") {
        if (-not $IsMac) { $TorchIndex = "https://download.pytorch.org/whl/cpu" }
    } else {
        $TorchIndex = "https://download.pytorch.org/whl/$TorchBackend"
    }
    Write-Host "Backend: $TorchBackend  |  Índice: $(if ($TorchIndex) { $TorchIndex } else { 'PyPI' })"

    $pkgs = @($(if ($TorchVersion) { "torch==$TorchVersion" } else { "torch" }))
    if ($WithTorchExtras) { $pkgs += "torchvision", "torchaudio" }

    Write-Step "Instalando $($pkgs -join ', ')"
    if ($TorchIndex) {
        & $PythonExe -m pip --isolated install --index-url $TorchIndex @pkgs
    } else {
        & $PythonExe -m pip --isolated install @pkgs
    }
    Assert-Ok "Falha ao instalar PyTorch ($TorchBackend). Confira se o build existe para este Python/SO em $TorchIndex."
}

# ------------------------------------------------------------
# 4. Instala as demais dependências
# ------------------------------------------------------------
Write-Step "Instalando $Requirements"

if (-not (Test-Path $ReqPath)) {
    Write-Host "Aviso: $Requirements não encontrado, pulando." -ForegroundColor Yellow
} else {
    # Remove linhas torch/torchvision/torchaudio para não sobrescrever o build escolhido
    $filtered = Get-Content $ReqPath | Where-Object { $_ -notmatch '^\s*(torch|torchvision|torchaudio)\s*([=<>!~;@\[]|$)' }
    if ($TorchBackend -eq "none") { $filtered = Get-Content $ReqPath }
    $tmpReq = Join-Path ([System.IO.Path]::GetTempPath()) "req-$([guid]::NewGuid().ToString('N')).txt"
    Set-Content -Path $tmpReq -Value $filtered -Encoding UTF8
    try {
        & $PythonExe -m pip --isolated install -r $tmpReq
        Assert-Ok "Falha ao instalar as dependências do projeto."
    } finally {
        Remove-Item $tmpReq -ErrorAction SilentlyContinue
    }
}

# ------------------------------------------------------------
# 5. Validações
# ------------------------------------------------------------
Write-Step "Verificando conflitos de dependências (pip check)"
& $PythonExe -m pip --isolated check
Assert-Ok "Conflitos de dependências encontrados."

if (Test-Path $ReqPath) {
    Write-Step "Verificando se todos os pacotes do requirements estão instalados"
    $checkReq = @'
import sys, re
import importlib.metadata as md

raw = open(sys.argv[1], "rb").read()
if raw.startswith((b"\xff\xfe", b"\xfe\xff")):
    text = raw.decode("utf-16")
else:
    text = raw.decode("utf-8-sig")

missing = []
for line in text.splitlines():
    line = line.split("#")[0].strip()
    if not line or line.startswith(("-", "http", "git+", ".")):
        continue
    name = re.split(r"[=<>!~;@\[\s]", line, maxsplit=1)[0]
    try:
        print(f"  {name} {md.version(name)}")
    except md.PackageNotFoundError:
        missing.append(name)

if missing:
    print("FALTANDO:", ", ".join(missing))
    sys.exit(1)
print("Todos os pacotes presentes: OK")
'@
    $checkReq | & $PythonExe - $ReqPath
    Assert-Ok "Há pacotes do requirements que não foram instalados."
}

if ($TorchBackend -ne "none") {
    Write-Step "Validando PyTorch"
    $env:EXPECTED_BACKEND = $TorchBackend
    $env:EXPECTED_TORCH   = $TorchVersion
    $checkTorch = @'
import os, sys
import torch

backend  = os.environ.get("EXPECTED_BACKEND", "")
expected = os.environ.get("EXPECTED_TORCH", "")

print("PyTorch:", torch.__version__)
print("Build CUDA:", torch.version.cuda)

if expected and not torch.__version__.startswith(expected):
    print(f"ERRO: versão esperada {expected}, obtida {torch.__version__}")
    sys.exit(3)

if backend.startswith("cu") and torch.version.cuda is None:
    print("ERRO: era esperado um build CUDA, mas o torch instalado é CPU.")
    sys.exit(4)

if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))
    x = torch.randn(1024, 1024, device="cuda")
    (x @ x).sum().item()
    print("Teste na GPU: OK")
elif backend.startswith("cu"):
    print("AVISO: build CUDA instalado, mas a GPU ainda não está utilizável (driver ausente ou antigo).")
    sys.exit(10)
else:
    print("Build CPU: OK")
'@
    $checkTorch | & $PythonExe -
    $code = $LASTEXITCODE
    Remove-Item Env:EXPECTED_BACKEND, Env:EXPECTED_TORCH -ErrorAction SilentlyContinue
    if ($code -eq 10) {
        Write-Host "Esperado se o driver NVIDIA será instalado depois. Rode este script de novo ou teste manualmente após instalar o driver." -ForegroundColor Yellow
    } elseif ($code -ne 0) {
        Stop-Setup "A validação do PyTorch falhou (código $code)."
    }
}

# ------------------------------------------------------------
# 6. Fim
# ------------------------------------------------------------
Write-Step "Ambiente pronto"
Write-Host "Ambiente: $VenvPath" -ForegroundColor Green
Write-Host "Python:   $(& $PythonExe --version)"
if ($IsWin) { Write-Host "Ativar:   .\$VenvName\Scripts\Activate.ps1" }
else        { Write-Host "Ativar:   source ./$VenvName/bin/activate" }