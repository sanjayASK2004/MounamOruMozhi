import speech_recognition as sr

recognizer = sr.Recognizer()
mic = sr.Microphone()

print("Adjusting for ambient noise... Speak now.")

with mic as source:
    recognizer.adjust_for_ambient_noise(source, duration=1)
    print("Listening...")
    try:
        audio = recognizer.listen(source, timeout=5)
        print("Recognizing...")
        recognized_text = recognizer.recognize_google(audio, language="ta-IN")
        print(f"Recognized Text: {recognized_text}")
    except sr.UnknownValueError:
        print("Speech not recognized.")
    except sr.RequestError as e:
        print(f"Network error: {e}")
    except sr.WaitTimeoutError:
        print("No speech detected. Try again.")
