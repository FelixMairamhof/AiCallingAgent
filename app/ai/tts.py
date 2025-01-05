import pyttsx3

def text_to_speech(text):
    """
    Convert text to speech and return the generated audio as bytes.
    """
    print("Performing Text-to-Speech...")
    engine = pyttsx3.init()
    engine.save_to_file(text, "response.mp3")
    engine.runAndWait()
    with open("response.mp3", "rb") as f:
        audio_bytes = f.read()
    return audio_bytes
