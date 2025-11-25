import speech_recognition as sr
from groq import Groq
from gtts import gTTS
import os

recognizer = sr.Recognizer()
client = Groq(api_key="YOUR_GROQ_API_KEY")

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source, timeout=5)
    
    try:
        return recognizer.recognize_google(audio)
    except:
        return None

def ask_groq(question, conversation_history=[]):
    """Maintain conversation context"""
    messages = conversation_history + [{"role": "user", "content": question}]
    
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.7,
        max_tokens=200
    )
    
    response = completion.choices[0].message.content
    return response

def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save("response.mp3")
    os.system("mpg123 -q response.mp3")

# Main loop with wake word
conversation_history = []
wake_word = "hey robobaby"

print(f"Say '{wake_word}' to activate")
speak("Voice assistant ready")

while True:
    command = listen()
    
    if command:
        command_lower = command.lower()
        
        # Check for wake word
        if wake_word in command_lower:
            speak("Yes, I'm listening")
            
            # Get the actual command
            command = listen()
            if not command:
                continue
        
        # Exit command
        if "goodbye" in command_lower:
            speak("Goodbye!")
            break
        
        # Clear history command
        if "clear history" in command_lower:
            conversation_history = []
            speak("Conversation history cleared")
            continue
        
        # Get AI response with context
        print("Thinking...")
        response = ask_groq(command, conversation_history)
        
        # Update conversation history
        conversation_history.append({"role": "user", "content": command})
        conversation_history.append({"role": "assistant", "content": response})
        
        print(f"AI: {response}")
        speak(response)
