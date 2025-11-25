import os
import sys
import speech_recognition as sr
from gpiozero import LED
import time
led = LED(18)

# Suppress ALSA warnings
os.environ['ALSA_CARD'] = 'default'
stderr = os.dup(2)
os.close(2)
os.open(os.devnull, os.O_RDWR)

recognizer = sr.Recognizer()

# Adjust these for better detection
recognizer.energy_threshold = 300  # Lower = more sensitive
recognizer.dynamic_energy_threshold = False

print("Voice control ready!")

try:
    while True:
        with sr.Microphone() as source:
            print("\n--- Listening (speak now!) ---")
            
            # Give it a timeout so it doesn't hang forever
            try:
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=2)
                print("Processing...")
            except sr.WaitTimeoutError:
                print("No speech detected, trying again...")
                continue

        try:
            text = recognizer.recognize_google(audio)
            print(f"? You said: '{text}'")
            
            if "milkshake" in text.lower():
                led.on()
                print("Light turned ON")
                
            elif "hamburger" in text.lower():
                led.off()
                print("Light turned OFF")
                
        except sr.UnknownValueError:
            print("? Couldn't understand audio")
        except sr.RequestError as e:
            print(f"? Google API error: {e}")

except KeyboardInterrupt:
    print("\nCleaning up...")
    GPIO.cleanup()
