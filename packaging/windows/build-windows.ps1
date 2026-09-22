param([switch]$NoInstaller)
$ErrorActionPreference = "Stop"
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$Release = Join-Path $Root "release"
$Version = (& python -c "import sys; sys.path.insert(0, r'$Root\src'); from auralyn_click import __version__; print(__version__)").Trim()
New-Item -ItemType Directory -Force -Path $Release | Out-Null

python -m pip install --upgrade pip
python -m pip install -r (Join-Path $Root "requirements.txt") pyinstaller

$sep = ";"
python -m PyInstaller --noconfirm --clean --windowed `
  --name AuralynClick `
  --icon (Join-Path $Root "assets\auralyn-click.ico") `
  --paths (Join-Path $Root "src") `
  --add-data ((Join-Path $Root "src\auralyn_click\assets") + "$sep" + "auralyn_click\assets") `
  --hidden-import pynput.keyboard._win32 `
  --hidden-import pynput.mouse._win32 `
  (Join-Path $Root "packaging\entry.py")

$Portable = Join-Path $Release "AuralynClick-$Version-Windows-x64-Portable.zip"
if (Test-Path $Portable) { Remove-Item $Portable -Force }
Compress-Archive -Path (Join-Path $Root "dist\AuralynClick\*") -DestinationPath $Portable
Write-Host "Portable build: $Portable"

if ($NoInstaller) { exit 0 }

$ISCC = @(
  "${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe",
  "$env:ProgramFiles\Inno Setup 6\ISCC.exe"
) | Where-Object { Test-Path $_ } | Select-Object -First 1

if (-not $ISCC) {
  Write-Host "Inno Setup 6 not found. Install it with: winget install JRSoftware.InnoSetup"
  Write-Host "Then run this script again to build the Setup.exe."
  exit 2
}

& $ISCC "/DMyAppVersion=$Version" "/DSourceRoot=$Root" (Join-Path $Root "packaging\windows\AuralynClick.iss")
Write-Host "Windows installer created in $Release"
