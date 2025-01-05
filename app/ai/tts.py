import pyttsx3

def text_to_speech(text):
    print("Text to Speech")
    engine = pyttsx3.init()
    engine.save_to_file(text, "response.mp3")
    engine.runAndWait()
    with open("response.mp3", "rb") as f:
        return f.read()
