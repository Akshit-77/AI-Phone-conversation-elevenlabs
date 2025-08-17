import requests
import os
import io
from typing import Optional
from utils.env_loader import load_env

load_env(override=True)

class ElevenLabsService:
    def __init__(self):
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        self.base_url = "https://api.elevenlabs.io/v1"
        self.voice_id = os.getenv("ELEVENLABS_VOICE_ID", "pNInz6obpgDQGcFmaJgB")  # Default voice ID
        
        if not self.api_key:
            raise ValueError("ELEVENLABS_API_KEY environment variable is required")
    
    async def text_to_speech(self, text: str) -> bytes:
        """Convert text to speech using ElevenLabs API"""
        url = f"{self.base_url}/text-to-speech/{self.voice_id}"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }
        
        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }
        
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            return response.content
            
        except requests.exceptions.RequestException as e:
            print(f"ElevenLabs TTS error: {e}")
            # Return empty bytes on error
            return b""
    
    async def speech_to_text(self, audio_data: bytes) -> Optional[str]:
        """Convert speech to text using ElevenLabs API"""
        url = f"{self.base_url}/speech-to-text"
        
        print(f"🎙️ Sending {len(audio_data)} bytes to ElevenLabs STT API")
        
        headers = {
            "xi-api-key": self.api_key
        }
        
        files = {
            "audio": ("audio.wav", io.BytesIO(audio_data), "audio/wav")
        }
        
        data = {
            "model_id": "scribe_v1"
        }
        
        try:
            print(f"🌐 Making STT request to: {url}")
            response = requests.post(url, headers=headers, files=files, data=data)
            print(f"📊 STT Response status: {response.status_code}")
            
            response.raise_for_status()
            
            result = response.json()
            transcribed_text = result.get("text", "").strip()
            print(f"✅ STT Success - Transcribed: '{transcribed_text}'")
            return transcribed_text
            
        except requests.exceptions.RequestException as e:
            print(f"❌ ElevenLabs STT error: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"📄 Error response: {e.response.text}")
            return None
        except Exception as e:
            print(f"❌ STT processing error: {e}")
            return None