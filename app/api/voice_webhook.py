from fastapi import APIRouter, WebSocket
from app1.ai.gpt_handler import process_conversation
from app1.ai.tts import text_to_speech
from app1.ai.stt import transcribe_audio
import logging
voice_router = APIRouter()
@voice_router.websocket("/stream")
async def voice_stream(websocket: WebSocket):
    """
    WebSocket endpoint to stream audio and handle AI conversations.
    """
    await websocket.accept()
    logging.info("WebSocket connection established")
    try:
        while True:
            # Receive audio chunks from Twilio
            try:
                audio_data = await websocket.receive_bytes()
                logging.info("Audio chunk received")

                # Process audio and generate a response
                text = transcribe_audio(audio_data)
                logging.info(f"Transcribed text: {text}")
                response = process_conversation(text)
                audio_response = text_to_speech(response)

                # Send the response back as audio
                await websocket.send_bytes(audio_response)
            except Exception as e:
                logging.error(f"Error processing audio: {e}")
                break
    except Exception as e:
        logging.error(f"WebSocket communication error: {e}")
    finally:
        await websocket.close()
        logging.info("WebSocket connection closed")

