import speech_recognition as sr

# Initialize recognizer
recognizer = sr.Recognizer()

# Use microphone as audio source
with sr.Microphone() as source:
    print("Say something!")
    audio = recognizer.listen(source)

try:
    # Send audio to Google and get text back
    text = recognizer.recognize_google(audio)
    print(f"You said: {text}")
    
    # Add your commands here
    if "turn on light" in text.lower():
        print("Turning on light...")
        # Your code to control light
        
except sr.UnknownValueError:
    print("Couldn't understand audio")
except sr.RequestError:
    print("Could not connect to Google API")
