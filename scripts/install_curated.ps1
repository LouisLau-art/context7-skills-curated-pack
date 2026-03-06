param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$RemainingArgs
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$installScript = Join-Path $scriptDir "install_curated.py"

$pythonCandidates = @()
if ($env:PYTHON_BIN) {
    $pythonCandidates += $env:PYTHON_BIN
}
if ($env:PYTHON_EXE) {
    $pythonCandidates += $env:PYTHON_EXE
}
$pythonCandidates += @("python", "py")
$pythonCandidates = $pythonCandidates | Select-Object -Unique

foreach ($candidate in $pythonCandidates) {
    $command = Get-Command $candidate -ErrorAction SilentlyContinue
    if (-not $command) {
        continue
    }

    & $candidate $installScript @RemainingArgs
    exit $LASTEXITCODE
}

Write-Error "Python is required. Set PYTHON_BIN or PYTHON_EXE, or install Python."
exit 1
