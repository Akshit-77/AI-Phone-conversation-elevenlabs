#!/usr/bin/env powershell

Write-Host "🎯 RealTime Voice Agent - Quick Start" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan

# Check if Python is available
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    if (-not (Get-Command python3 -ErrorAction SilentlyContinue)) {
        Write-Host "❌ Python is not installed or not in PATH" -ForegroundColor Red
        Write-Host "Please install Python 3.12+ from https://python.org" -ForegroundColor Yellow
        exit 1
    }
    $pythonCmd = "python3"
} else {
    $pythonCmd = "python"
}

# Check if pip is available
if (-not (Get-Command pip -ErrorAction SilentlyContinue)) {
    Write-Host "❌ pip is not installed" -ForegroundColor Red
    Write-Host "Please install pip or reinstall Python with pip included" -ForegroundColor Yellow
    exit 1
}

# Install requirements if they haven't been installed
if (-not (Test-Path ".requirements_installed")) {
    Write-Host "📦 Installing Python requirements..." -ForegroundColor Yellow
    pip install -r requirements.txt
    if ($LASTEXITCODE -eq 0) {
        New-Item -Path ".requirements_installed" -ItemType File -Force | Out-Null
    } else {
        Write-Host "❌ Failed to install requirements" -ForegroundColor Red
        exit 1
    }
}

# Check if .env exists
if (-not (Test-Path ".env")) {
    Write-Host "❌ .env file not found!" -ForegroundColor Red
    Write-Host "Please copy .env.example to .env and add your API keys:" -ForegroundColor Yellow
    Write-Host "  Copy-Item .env.example .env" -ForegroundColor White
    Write-Host "  # Then edit .env with your actual API keys" -ForegroundColor Gray
    exit 1
}

Write-Host "🚀 Starting RealTime Voice Agent..." -ForegroundColor Green
Write-Host "This will start all services: ngrok tunnel, FastAPI backend, and Streamlit frontend" -ForegroundColor White
Write-Host ""

# Run the Python startup script
& $pythonCmd run_app.py