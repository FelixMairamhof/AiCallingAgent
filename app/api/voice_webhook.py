import os
import json
import base64
import asyncio
import websockets
from fastapi import FastAPI, WebSocket, APIRouter
from dotenv import load_dotenv

load_dotenv()

# Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
PORT = int(os.getenv('PORT', 5050))
MODEL = "gpt-4o-realtime-preview-2024-12-17"  # The model you want to use

# WebSocket connection URL
OPENAI_WS_URL = f"wss://api.openai.com/v1/realtime?model={MODEL}"

# Initialize FastAPI
app = FastAPI()

# WebSocket router for voice
voice_router = APIRouter()

@voice_router.websocket("/stream")
async def handle_media_stream(websocket: WebSocket):
    """Handle WebSocket connection with OpenAI Realtime API."""
    await websocket.accept()
    print("Client connected.")

    # Connect to OpenAI Realtime API WebSocket
    async with websockets.connect(
            OPENAI_WS_URL,
            additional_headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "OpenAI-Beta": "realtime=v1"
            }
    ) as openai_ws:
        print("Connected to OpenAI Realtime API.")

        # Initialize session with OpenAI
        await initialize_session(openai_ws)

        # Function to receive data from Twilio and send it to OpenAI
        async def receive_from_twilio():
            """Receive audio data from Twilio and send it to OpenAI."""
            try:
                async for message in websocket.iter_text():
                    data = json.loads(message)
                    if data['event'] == 'media':
                        audio_payload = {
                            "type": "input_audio_buffer.append",
                            "audio": data['media']['payload']
                        }
                        await openai_ws.send(json.dumps(audio_payload))
                    elif data['event'] == 'start':
                        print(f"Stream started with SID: {data['start']['streamSid']}")
            except websockets.exceptions.ConnectionClosed:
                print("Twilio WebSocket connection closed.")

        # Function to receive events from OpenAI and send them to Twilio
        async def send_to_twilio():
            """Receive events from OpenAI and send them back to Twilio."""
            try:
                async for openai_message in openai_ws:
                    response = json.loads(openai_message)
                    if response['type'] in ['error', 'response.content.done', 'rate_limits.updated', 'response.done']:
                        print(f"Received event: {response['type']}", response)

                    # Handle the audio delta and send back to Twilio
                    if response.get('type') == 'response.audio.delta' and 'delta' in response:
                        audio_delta = {
                            "event": "media",
                            "media": {
                                "payload": base64.b64encode(base64.b64decode(response['delta'])).decode('utf-8')
                            }
                        }
                        await websocket.send(json.dumps(audio_delta))
            except websockets.exceptions.ConnectionClosed:
                print("OpenAI WebSocket connection closed.")

        # Start receiving and sending events
        await asyncio.gather(receive_from_twilio(), send_to_twilio())

# Function to initialize session with OpenAI Realtime API
async def initialize_session(openai_ws):
    """Initialize session with OpenAI."""
    session_update = {
        "type": "session.update",
        "session": {
            "turn_detection": {"type": "server_vad"},
            "input_audio_format": "g711_ulaw",
            "output_audio_format": "g711_ulaw",
            "voice": "en_us_male",  # Define the voice you'd like to use
            "instructions": "Please assist the user.",
            "modalities": ["text", "audio"],
            "temperature": 0.8
        }
    }
    print('Sending session update:', json.dumps(session_update))
    await openai_ws.send(json.dumps(session_update))



