import os

def speak(text):
    os.system(f'espeak "{text}"')

speak("Hello, I'm a robot but I've loved you since the beginning of time.")
