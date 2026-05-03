@echo off
setlocal

cd /d "%~dp0"

echo [1/5] Create venv if not exists...
if not exist ".venv" (
    python -m venv .venv
)

echo [2/5] Activate venv...
call .venv\Scripts\activate

echo [3/5] Detect python...
where python >nul 2>nul
if errorlevel 1 (
    echo Python not found. Please install Python and add to PATH.
    pause
    exit /b 1
)

echo [4/5] Upgrade pip...
python -m pip install --upgrade pip

echo [5/6] Install dependencies...
if exist requirements.txt (
    pip install -r requirements.txt
) else (
    echo No requirements.txt found. Installing minimal deps...
    pip install sqlite-utils
)

echo [6/6] Run pipeline with AI...

if not exist samples\events.csv (
    echo Missing samples\events.csv
    echo Please add dataset before running.
    pause
    exit /b 1
)

python pipeline.py samples\events.csv --use-ai

echo Launching Product UI...
cd web
python app.py

echo.
echo Pipeline finished.
echo Launching workbench UI...
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0..\_shared_project_workbench\bootstrap_project_workbench.ps1" -ProjectDir "%~dp0"

if errorlevel 1 (
  echo.
  echo Workbench launch failed.
  pause
)

endlocal

