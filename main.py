import sys
import json
import os
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QGraphicsOpacityEffect,
    QStatusBar,
    QFileDialog,
    QPlainTextEdit,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QCheckBox
)
from PyQt5.QtCore import (
    QThread,
    pyqtSignal,
    QUrl
)
from PyQt5.QtGui import QFont
import speech_recognition as sr
from translate import Translator
from gtts import gTTS


class SpeechRecognitionThread(QThread):
    recognition_result = pyqtSignal(str)
    status_signal = pyqtSignal(str)

    def __init__(self, recognizer):
        super().__init__()
        self.recognizer = recognizer

    def run(self):
        try:
            with sr.Microphone() as source:
                self.status_signal.emit("Listening...")
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source, timeout=5)

            try:
                self.status_signal.emit("Recognizing speech...")
                text = self.recognizer.recognize_google(audio)
                self.recognition_result.emit(text)
            except sr.UnknownValueError:
                self.status_signal.emit("Could not understand audio")
            except sr.RequestError as e:
                self.status_signal.emit(f"Error: {e}")
        except Exception as e:
            self.status_signal.emit(f"Error: {e}")


class VoiceConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Multi-Language Voice Transcriber & Translator')

        self.start_button = QPushButton('Start Recording', self)
        self.start_button.setFont(QFont('Arial', 14))

        self.spoken_label = QPlainTextEdit(self)
        self.spoken_label.setFont(QFont('Arial', 14))
        self.spoken_label.setReadOnly(True)

        self.translated_label = QPlainTextEdit(self)
        self.translated_label.setFont(QFont('Arial', 14))
        self.translated_label.setReadOnly(True)

        self.language_list = QListWidget(self)
        self.language_list.setFont(QFont('Arial', 12))
        self.language_list.setSelectionMode(QListWidget.MultiSelection)

        # Load language codes
        with open('language_codes.json', 'r') as f:
            self.language_dict = json.load(f)
        
        for lang in self.language_dict.keys():
            item = QListWidgetItem(lang)
            item.setCheckState(0)
            self.language_list.addItem(item)

        self.status_bar = QStatusBar(self)
        self.download_button = QPushButton('Download Audio', self)
        self.download_button.setEnabled(False)
        self.download_button.clicked.connect(self.download_audio)

        vbox = QVBoxLayout()
        vbox.addWidget(QLabel("Select Target Languages:"))
        vbox.addWidget(self.language_list)
        vbox.addWidget(self.start_button)
        vbox.addWidget(self.spoken_label)
        vbox.addWidget(self.translated_label)
        vbox.addWidget(self.status_bar)
        vbox.addWidget(self.download_button)

        self.setLayout(vbox)
        self.start_button.clicked.connect(self.start_recording)

        self.recognition_thread = SpeechRecognitionThread(sr.Recognizer())
        self.recognition_thread.recognition_result.connect(self.translate_and_play)
        self.recognition_thread.status_signal.connect(self.update_status)
        self.recognition_thread.finished.connect(self.on_recognition_finished)

        self.player = QMediaPlayer()

    def start_recording(self):
        self.start_button.setEnabled(False)
        self.spoken_label.clear()
        self.translated_label.clear()

        self.selected_languages = [
            self.language_dict[self.language_list.item(i).text()]
            for i in range(self.language_list.count())
            if self.language_list.item(i).checkState() == 2
        ]

        if self.selected_languages:
            self.recognition_thread.start()
        else:
            self.update_status("Please select at least one target language.")
            self.start_button.setEnabled(True)

    def translate_and_play(self, text):
        self.update_status("Translating text...")
        self.spoken_label.setPlainText('Spoken Text: ' + text)

        translated_texts = {}
        for lang in self.selected_languages:
            translator = Translator(to_lang=lang)
            translated_texts[lang] = translator.translate(text)

        display_text = ""
        for lang, translation in translated_texts.items():
            display_text += f"{lang}: {translation}\n"
            tts = gTTS(translation, lang=lang)
            tts.save(f"translated_audio_{lang}.mp3")

        self.update_status("Text translated and audio generated.")
        self.translated_label.setPlainText(display_text)
        self.download_button.setEnabled(True)

        # Play the first translated audio
        first_lang = self.selected_languages[0]
        media = QMediaContent(QUrl.fromLocalFile(os.path.abspath(f"translated_audio_{first_lang}.mp3")))
        self.player.setMedia(media)
        self.player.play()

    def on_recognition_finished(self):
        self.start_button.setEnabled(True)

    def update_status(self, status):
        self.status_bar.showMessage(status)

    def download_audio(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            for lang in self.selected_languages:
                os.rename(f"translated_audio_{lang}.mp3", os.path.join(folder_path, f"translated_audio_{lang}.mp3"))
            self.update_status("Audio files saved.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    converter_app = VoiceConverterApp()
    converter_app.show()
    sys.exit(app.exec_())
