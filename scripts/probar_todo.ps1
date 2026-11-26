#Requires -Version 5.1
<#
.SYNOPSIS
    Ejecuta todas las pruebas locales del asistente cripto.

.DESCRIPTION
    Corre en orden los tres conjuntos de pruebas del proyecto y una tabla
    resumen al final:

      1. Pruebas unitarias      (tests/)      -> no necesitan servicios.
      2. Casos de evaluación    (evals/)      -> necesitan el agente levantado.
      3. Pruebas de evidencias  (evidencias/) -> necesitan agente + especialistas.
      4. Métricas del registro  (scripts/)    -> lee lo que dejaron las anteriores.

    Antes de ejecutar comprueba qué servicios están escuchando, para que un
    fallo por "servicio apagado" no se confunda con un fallo del código.

.PARAMETER SinN8n
    Omite los casos que dependen del workflow de n8n. Útil si no lo tienes
    corriendo: esos casos se marcan OMITIDOS en vez de FALLIDOS.

.PARAMETER SoloUnitarias
    Ejecuta únicamente las pruebas unitarias (rápido, sin red ni servicios).

.EXAMPLE
    .\scripts\probar_todo.ps1

.EXAMPLE
    .\scripts\probar_todo.ps1 -SinN8n

.EXAMPLE
    .\scripts\probar_todo.ps1 -SoloUnitarias
#>

param(
    [switch]$SinN8n,
    [switch]$SoloUnitarias
)

# Los stderr de Python (warnings) no deben abortar el script.
$ErrorActionPreference = 'Continue'

$raiz = Split-Path -Parent $PSScriptRoot
Set-Location $raiz

$python = Join-Path $raiz '.venv\Scripts\python.exe'
if (-not (Test-Path $python)) {
    Write-Host 'No existe .venv. Crea el entorno primero:' -ForegroundColor Red
    Write-Host '    py -3.12 -m venv .venv'
    Write-Host '    .\.venv\Scripts\Activate.ps1'
    Write-Host '    python -m pip install -r requirements.txt'
    exit 1
}

$env:PYTHONIOENCODING = 'utf-8'

function Test-Puerto {
    param([int]$Puerto, [string]$Nombre)
    $escucha = Get-NetTCPConnection -LocalPort $Puerto -State Listen -ErrorAction SilentlyContinue
    if ($escucha) {
        Write-Host ("  [OK ] {0,-28} puerto {1}" -f $Nombre, $Puerto) -ForegroundColor DarkGray
        return $true
    }
    Write-Host ("  [-- ] {0,-28} puerto {1} apagado" -f $Nombre, $Puerto) -ForegroundColor Yellow
    return $false
}

function Invoke-Suite {
    param([string]$Nombre, [string[]]$Argumentos)

    Write-Host ''
    Write-Host ("=== {0} ===" -f $Nombre) -ForegroundColor Cyan

    # Se ejecuta via cmd para que stderr quede fusionado con stdout sin que
    # PowerShell 5.1 lo convierta en NativeCommandError (y sin perder el codigo
    # de salida, que es lo que decide si la suite paso).
    $linea = '"' + $python + '" ' + ($Argumentos -join ' ') + ' 2>&1'
    & cmd /c $linea | Out-Host
    return $LASTEXITCODE
}

# --- Servicios -------------------------------------------------------------
Write-Host 'Servicios detectados:' -ForegroundColor Cyan
Write-Host ("  raiz: {0}" -f $raiz) -ForegroundColor DarkGray
$hayAgente = Test-Puerto 8000 'agente principal'
$hayEspecialista = Test-Puerto 2024 'especialista LangGraph'
$hayN8n = Test-Puerto 5678 'especialista n8n'

$resultados = [System.Collections.Generic.List[object]]::new()

# --- 1. Unitarias ----------------------------------------------------------
$codigo = Invoke-Suite 'Pruebas unitarias' @('-m', 'unittest', 'discover', '-s', 'tests')
$resultados.Add([pscustomobject]@{
        Suite = 'Unitarias'; Codigo = $codigo
        Estado = if ($codigo -eq 0) { 'OK' } else { 'FALLO' }
    })

if ($SoloUnitarias) {
    Write-Host ''
    Write-Host ('Resultado: {0}' -f $resultados[0].Estado) -ForegroundColor $(if ($codigo -eq 0) { 'Green' } else { 'Red' })
    exit $codigo
}

# --- 2. Evaluación ---------------------------------------------------------
$argsEval = @('-m', 'evals.ejecutar')
if ($SinN8n -or -not $hayN8n) { $argsEval += '--sin-dependencias' }
if (-not $hayAgente) {
    Write-Host ''
    Write-Host 'AVISO: el agente no esta en el puerto 8000; la evaluacion fallara.' -ForegroundColor Yellow
}
$codigo = Invoke-Suite 'Casos de evaluacion' $argsEval
$resultados.Add([pscustomobject]@{
        Suite = 'Evaluacion'; Codigo = $codigo
        Estado = if ($codigo -eq 0) { 'OK' } else { 'FALLO' }
    })

# --- 3. Evidencias ---------------------------------------------------------
$codigo = Invoke-Suite 'Pruebas de evidencias' @('evidencias/pruebas_base.py')
$resultados.Add([pscustomobject]@{
        Suite = 'Evidencias'; Codigo = $codigo
        Estado = if ($codigo -eq 0) { 'OK' } else { 'FALLO' }
    })

# --- 4. Métricas -----------------------------------------------------------
$codigo = Invoke-Suite 'Metricas del registro' @('scripts/metricas.py')
$resultados.Add([pscustomobject]@{
        Suite = 'Metricas'; Codigo = $codigo
        Estado = if ($codigo -eq 0) { 'OK' } else { 'FALLO' }
    })

# --- Resumen ---------------------------------------------------------------
Write-Host ''
Write-Host '=== Resumen ===' -ForegroundColor Cyan
$resultados | Format-Table -AutoSize | Out-Host

$fallos = @($resultados | Where-Object { $_.Estado -ne 'OK' }).Count
if ($fallos -gt 0) {
    Write-Host ("{0} suite(s) con fallos." -f $fallos) -ForegroundColor Red
    if (-not $hayEspecialista) { Write-Host 'Recuerda levantar el especialista: python -m uvicorn servidor_especialista:app --port 2024' }
    if (-not $hayN8n) { Write-Host 'O usa -SinN8n para omitir los casos de n8n.' }
    exit 1
}

Write-Host 'Todo en verde.' -ForegroundColor Green
exit 0
