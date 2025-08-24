Param(
    [switch]$NoInstall
)

Write-Host "[CDS] Starting Python backend..."

# Move to script directory
Set-Location -Path $PSScriptRoot

if (-not $NoInstall) {
    Write-Host "[CDS] Installing dependencies from requirements.txt"
    py -m pip install -r requirements.txt
}

$env:PYTHONPATH = (Get-Location).Path
Write-Host "[CDS] PYTHONPATH set to $($env:PYTHONPATH)"

Write-Host "[CDS] Launching Uvicorn on http://0.0.0.0:8000"
py -m uvicorn api_server:app --host 0.0.0.0 --port 8000 --reload


