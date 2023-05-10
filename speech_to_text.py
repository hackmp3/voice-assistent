from vosk import Model, KaldiRecognizer
import pyaudio
import json

model = Model("model small")
rec = KaldiRecognizer(Model("model small"), 16000)
p = pyaudio.PyAudio()
stream = p.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=16000,
    input=True,
    frames_per_buffer=16000
)
stream.start_stream()

def listen():
    while True:
        data = stream.read(8000, exception_on_overflow=False)
        if (rec.AcceptWaveform(data)) and (len(data) > 0):
            anwswer = json.loads(rec.Result())
            if anwswer['text']:
                    print(anwswer['text'])
                    yield anwswer['text']

