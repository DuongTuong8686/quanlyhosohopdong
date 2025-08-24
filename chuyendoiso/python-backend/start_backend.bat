@echo off
setlocal ENABLEDELAYEDEXPANSION

echo [CDS] Starting Python backend...

cd /d %~dp0

if "%1"=="--no-install" goto SKIP_INSTALL
echo [CDS] Installing dependencies from requirements.txt
py -m pip install -r requirements.txt
:SKIP_INSTALL

set PYTHONPATH=%cd%
echo [CDS] PYTHONPATH set to %PYTHONPATH%

echo [CDS] Launching Uvicorn on http://0.0.0.0:8000
py -m uvicorn api_server:app --host 0.0.0.0 --port 8000 --reload

endlocal

