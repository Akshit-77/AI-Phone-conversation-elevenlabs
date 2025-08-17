#!/usr/bin/env python3
import subprocess
import time
import requests
import json
import os
import sys
import signal
import threading
from pathlib import Path
from pyngrok import ngrok
from utils.env_loader import load_env

def configure_ngrok_auth():
    """Configure ngrok with authtoken from environment"""
    authtoken = os.getenv("NGROK_AUTHTOKEN")
    if authtoken:
        try:
            ngrok.set_auth_token(authtoken)
            print("✅ Ngrok authtoken configured")
            return True
        except Exception as e:
            print(f"❌ Error setting ngrok authtoken: {e}")
            return False
    else:
        print("⚠️  NGROK_AUTHTOKEN not found in .env file")
        print("Please add your ngrok authtoken to .env file:")
        print("NGROK_AUTHTOKEN=your_ngrok_authtoken_here")
        return False

# Global process references
fastapi_process = None
streamlit_process = None
ngrok_tunnel = None

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print("\n🛑 Shutting down all services...")
    
    global fastapi_process, streamlit_process, ngrok_tunnel
    
    if fastapi_process:
        print("Stopping FastAPI server...")
        fastapi_process.terminate()
        fastapi_process.wait()
    
    if streamlit_process:
        print("Stopping Streamlit server...")
        streamlit_process.terminate()
        streamlit_process.wait()
    
    if ngrok_tunnel:
        print("Stopping ngrok tunnel...")
        ngrok.kill()
    
    print("✅ All services stopped")
    sys.exit(0)

def start_ngrok_tunnel(port=8000):
    """Start ngrok tunnel for the specified port"""
    print(f"🌐 Starting ngrok tunnel for port {port}...")
    
    global ngrok_tunnel
    
    try:
        # Check if static domain is configured
        static_domain = os.getenv("NGROK_STATIC_DOMAIN")
        
        if static_domain:
            # Use static domain
            ngrok_tunnel = ngrok.connect(port, domain=static_domain)
            public_url = f"https://{static_domain}"
            print(f"✅ Ngrok tunnel with static domain: {public_url}")
        else:
            # Use random domain
            ngrok_tunnel = ngrok.connect(port)
            public_url = ngrok_tunnel.public_url
            print(f"✅ Ngrok tunnel: {public_url}")
        
        return public_url
        
    except Exception as e:
        print(f"❌ Error starting ngrok tunnel: {e}")
        return None

def update_env_file(webhook_url):
    """Update .env file with the ngrok webhook URL"""
    env_path = Path('.env')
    
    if not env_path.exists():
        print("❌ .env file not found. Please create one first.")
        return False
    
    # Read current .env content
    with open(env_path, 'r') as f:
        lines = f.readlines()
    
    # Update WEBHOOK_URL
    updated = False
    for i, line in enumerate(lines):
        if line.strip().startswith('WEBHOOK_URL='):
            lines[i] = f'WEBHOOK_URL={webhook_url}\n'
            updated = True
            break
    
    # If WEBHOOK_URL doesn't exist, add it
    if not updated:
        lines.append(f'WEBHOOK_URL={webhook_url}\n')
    
    # Write back to .env
    with open(env_path, 'w') as f:
        f.writelines(lines)
    
    print(f"✅ Updated webhook URL in .env")
    return True

def start_fastapi():
    """Start FastAPI server"""
    print("🚀 Starting FastAPI server...")
    
    global fastapi_process
    fastapi_process = subprocess.Popen([
        sys.executable, '-m', 'app.main'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Wait a bit for server to start
    time.sleep(3)
    
    # Check if server is running
    try:
        response = requests.get('http://localhost:8000', timeout=5)
        print("✅ FastAPI server running on http://localhost:8000")
        return True
    except Exception as e:
        print("❌ FastAPI server failed to start")
        
        # Get error details from the process
        if fastapi_process.poll() is not None:
            stdout, stderr = fastapi_process.communicate()
            if stderr:
                print(f"Error output: {stderr}")
            if stdout:
                print(f"Standard output: {stdout}")
        else:
            print(f"Connection error: {e}")
        
        return False

def start_streamlit():
    """Start Streamlit server"""
    print("🎨 Starting Streamlit interface...")
    
    global streamlit_process
    streamlit_process = subprocess.Popen([
        'streamlit', 'run', 'app/streamlit_app.py', '--server.port=8501'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Wait a bit for server to start
    time.sleep(3)
    
    print("✅ Streamlit interface running on http://localhost:8501")
    return True

def wait_for_processes():
    """Wait for all processes and handle termination"""
    try:
        while True:
            time.sleep(1)
            
            # Check if any process has died
            global fastapi_process, streamlit_process
            
            if fastapi_process and fastapi_process.poll() is not None:
                print("❌ FastAPI process died")
                break
                
            if streamlit_process and streamlit_process.poll() is not None:
                print("❌ Streamlit process died")
                break
                
    except KeyboardInterrupt:
        pass

def main():
    print("🎯 RealTime Voice Agent - Complete Setup")
    print("=" * 50)
    
    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    # Load environment variables
    load_env(override=True)
    
    # Check if .env file exists
    if not Path('.env').exists():
        print("❌ .env file not found!")
        print("Please copy .env.example to .env and add your API keys:")
        print("  cp .env.example .env")
        return False
    
    # Configure ngrok auth
    if not configure_ngrok_auth():
        return False
    
    print("✅ Prerequisites check passed")
    print()
    
    # Start ngrok tunnel
    public_url = start_ngrok_tunnel(8000)
    if not public_url:
        print("❌ Failed to establish ngrok tunnel")
        return False
    
    # Update .env file with webhook URL
    if not update_env_file(public_url):
        return False
    
    print()
    
    # Start FastAPI server
    if not start_fastapi():
        return False
    
    # Start Streamlit interface
    if not start_streamlit():
        return False
    
    print()
    print("🎉 All services are running!")
    print("-" * 30)
    print(f"📞 Webhook URL: {public_url}")
    print(f"🔧 FastAPI Server: http://localhost:8000")
    print(f"🔧 API Docs: http://localhost:8000/docs")
    print(f"🎨 Streamlit App: http://localhost:8501")
    print(f"📊 Ngrok Dashboard: http://localhost:4040")
    print()
    print("📱 Open http://localhost:8501 to start making calls!")
    print()
    print("⚠️  Keep this terminal open to maintain all services")
    print("Press Ctrl+C to stop all services...")
    print()
    
    # Wait for processes
    wait_for_processes()
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)