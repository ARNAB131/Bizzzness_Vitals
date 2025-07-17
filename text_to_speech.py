import os

if os.getenv("RENDER") == "true":
    print("[Render Mode]: Skipping pyttsx3 import")

    def speak(text):
        print(f"[Render Mode]: {text}")
else:
    print("[Local Mode]: Using pyttsx3")
    import pyttsx3

    def speak(text):
        print(f"[SPEAK]: {text}")
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
