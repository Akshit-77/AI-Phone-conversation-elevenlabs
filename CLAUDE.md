# RealTime Voice Agent

## Project Overview

**Objective**: Build a voice calling agent for resolving user queries over phone calls.

## Technical Stack

- Python 3.12
- FastAPI
- OpenAI
- ElevenLabs API for TTS and STT
- Twilio WebSocket logic for streaming response over the call
- Twilio API for making phone calls

## User Flow

1. User enters phone number in the interface to receive a call
2. User speaks query at the phone interface
3. Query is processed by STT model and converted to text
4. Text is provided to OpenAI model for response generation
5. Response is sent to TTS model (ElevenLabs API) 
6. Voice response is streamed over the phone call
7. Complete context is maintained throughout the phone call
8. OpenAI model system prompt configured to provide concise answers
9. Voice call experience supports user interruptions and call termination via distinct voice phrases

## Development Requirements

- Project designed for prototyping - implement workflow with accuracy without complex logic
- All necessary files must include `load_env(override=True)` to load environment variables from `.env` file
- Ensure correct library/module imports with conflict-free installations
- Implement minimal error handling only at necessary places
- Create Streamlit interface for phone number input and call initiation
- Use Twilio WebSockets for reduced response latency during calls
- make a clear project and directory structure
- Generate README.md file for GitHub deployment and usage instructions