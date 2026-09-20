@echo off
setlocal


if not exist "venv" (
    echo [INFO] Creating Python virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b %errorlevel%
    )
)

echo [INFO] Updating pip and installing dependencies...
.\venv\Scripts\python.exe -m pip install --upgrade pip
if exist "requirements.txt" (
    .\venv\Scripts\pip.exe install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install requirements.
        pause
        exit /b %errorlevel%
    )
) else (
    echo [WARNING] requirements.txt not found, skipping installation.
)

echo.
echo ==========================================
echo Setup completed! Launching application...
echo ==========================================
echo.

.\venv\Scripts\python.exe main.py

pause