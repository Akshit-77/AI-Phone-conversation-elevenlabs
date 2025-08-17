from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Form
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
import json
import base64
import asyncio
import sys
import os
import audioop
import wave
import io
from typing import Dict, Any
from pathlib import Path

# Add parent directory to Python path so we can import services and utils
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from services.twilio_service import TwilioService
from services.openai_service import OpenAIService
from services.elevenlabs_service import ElevenLabsService
from utils.env_loader import load_env

load_env(override=True)

app = FastAPI()

# Initialize services
twilio_service = TwilioService()
openai_service = OpenAIService()
elevenlabs_service = ElevenLabsService()

# Store active connections and audio buffers
active_connections: Dict[str, WebSocket] = {}
audio_buffers: Dict[str, list] = {}
last_activity: Dict[str, float] = {}

@app.get("/")
async def get():
    return {"message": "RealTime Voice Agent API"}

@app.post("/twiml")
async def twiml_endpoint(CallSid: str = Form(...), From: str = Form(None), To: str = Form(None)):
    """Handle Twilio webhook and return TwiML response"""
    print(f"📞 Received Twilio webhook for call: {CallSid}")
    print(f"📞 From: {From}, To: {To}")
    
    twiml_response = twilio_service.generate_twiml_response(CallSid)
    print(f"📋 Generated TwiML response: {twiml_response}")
    
    return Response(
        content=twiml_response,
        media_type="application/xml"
    )


def convert_mulaw_to_wav(mulaw_data: bytes) -> bytes:
    """Convert mu-law audio to WAV format"""
    try:
        # Convert mu-law to linear PCM
        pcm_data = audioop.ulaw2lin(mulaw_data, 2)
        
        # Create WAV file in memory
        wav_buffer = io.BytesIO()
        with wave.open(wav_buffer, 'wb') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(8000)  # 8kHz sample rate
            wav_file.writeframes(pcm_data)
        
        wav_buffer.seek(0)
        return wav_buffer.read()
    except Exception as e:
        print(f"Error converting audio: {e}")
        return b""

@app.websocket("/ws/{call_sid}")
async def websocket_endpoint(websocket: WebSocket, call_sid: str):
    await websocket.accept()
    active_connections[call_sid] = websocket
    audio_buffers[call_sid] = []
    last_activity[call_sid] = asyncio.get_event_loop().time()
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("event") == "media":
                # Handle incoming audio data
                audio_payload = message["media"]["payload"]
                audio_data = base64.b64decode(audio_payload)
                
                # Store audio chunk in buffer
                audio_buffers[call_sid].append(audio_data)
                last_activity[call_sid] = asyncio.get_event_loop().time()
                
                # Process accumulated audio if we have enough data or after silence
                current_time = asyncio.get_event_loop().time()
                if (len(audio_buffers[call_sid]) >= 20 or 
                    current_time - last_activity[call_sid] > 1.0):
                    
                    # Combine all audio chunks
                    combined_audio = b"".join(audio_buffers[call_sid])
                    audio_buffers[call_sid] = []
                    
                    if len(combined_audio) > 0:
                        # Convert mu-law to WAV
                        wav_data = convert_mulaw_to_wav(combined_audio)
                        
                        if wav_data:
                            # Convert speech to text
                            text = await elevenlabs_service.speech_to_text(wav_data)
                            
                            if text and text.strip():
                                # Get response from OpenAI
                                response = await openai_service.get_response(text, call_sid)
                                
                                # Convert response to speech
                                audio_response = await elevenlabs_service.text_to_speech(response)
                                
                                if audio_response:
                                    # Send audio back through WebSocket
                                    audio_b64 = base64.b64encode(audio_response).decode("utf-8")
                                    media_message = {
                                        "event": "media",
                                        "streamSid": message.get("streamSid"),
                                        "media": {
                                            "payload": audio_b64
                                        }
                                    }
                                    await websocket.send_text(json.dumps(media_message))
            
            elif message.get("event") == "start":
                # Call started
                print(f"Call {call_sid} started")
                
            elif message.get("event") == "stop":
                # Call ended
                print(f"Call {call_sid} ended")
                break
                
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for call {call_sid}")
    except Exception as e:
        print(f"Error in WebSocket: {e}")
    finally:
        if call_sid in active_connections:
            del active_connections[call_sid]
        if call_sid in audio_buffers:
            del audio_buffers[call_sid]
        if call_sid in last_activity:
            del last_activity[call_sid]

@app.post("/initiate-call")
async def initiate_call(phone_data: dict):
    phone_number = phone_data.get("phone_number")
    if not phone_number:
        return {"error": "Phone number is required"}
    
    try:
        call_sid = await twilio_service.make_call(phone_number)
        return {"success": True, "call_sid": call_sid}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)