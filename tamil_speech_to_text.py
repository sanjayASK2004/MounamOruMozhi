import sys
import speech_recognition as sr
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTextEdit, QVBoxLayout, QFileDialog
from docx import Document

class TamilSpeechToTextApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.recognizer = sr.Recognizer()
        self.is_listening = False
    
    def init_ui(self):
        self.setWindowTitle("Tamil Speech to Text")
        self.setGeometry(100, 100, 500, 400)
        
        self.text_box = QTextEdit(self)
        self.text_box.setPlaceholderText("Recognized Tamil text will appear here...")
        
        self.start_button = QPushButton("🎤 Start Listening", self)
        self.start_button.clicked.connect(self.start_listening)
        
        self.stop_button = QPushButton("🛑 Stop Listening", self)
        self.stop_button.clicked.connect(self.stop_listening)
        
        self.save_button = QPushButton("💾 Save as DOCX", self)
        self.save_button.clicked.connect(self.save_text)
        
        layout = QVBoxLayout()
        layout.addWidget(self.text_box)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.save_button)
        
        self.setLayout(layout)
    
    def start_listening(self):
        self.is_listening = True
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            self.text_box.append("Listening for Tamil speech...")
            while self.is_listening:
                try:
                    audio = self.recognizer.listen(source, timeout=5)
                    tamil_text = self.recognizer.recognize_google(audio, language="ta-IN")
                    self.text_box.append(tamil_text)
                except sr.UnknownValueError:
                    self.text_box.append("⚠️ Could not understand the audio.")
                except sr.RequestError:
                    self.text_box.append("⚠️ Speech recognition service unavailable.")
                except Exception as e:
                    self.text_box.append(f"⚠️ Error: {str(e)}")
    
    def stop_listening(self):
        self.is_listening = False
        self.text_box.append("🛑 Stopped listening.")
    
    def save_text(self):
        text = self.text_box.toPlainText()
        if text:
            file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "tamil_speech.docx", "Word Documents (*.docx)")
            if file_path:
                doc = Document()
                doc.add_paragraph(text)
                doc.save(file_path)
                self.text_box.append("✅ Saved successfully!")
        else:
            self.text_box.append("⚠️ No text to save!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TamilSpeechToTextApp()
    window.show()
    sys.exit(app.exec_())