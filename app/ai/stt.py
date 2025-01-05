import openai

def transcribe_audio(audio_data):
    # Use Whisper API or another STT library
    print("Transcribe Audio")
    response = openai.Audio.transcribe("whisper-1", audio_data)
    return response.get("text", "")
