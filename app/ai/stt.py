import base64
from io import BytesIO
import openai

def transcribe_audio(audio_payload):
    """
    Transcribe audio payload (Base64-encoded) using OpenAI Whisper API.
    """
    print("Performing Speech-to-Text with the latest OpenAI API...")

    try:
        # Decode Base64 payload into bytes
        audio_bytes = base64.b64decode(audio_payload)

        # Create a file-like object from the audio bytes
        audio_file = BytesIO(audio_bytes)
        audio_file.name = "audio.wav"  # Whisper API requires a file name for MIME type detection

        # Transcribe the audio using Whisper API
        response = openai.Audio.create(
            model="whisper-1",
            file=audio_file
        )

        return response.get("text", "")
    except Exception as e:
        print(f"Error during transcription: {e}")
        return ""
