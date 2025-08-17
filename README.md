# RealTime Voice Agent

A voice calling agent that resolves user queries over phone calls using AI-powered speech recognition, natural language processing, and text-to-speech synthesis.

## Features

- 📞 Automated phone call initiation via web interface
- 🎤 Real-time speech-to-text conversion using ElevenLabs API
- 🤖 Intelligent response generation using OpenAI GPT
- 🔊 Natural text-to-speech synthesis using ElevenLabs voices
- 📱 WebSocket-based real-time communication with Twilio
- 🌐 User-friendly Streamlit web interface

## Technical Stack

- **Backend**: FastAPI with WebSocket support
- **Frontend**: Streamlit web interface
- **Speech Processing**: ElevenLabs API (TTS/STT)
- **AI**: OpenAI GPT-3.5-turbo
- **Telephony**: Twilio API and WebSockets
- **Language**: Python 3.12

## Prerequisites

1. **Python 3.12** installed on your system
2. **API Keys** for the following services:
   - OpenAI API key
   - ElevenLabs API key
   - Twilio Account SID, Auth Token, and Phone Number

Note: ngrok is now included as a Python dependency (pyngrok) and will be automatically installed.

## Installation

1. **Clone or download the project**
   ```bash
   cd /path/to/elevenlabs
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit the `.env` file with your actual API keys:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
   ELEVENLABS_VOICE_ID=pNInz6obpgDQGcFmaJgB
   TWILIO_ACCOUNT_SID=your_twilio_account_sid_here
   TWILIO_AUTH_TOKEN=your_twilio_auth_token_here
   TWILIO_PHONE_NUMBER=your_twilio_phone_number_here
   WEBHOOK_URL=http://localhost:8000
   ```

## Usage

### Quick Start (Recommended)

The easiest way to run the entire application with ngrok tunneling:

**Linux/macOS:**
```bash
./start.sh
```

**Windows (PowerShell):**
```powershell
.\start.ps1
```

**Windows (Command Prompt):**
```cmd
start.bat
```

**Cross-platform (Python):**
```bash
python run_app.py
```

This single command will:
- Install dependencies (if needed)
- Start ngrok tunnel for localhost:8000
- Update .env with the webhook URL automatically
- Start FastAPI backend server
- Start Streamlit web interface
- Display all service URLs

### Manual Setup

If you prefer to run services individually:

#### 1. Set up ngrok tunnel (for Twilio webhooks)

```bash
python3 setup_ngrok.py
```

This will start ngrok and automatically update your .env file with the webhook URL.

#### 2. Start the FastAPI Backend

```bash
python -m app.main
```

#### 3. Start the Streamlit Interface

In a new terminal:

```bash
streamlit run app/streamlit_app.py
```

### Making Calls

1. Open the Streamlit interface at `http://localhost:8501`
2. Enter your phone number (include country code, e.g., +1234567890)
3. Click "📞 Call Me"
4. Answer the incoming call and start speaking your query
5. The AI will respond with a voice answer

## Project Structure

```
elevenlabs/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI backend with WebSocket support
│   └── streamlit_app.py     # Streamlit web interface
├── services/
│   ├── __init__.py
│   ├── openai_service.py    # OpenAI integration
│   ├── elevenlabs_service.py # ElevenLabs TTS/STT
│   └── twilio_service.py    # Twilio call management
├── utils/
│   ├── __init__.py
│   └── env_loader.py        # Environment variable loader
├── static/                  # Static files (if needed)
├── .env.example            # Environment variables template
├── requirements.txt        # Python dependencies
├── setup_ngrok.py          # Ngrok setup script
├── run_app.py             # Complete application launcher
├── start.sh               # Quick start bash script
├── CLAUDE.md              # Project specifications
└── README.md              # This file
```

## API Endpoints

- `GET /` - Health check
- `POST /initiate-call` - Initiate a phone call
- `POST /twiml` - Twilio webhook endpoint
- `WebSocket /ws/{call_sid}` - Real-time audio streaming

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for GPT responses | Yes |
| `ELEVENLABS_API_KEY` | ElevenLabs API key for TTS/STT | Yes |
| `ELEVENLABS_VOICE_ID` | Voice ID for TTS (default provided) | No |
| `TWILIO_ACCOUNT_SID` | Twilio Account SID | Yes |
| `TWILIO_AUTH_TOKEN` | Twilio Auth Token | Yes |
| `TWILIO_PHONE_NUMBER` | Twilio phone number | Yes |
| `WEBHOOK_URL` | Base URL for webhooks | No |

### Voice Configuration

The default voice ID (`pNInz6obpgDQGcFmaJgB`) uses ElevenLabs' default voice. You can change this in your `.env` file to use different voices available in your ElevenLabs account.

## Deployment

### Local Development
- Use ngrok to expose your local server: `ngrok http 8000`
- Update `WEBHOOK_URL` in `.env` with your ngrok URL

### Production Deployment
1. Deploy to a cloud platform (AWS, GCP, Azure, etc.)
2. Update `WEBHOOK_URL` with your production domain
3. Ensure proper SSL/TLS configuration for WebSocket connections
4. Set up proper logging and monitoring

## Troubleshooting

### Common Issues

1. **"Could not connect to API server"**
   - Ensure FastAPI server is running on port 8000
   - Check if port 8000 is available

2. **"Invalid phone number"**
   - Include country code (e.g., +1 for US numbers)
   - Use format: +[country_code][number]

3. **Call not connecting**
   - Verify Twilio credentials in `.env`
   - Check Twilio account balance
   - Ensure webhook URL is accessible

4. **No voice response**
   - Verify ElevenLabs API key
   - Check OpenAI API key and quota
   - Review server logs for errors

### Logs and Debugging

- FastAPI server logs appear in the terminal where you ran `python -m app.main`
- Streamlit logs appear in the terminal where you ran `streamlit run app/streamlit_app.py`
- Check Twilio console for call logs and webhook delivery status

## License

This project is designed for prototyping purposes. Please ensure compliance with all API terms of service when deploying to production.

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review API documentation for OpenAI, ElevenLabs, and Twilio
3. Ensure all environment variables are properly configured