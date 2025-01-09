![](https://i.imgur.com/iNRJ6Ey.png)
# LocalLLamas - AI Chat with Voice Recognition and Text-to-Speech

LocalLLamas is a desktop application that integrates AI chat functionality, voice recognition, and text-to-speech (TTS) capabilities. It allows users to interact with AI models through their voice, receive responses from the AI, and have those responses read aloud.

## Features
- **Voice Interaction**: Speak to the application, and it will recognize your speech and generate AI responses.
- **Text-to-Speech**: The AI responses are read aloud using the `pyttsx3` library, with adjustable speaking speed.
- **Model Loading**: Dynamically load Llama language models (.gguf files) from the `models/` directory.
- **Real-Time AI Responses**: The AI responds to user queries based on the selected model and speaks the response aloud.
- **PyQt5 GUI**: A simple GUI built with PyQt5 that allows users to select models, view responses, and interact with the AI.

## Requirements
- Python 3.7+
- PyQt5
- pyttsx3
- speech_recognition
- ctransformers
- Llama (.gguf) models (placed in the `models/` directory)

### Install Dependencies
To install the required dependencies, you can use `pip`:

```bash
pip install pyqt5 pyttsx3 SpeechRecognition ctransformers
```

# Clone the repository:

```bash
git clone https://github.com/yourusername/LocalLLamas.git
cd LocalLLamas
```
Place your .gguf models in the models/ directory. This directory will be automatically scanned for available models.

# Run the application:

```bash
python app.py
```
# How It Works

- Text-to-Speech (TTS): The speak() function uses pyttsx3 to convert the AI's text response into speech.
- Model Loading: The AutoModelForCausalLM from the ctransformers library loads a selected model. The models are expected to be in the models/ directory with .gguf file extensions.
- Speech Recognition: The listen() function continuously listens for user speech and converts it to text using the Google Web Speech API.
- AI Interaction: The speech input is sent to the AI model as a prompt, and the model generates a response. The response is then displayed in the GUI and spoken aloud.
- GUI: The PyQt5-based GUI allows users to:
  - Select a model from a list of .gguf files.
  - View the AI's response.
  - Interact with the AI by speaking into the microphone.
# Application Flow

- Model Selection: The user selects a model from a drop-down list.
- Speech Recognition: The application listens for user input, and when speech is detected, it converts it into text.
- AI Response: The input text is passed to the selected AI model, and the response is generated.
- Text-to-Speech: The AI's response is displayed in the GUI and read aloud.
- Continuous Listening: The application continuously listens for new input and responds accordingly.
# Contributing
- Feel free to fork this repository, contribute improvements, or report issues. If you'd like to submit a pull request, ensure that your changes are well-documented and tested.
