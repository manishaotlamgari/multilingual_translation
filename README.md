# Multilingual Voice Transcriber and Translator

This project implements a **Multilingual Voice Transcriber and Translator** using machine learning to translate text from one language to different languages, generates translated text and translated audio files. It supports multiple languages and demonstrates preprocessing, training, evaluation, and real-time translation using a trained model.
This application is built with PyQt5, Google Text-to-Speech (gTTS), and the translate and speech_recognition libraries.

# Features
- Translate text to multiple languages
- Preprocessing pipeline for tokenization and normalization
- Encoder-decoder (Seq2Seq)
- Model training and evaluation
- Real-time translation via notebook interface

# Model Overview

- Voice Transcription: The application can transcribe spoken language into text using Google's Speech Recognition service.
- Translation: The transcribed text can be translated into various languages using the translate library.
- Text-to-Speech: The translated text can be converted back into speech using Google's Text-to-Speech service (gTTS).
- Download Audio: The audio of the translated text can be downloaded as an MP3 file.
- Copy Text: Both the transcribed and translated texts can be copied to the clipboard.
  
# Usage
Run the application: python main.py
- Select the target language for translation from the dropdown menu.
- Click the 'Upload' button to upload the voice transcription.
- The application will transcribe the uploaded language file into text, translate the text into the selected languages, and    then convert the translated text back into speech.
- The 'Download Audio' button allows you to download the audio of the translated text as an MP3 file.

