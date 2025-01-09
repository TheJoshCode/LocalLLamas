import os
import threading
import pyttsx3
import speech_recognition as sr
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLabel, QComboBox, QWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from ctransformers import AutoModelForCausalLM

# Initialize TTS engine
def speak(text):
    """Convert text to speech."""
    engine = pyttsx3.init()
    engine.setProperty('rate', 200)  # Adjust speaking speed
    engine.say(text)
    engine.runAndWait()

# Load Llama model
def get_model_path(filename):
    """Return the full path to the model file in the models/ directory."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, "models", filename)

def list_gguf_models():
    """List all .gguf models in the models/ folder."""
    models_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models")
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)  # Create the directory if it doesn't exist
    return [f for f in os.listdir(models_dir) if f.endswith(".gguf")]

current_model = None

def load_model(model_name):
    """Load the selected Llama model."""
    global current_model
    model_path = get_model_path(model_name)
    print(f"Loading model from: {model_path}")
    current_model = AutoModelForCausalLM.from_pretrained(
        model_path,
        model_type="llama",
        gpu_layers=-1  # Fully offload to GPU
    )

# Chat with AI
def chat_with_ai(prompt):
    """Generate a response using the AI model."""
    if current_model is None:
        return "No model loaded. Please select a model."
    print("Generating response...")
    response = current_model(f"[INST] <<SYS>>\nYou are a helpful assistant.\n<</SYS>>\n{prompt}[/INST]")
    return response.strip()

# Microphone-based listening
recognizer = sr.Recognizer()

def listen():
    """Continuously listen for user input via microphone."""
    print("Listening for user input...")
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        while True:
            try:
                print("Waiting for speech...")
                audio = recognizer.listen(source, timeout=5)
                print("Processing speech...")
                return recognizer.recognize_google(audio)
            except sr.UnknownValueError:
                print("Could not understand audio.")
            except sr.WaitTimeoutError:
                print("Listening timeout. Retrying...")

# GUI Application
class LocalLLamas(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window setup
        self.setWindowTitle("LocalLLamas")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("background-color: #F5F7FA;")

        # Fonts
        self.heading_font = QFont("Arial", 18, QFont.Bold)
        self.text_font = QFont("Arial", 12)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        # Heading
        self.heading_label = QLabel("LocalLLamas")
        self.heading_label.setFont(self.heading_font)
        self.heading_label.setStyleSheet("color: #4A90E2;")
        self.heading_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.heading_label)

        # Model Selector
        self.model_selector_label = QLabel("Select Llama Model:")
        self.model_selector_label.setFont(self.text_font)
        layout.addWidget(self.model_selector_label)

        self.model_selector = QComboBox()
        self.model_selector.setFont(self.text_font)
        self.model_selector.addItems(list_gguf_models())
        self.model_selector.setStyleSheet("""
            background-color: #E1F5FE;
            border: 1px solid #4A90E2;
            border-radius: 5px;
            padding: 5px;
            color: #4A90E2;
        """)
        self.model_selector.currentIndexChanged.connect(self.on_model_change)
        layout.addWidget(self.model_selector)

        # AI Response
        self.response_label = QLabel("AI Response:")
        self.response_label.setFont(self.text_font)
        layout.addWidget(self.response_label)

        self.response_text = QLabel("")
        self.response_text.setFont(self.text_font)
        self.response_text.setStyleSheet("""
            color: #007AFF;
            font-weight: bold;
            background-color: #E8F4FD;
            padding: 10px;
            border-radius: 5px;
        """)
        self.response_text.setWordWrap(True)
        layout.addWidget(self.response_text)

        central_widget.setLayout(layout)

        # Start background thread for listening
        self.listening_thread = threading.Thread(target=self.listen_loop, daemon=True)
        self.listening_thread.start()

        # Load initial model
        if self.model_selector.count() > 0:
            self.on_model_change(0)

    def on_model_change(self, index):
        """Handle model change event."""
        model_name = self.model_selector.itemText(index)
        if model_name:
            threading.Thread(target=load_model, args=(model_name,)).start()

    def listen_loop(self):
        """Continuously listen for user input and generate responses."""
        while True:
            user_input = listen()
            if user_input:
                print(f"You said: {user_input}")
                ai_response = chat_with_ai(user_input)
                print(f"AI: {ai_response}")
                self.response_text.setText(ai_response)
                speak(ai_response)


# Run the App
if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = LocalLLamas()
    window.show()
    sys.exit(app.exec_())
