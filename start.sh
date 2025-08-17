#!/bin/bash

echo "🎯 RealTime Voice Agent - Quick Start"
echo "===================================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

# Check if pip is available
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo "❌ pip is not installed"
    exit 1
fi

# Install requirements if they haven't been installed
if [ ! -d "venv" ] && [ ! -f ".requirements_installed" ]; then
    echo "📦 Installing Python requirements..."
    pip install -r requirements.txt
    touch .requirements_installed
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    echo "Please copy .env.example to .env and add your API keys:"
    echo "  cp .env.example .env"
    echo "  # Then edit .env with your actual API keys"
    exit 1
fi

echo "🚀 Starting RealTime Voice Agent..."
echo "This will start all services: ngrok tunnel, FastAPI backend, and Streamlit frontend"
echo ""

# Run the Python startup script
python3 run_app.py