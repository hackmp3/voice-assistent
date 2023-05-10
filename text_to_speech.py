import torch
import sounddevice as sd
import time



language = 'ru'
model_id = 'v3_1_ru'
sample_rate = 48000
speaker = 'eugene'
put_accent = True
put_yo = True
device = torch.device('cpu')
model1, _ = torch.hub.load(repo_or_dir='snakers4/silero-models',
                          model='silero_tts',
                          language=language,
                          speaker=model_id)
model1.to(device)

def talk(text):
    audio = model1.apply_tts(text=text,
                            speaker=speaker,
                            sample_rate=sample_rate,
                            put_accent=put_accent,
                            put_yo=put_yo)

    sd.play(audio, sample_rate)
    time.sleep((len(audio) / sample_rate))
    sd.stop()


