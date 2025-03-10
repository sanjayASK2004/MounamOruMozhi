import os
import speech_recognition as sr

def transcribe_tamil_speech():
    """Convert Tamil speech to Tamil text using Google Speech-to-Text API."""
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("🎤 Speak something in Tamil...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        print("📝 Recognizing...")
        tamil_text = recognizer.recognize_google(audio, language="ta-IN")
        print("✅ Tamil Text:", tamil_text)
        return tamil_text
    except sr.UnknownValueError:
        print("❌ Could not understand the audio.")
    except sr.RequestError:
        print("❌ Could not request results from Google Speech Recognition service.")
    
    return None

if __name__ == "__main__":
    transcribe_tamil_speech()
