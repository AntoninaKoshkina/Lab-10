import requests
import pyttsx3
import pyaudio
import vosk
import json
import os
import time
from bs4 import BeautifulSoup

class Speech:
    def __init__(self):
        self.speaker = 0
        self.tts = pyttsx3.init('sapi5')

    def set_voice(self, speaker):
        self.voices = self.tts.getProperty('voices')
        for count, voice in enumerate(self.voices):
            if count == 0:
                print('0')
                id = voice.id
            if speaker == count:
                id = voice.id
        return id

    def text2voice(self, speaker=0, text='Готов'):
        self.tts.setProperty('voice', self.set_voice(speaker))
        self.tts.say(text)
        self.tts.runAndWait()


class Recognize:
    def __init__(self):
        model = vosk.Model('model')
        self.record = vosk.KaldiRecognizer(model, 16000)
        self.stream()

    def stream(self):
        pa = pyaudio.PyAudio()
        self.stream = pa.open(format=pyaudio.paInt16,
                         channels=1,
                         rate=16000,
                         input=True,
                         frames_per_buffer=8000)


    def listen(self):
        while True:
            data = self.stream.read(4000, exception_on_overflow=False)
            if self.record.AcceptWaveform(data) and len(data) > 0:
                answer = json.loads(self.record.Result())
                if answer['text']:
                    yield answer['text']


def speak(text):
    speech = Speech()
    speech.text2voice(speaker=1, text=text)

def create_loripsum():
    try:
        response = requests.get("https://loripsum.net/api/10/short/headers")
        return response.text
    except requests.exceptions.HTTPError as http_err:
        speak(f"HTTP error occurred: {http_err}")
    except Exception as err:
        speak(f"An error occurred: {err}")
    return None

def remove_html(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    return soup.get_text()

rec = Recognize()
text_gen = rec.listen()
rec.stream.stop_stream()
speak('Starting')
time.sleep(0.5)
rec.stream.start_stream()



for text in text_gen:
    if text == 'stop':
        speak('Bee free')
        quit()

    elif text == 'make':
        loripsum_text = create_loripsum()
        speak('Quotes collected')

    elif text == 'read':
        if 'loripsum_text' in locals():
            speak(f"Here are some quotes: {remove_html(loripsum_text)}")
        else:
            speak("No quotes has been created yet.")

    elif text == 'save':
        if 'loripsum_text' in locals():
            with open("quotes.html", "w") as f:
                f.write(loripsum_text)
            speak("Quotes saved as html file")
        else:
            speak("No quotes has been created yet.")


    elif text == 'that':
        if 'loripsum_text' in locals():
            with open("pure_quotes.txt", "w", encoding="utf-8", errors="replace") as f:
                f.write(remove_html(loripsum_text))
            speak("Quotes saved as txt file")
        else:
            speak("No quotes has been created yet.")

    else:
        print(text)