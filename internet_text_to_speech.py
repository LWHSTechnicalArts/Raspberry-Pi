from gtts import gTTS
from gtts import lang
import os

def speak(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    tts.save("output.mp3")
    os.system("mpg123 -q output.mp3")

# English
speak("Hello, how are you?", lang='en')

# French
speak("Bonjour, comment allez-vous?", lang='fr')

# Spanish
speak("Hola, cÃ³mo estÃ¡s?", lang='es')

# Chinese (Simplified)
speak("你好你最近怎么样", lang='zh-CN')

# Get all supported languages
languages = lang.tts_langs()

# Print them nicely
for code, name in sorted(languages.items()):
    print(f"{code}: {name}")



