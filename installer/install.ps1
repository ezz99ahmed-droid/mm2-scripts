# MM2 Scripts installer — copies host, registers pipe, drops extensions
param(
    [string]$InstallDir = "$env:LOCALAPPDATA\mm2-scripts",
    [switch]$SkipBridge
)

$ErrorActionPreference = "Stop"
Write-Host "[mm2-scripts] installing to $InstallDir"

New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null
Copy-Item -Recurse -Force ".\src\*" $InstallDir
Copy-Item -Recurse -Force ".\extensions" $InstallDir
Copy-Item -Force ".\scripts\manifest.yaml" "$InstallDir\manifest.yaml"

if (-not $SkipBridge) {
    Push-Location executor
    dotnet publish -c Release -o "$InstallDir\executor"
    Pop-Location
}

Write-Host "[mm2-scripts] done. run: python -m mm2_host.cli boot --root `"$InstallDir`""