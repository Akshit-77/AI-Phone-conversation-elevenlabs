import os
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
from typing import Optional
from utils.env_loader import load_env

load_env(override=True)

class TwilioService:
    def __init__(self):
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.phone_number = os.getenv("TWILIO_PHONE_NUMBER")
        self.webhook_url = os.getenv("WEBHOOK_URL", "http://localhost:8000")
        
        if not all([self.account_sid, self.auth_token, self.phone_number]):
            raise ValueError("Twilio credentials (TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER) are required")
        
        self.client = Client(self.account_sid, self.auth_token)
    
    async def make_call(self, to_number: str) -> str:
        """Initiate a call to the specified number"""
        try:
            call = self.client.calls.create(
                to=to_number,
                from_=self.phone_number,
                url=f"{self.webhook_url}/twiml",
                method="POST"
            )
            return call.sid
        except Exception as e:
            raise Exception(f"Failed to initiate call: {str(e)}")
    
    def generate_twiml_response(self, call_sid: str) -> str:
        """Generate TwiML response to start media streaming"""
        response = VoiceResponse()
        
        # Start the conversation
        response.say("Hello! I'm your AI voice assistant. How can I help you today?")
        
        # Get WebSocket URL from environment or construct it
        websocket_url = os.getenv("WEBSOCKET_URL")
        
        if not websocket_url:
            # Construct WebSocket URL from webhook URL
            webhook_domain = self.webhook_url.replace('http://', '').replace('https://', '')
            # Always use wss:// for ngrok and production
            websocket_url = f"wss://{webhook_domain}/ws/{call_sid}"
        else:
            # Use provided WebSocket URL and append call_sid
            websocket_url = f"{websocket_url}/ws/{call_sid}"
        
        print(f"🌐 WebSocket URL for streaming: {websocket_url}")
        
        # Start media streaming
        start = response.start()
        start.stream(
            url=websocket_url,
            track="inbound_track"  # Only capture user's audio
        )
        
        # Keep the call active with a long pause
        response.pause(length=3600)  # 1 hour to keep call active
        
        return str(response)
    
    def end_call(self, call_sid: str):
        """End an active call"""
        try:
            call = self.client.calls(call_sid).update(status="completed")
            return call.status
        except Exception as e:
            print(f"Error ending call: {e}")
            return None