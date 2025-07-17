import pyttsx3

def speak(text):
    print(f"[SPEAK]: {text}")
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
