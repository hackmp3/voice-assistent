import text_to_speech
import config
from num2t4ru import num2text
from vosk import Model, KaldiRecognizer
import pyaudio
import json
import datetime
import webbrowser
# import openai #если хотите использовать чат-gpt то тогда используйте этот модуль

# openai.api_key = "" #если хотите использовать чат-gpt то введите api ключ chat-gpt


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

def command(anwswer):
    for anwswer in listen():
        # i1 = 0 переменная для openai
        if anwswer in config.sttime:
            timeget()
        elif anwswer in config.stgithub:
            webbrowser.open('github.com')
            text_to_speech.talk("открыл.")
        """ #сам комманда openai
        elif anwswer in config.stapi:
            i1 = 1
            text_to_speech.talk("задавайте вопрос.")
        elif i1 == 1:
            try:
                i1 = 0
                text_to_speech.talk("подождите.")
                response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=anwswer,
                    temperature=0.5,
                    max_tokens=1000,
                    top_p=1.0,
                    frequency_penalty=0.5,
                    presence_penalty=0.0,
                    stop=["You:"]
                )
                textbot = response['choices'][0]['text']
                print("нейросеть : ", textbot)
                text_to_speech.talk(textbot)
            except:
                text_to_speech.talk("включите интернет. либо введдите апи ключ.")
                """


def datetimestart():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 11:
        text_to_speech.talk("доброе утро. Чем могу помочь.")
    if hour >= 12 and hour < 18:
        text_to_speech.talk("добрый день. Чем могу помочь.")
    if hour >= 18 and hour <= 20:
        text_to_speech.talk("добрый вечер. Чем могу помочь.")
    if hour > 20 and hour < 24:
        text_to_speech.talk("доброй ночи. Чем могу помочь.")

def timeget():
    hour = int(datetime.datetime.now().hour)
    minute = int(datetime.datetime.now().minute)
    minute_word = ((u'минута', u'минуты', u'минут'), 'f')
    hour_word = ((u'час', u'часа', u'часов'), 'm')
    hourminute_word = "сейчас " + num2text(hour, hour_word) + "." + num2text(minute, minute_word) + "."
    text_to_speech.talk(hourminute_word)
    hourminute_word = ""

def main():
    datetimestart()
    command(listen())

if __name__ == "__main__":
    main()