#!/usr/bin/env python3
import time
import os
import sys
from pathlib import Path
from pyngrok import ngrok
from utils.env_loader import load_env

load_env(override=True)

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

def start_ngrok_tunnel(port=8000):
    """Start ngrok tunnel for the specified port"""
    print(f"Starting ngrok tunnel for port {port}...")
    
    try:
        # Check if static domain is configured
        static_domain = os.getenv("NGROK_STATIC_DOMAIN")
        
        if static_domain:
            # Use static domain
            tunnel = ngrok.connect(port, domain=static_domain)
            public_url = f"https://{static_domain}"
            print(f"✅ Ngrok tunnel established with static domain: {public_url}")
        else:
            # Use random domain
            tunnel = ngrok.connect(port)
            public_url = tunnel.public_url
            print(f"✅ Ngrok tunnel established: {public_url}")
        
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
    
    print(f"✅ Updated .env file with webhook URL: {webhook_url}")
    return True

def main():
    print("🚀 Setting up ngrok tunnel for RealTime Voice Agent")
    print("-" * 50)
    
    # Configure ngrok auth
    if not configure_ngrok_auth():
        return False
    
    # Start ngrok tunnel
    public_url = start_ngrok_tunnel(8000)
    
    if not public_url:
        print("❌ Failed to establish ngrok tunnel")
        return False
    
    # Update .env file
    if update_env_file(public_url):
        print("\n🎉 Setup complete!")
        print(f"📞 Your webhook URL: {public_url}")
        print(f"🌐 FastAPI docs: {public_url}/docs")
        print(f"📊 Ngrok dashboard: http://localhost:4040")
        print("\nNow you can:")
        print("1. Run: python run_app.py")
        print("2. Or manually start your FastAPI server: python -m app.main")
        print("3. In another terminal, start Streamlit: streamlit run app/streamlit_app.py")
        print("\n⚠️  Keep this terminal open to maintain the ngrok tunnel!")
        
        # Keep ngrok running
        try:
            print("\nPress Ctrl+C to stop the tunnel...")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping ngrok tunnel...")
            ngrok.kill()
            print("✅ Tunnel stopped")
        
        return True
    
    return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)