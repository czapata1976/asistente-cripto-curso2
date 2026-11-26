#Requires -Version 5.1
<#
.SYNOPSIS
    Publica la rama DEV en el repositorio de GitLab del curso.

.DESCRIPTION
    Crea (o actualiza) la rama DEV en
    https://gitlab.com/profe.bryhan/asistente-cripto

    Seguridad:
    - El token se pide enmascarado (Read-Host -AsSecureString): no se muestra
      en pantalla ni queda en el historial de PowerShell.
    - Se usa una sola vez en memoria y se borra al terminar.
    - Se empuja contra una URL completa, NO contra un remote, así que el token
      no queda escrito en .git\config.
    - La rama de destino está fijada en el script: nunca se empuja main ni se
      toca la rama principal del profesor.

.PARAMETER Rama
    Rama local a publicar. Por defecto DEV.

.PARAMETER Destino
    Nombre de la rama en GitLab. Por defecto el mismo que -Rama.

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File .\scripts\publicar_dev.ps1

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File .\scripts\publicar_dev.ps1 -Rama main -Destino DEV
#>

param(
    [string]$Rama = 'DEV',
    [string]$Destino = 'DEV'
)

$ErrorActionPreference = 'Stop'

$RepoUrl = 'https://gitlab.com/profe.bryhan/asistente-cripto.git'
$Raiz = Split-Path -Parent $PSScriptRoot
Set-Location $Raiz

# Salvaguarda: no publicar sobre la rama principal del profesor.
if ($Destino -in @('main', 'master')) {
    throw "Por seguridad este script no empuja a '$Destino'. La rama principal del curso no se toca."
}

# Comprobar que la rama local exista.
& git rev-parse --verify --quiet "refs/heads/$Rama" | Out-Null
if ($LASTEXITCODE -ne 0) {
    throw "No existe la rama local '$Rama'. Crea una con: git checkout -b $Rama"
}

# Avisar si quedan cambios sin commitear.
$pendientes = (& git status --porcelain) -join "`n"
if ($pendientes.Trim()) {
    Write-Host 'Hay cambios sin commitear (no se subirán):' -ForegroundColor Yellow
    Write-Host $pendientes -ForegroundColor DarkGray
    $resp = Read-Host '¿Continuar igual? (s/N)'
    if ($resp -notmatch '^[sS]$') { Write-Host 'Cancelado.'; return }
}

$commit = (& git rev-parse --short "refs/heads/$Rama")
Write-Host "Se publicará la rama local '$Rama' ($commit) como '$Destino' en GitLab." -ForegroundColor Cyan

$secure = Read-Host -AsSecureString 'Pega tu GitLab Personal Access Token (scope: write_repository)'
$bstr = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)

try {
    $token = [System.Runtime.InteropServices.Marshal]::PtrToStringBSTR($bstr)
    if ([string]::IsNullOrWhiteSpace($token)) { throw 'No se ingresó ningún token.' }

    $authUrl = "https://oauth2:$([uri]::EscapeDataString($token))@gitlab.com/profe.bryhan/asistente-cripto.git"

    Write-Host 'Empujando...' -ForegroundColor Cyan
    & git -c credential.helper= push $authUrl "refs/heads/${Rama}:refs/heads/$Destino"
    if ($LASTEXITCODE -ne 0) { throw "git push falló con código $LASTEXITCODE." }

    Write-Host ''
    Write-Host "OK: rama '$Destino' publicada." -ForegroundColor Green
    Write-Host "Mírala en: https://gitlab.com/profe.bryhan/asistente-cripto/-/tree/$Destino"
}
finally {
    [System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr)
    if (Get-Variable token -ErrorAction SilentlyContinue) { Remove-Variable token -Force }
    $secure = $null
    [System.GC]::Collect()
}
