import os

# Check if running on Render (cloud)
if os.getenv("RENDER") == "true":
    def speak(text):
        print(f"[Render Mode]: Skipping TTS — Render has no audio")
else:
    import pyttsx3

    def speak(text):
        print(f"[SPEAK]: {text}")
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
