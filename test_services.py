#!/usr/bin/env python3
"""Test script to check if all services can initialize properly"""
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from utils.env_loader import load_env

print("🔍 Testing service initialization...")
print("-" * 40)

# Load environment variables
try:
    load_env(override=True)
    print("✅ Environment variables loaded")
except Exception as e:
    print(f"❌ Error loading environment: {e}")
    sys.exit(1)

# Test each service
services_to_test = [
    ("TwilioService", "services.twilio_service", "TwilioService"),
    ("OpenAIService", "services.openai_service", "OpenAIService"),
    ("ElevenLabsService", "services.elevenlabs_service", "ElevenLabsService"),
]

for service_name, module_path, class_name in services_to_test:
    try:
        print(f"Testing {service_name}...")
        module = __import__(module_path, fromlist=[class_name])
        service_class = getattr(module, class_name)
        service_instance = service_class()
        print(f"✅ {service_name} initialized successfully")
    except Exception as e:
        print(f"❌ {service_name} failed: {e}")
        print(f"   Error type: {type(e).__name__}")

print("-" * 40)
print("🔍 Testing FastAPI imports...")

try:
    from fastapi import FastAPI, WebSocket, WebSocketDisconnect
    from fastapi.responses import HTMLResponse
    print("✅ FastAPI imports successful")
except Exception as e:
    print(f"❌ FastAPI import error: {e}")

print("\n✨ Service test complete!")