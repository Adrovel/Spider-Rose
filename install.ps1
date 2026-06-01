$ErrorActionPreference = "Stop"

$RepoUrl = "git+https://github.com/Adrovel/Spider-Rose.git"

function Test-Command($Name) {
    $null -ne (Get-Command $Name -ErrorAction SilentlyContinue)
}

if (-not (Test-Command "py") -and -not (Test-Command "python")) {
    Write-Error "Spider Rose needs Python 3.11+ installed. Install Python from https://www.python.org/downloads/windows/ and rerun this command."
}

$Python = if (Test-Command "py") { "py" } else { "python" }

& $Python -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 11) else 1)"
if ($LASTEXITCODE -ne 0) {
    Write-Error "Spider Rose needs Python 3.11+."
}

if (-not (Test-Command "pipx")) {
    Write-Host "pipx not found. Installing pipx for this user..."
    & $Python -m pip install --user pipx
    & $Python -m pipx ensurepath
}

$Pipx = if (Test-Command "pipx") { "pipx" } else { "$env:APPDATA\Python\Scripts\pipx.exe" }

& $Pipx install --force $RepoUrl

Write-Host ""
Write-Host "Spider Rose installed."
Write-Host "Run it with:"
Write-Host "  spiderrose"
Write-Host ""
Write-Host "If your shell cannot find spiderrose, restart PowerShell and try again."
