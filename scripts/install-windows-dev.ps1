param()
$ErrorActionPreference = "Stop"
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$Target = Join-Path $env:LOCALAPPDATA "AuralynClickDev"
$Venv = Join-Path $Target ".venv"
New-Item -ItemType Directory -Force -Path $Target | Out-Null
if (-not (Test-Path (Join-Path $Venv "Scripts\python.exe"))) { python -m venv $Venv }
& (Join-Path $Venv "Scripts\python.exe") -m pip install --upgrade pip
& (Join-Path $Venv "Scripts\pip.exe") install -r (Join-Path $Root "requirements.txt")
Copy-Item -Recurse -Force (Join-Path $Root "src") $Target
$env:PYTHONPATH = (Join-Path $Target "src")
& (Join-Path $Venv "Scripts\python.exe") -m auralyn_click
