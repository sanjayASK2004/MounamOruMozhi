import cv2
import mediapipe as mp
import speech_recognition as sr
import json
import time

# Initialize MediaPipe Holistic
mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

# Load sign language mapping from JSON
sign_mapping = {
    "hello": "wave_hand",
    "thank you": "hand_to_chest"
}

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        text = recognizer.recognize_google(audio)
        print("Recognized:", text)
        return text.lower()
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError:
        print("Speech recognition service unavailable")
    return ""

def get_gesture(word):
    return sign_mapping.get(word, None)

def animate_avatar(gesture):
    cap = cv2.VideoCapture(0)
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = holistic.process(image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # Draw landmarks
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
            mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
            mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
            
            cv2.putText(image, f"Gesture: {gesture}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow("Sign Language Avatar", image)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    word = recognize_speech()
    gesture = get_gesture(word)
    if gesture:
        print(f"Playing gesture: {gesture}")
        animate_avatar(gesture)
    else:
        print("No matching sign found")

