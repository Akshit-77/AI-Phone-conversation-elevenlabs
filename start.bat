@echo off
echo 🎯 RealTime Voice Agent - Quick Start
echo ====================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    python3 --version >nul 2>&1
    if errorlevel 1 (
        echo ❌ Python is not installed or not in PATH
        echo Please install Python 3.12+ from https://python.org
        pause
        exit /b 1
    )
    set PYTHON_CMD=python3
) else (
    set PYTHON_CMD=python
)

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip is not installed
    echo Please install pip or reinstall Python with pip included
    pause
    exit /b 1
)

REM Install requirements if they haven't been installed
if not exist ".requirements_installed" (
    echo 📦 Installing Python requirements...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Failed to install requirements
        pause
        exit /b 1
    )
    echo. > .requirements_installed
)

REM Check if .env exists
if not exist ".env" (
    echo ❌ .env file not found!
    echo Please copy .env.example to .env and add your API keys:
    echo   copy .env.example .env
    echo   # Then edit .env with your actual API keys
    pause
    exit /b 1
)

echo 🚀 Starting RealTime Voice Agent...
echo This will start all services: ngrok tunnel, FastAPI backend, and Streamlit frontend
echo.

REM Run the Python startup script
%PYTHON_CMD% run_app.py
pause