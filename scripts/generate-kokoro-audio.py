#!/usr/bin/env python3
"""Generate all exam voice assets with Kokoro-82M (ONNX, local, no API keys)."""
import json, subprocess, shutil
from pathlib import Path
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / 'content/academic/test001.json').read_text())
MODEL = ROOT / 'models/kokoro/kokoro-v1.0.onnx'
VOICES = ROOT / 'models/kokoro/voices-v1.0.bin'
OUT = ROOT / 'apps/web/public/media'
TMP = ROOT / 'scripts/kokoro-tmp'
shutil.rmtree(TMP, ignore_errors=True)
TMP.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)
(OUT / 'speaking/examiner').mkdir(parents=True, exist_ok=True)

kokoro = Kokoro(str(MODEL), str(VOICES))
SR = 24000

VOICE = {
    'Narrator': ('bm_george', 0.80),
    'Guide': ('bm_george', 0.84),
    'Lecturer': ('bm_lewis', 0.82),
    'Mia': ('bf_emma', 0.87),
    'Priya': ('bf_alice', 0.87),
    'Elena': ('bf_isabella', 0.86),
    'Tom': ('bm_fable', 0.84),
}

def silence(seconds):
    return np.zeros(int(SR * seconds), dtype=np.float32)

def synth(part, line):
    voice, speed = VOICE.get(line['speaker'], ('bm_george', 0.84))
    samples, sr = kokoro.create(line['text'], voice=voice, speed=speed, lang='en-gb')
    if sr != SR:
        raise RuntimeError(f'unexpected sample rate {sr}')
    return np.asarray(samples, dtype=np.float32)

def encode_mp3(wav_path, mp3_path, bitrate='96k'):
    subprocess.run(['ffmpeg','-y','-i',str(wav_path),'-c:a','libmp3lame','-b:a',bitrate,str(mp3_path)], check=True, capture_output=True)

# Listening: four continuous parts, built from per-speaker turns.
for part in DATA['listening']:
    pnum = part['number']
    pieces = [silence(1.1)]
    previous = None
    for line in part['transcript']:
        pieces.append(synth(part, line))
        speaker = line['speaker']
        if speaker == 'Narrator':
            pieces.append(silence(1.1))
        elif previous and speaker != previous:
            pieces.append(silence(0.48))
        else:
            pieces.append(silence(0.28))
        previous = speaker
    pieces.append(silence(24))
    audio = np.concatenate(pieces)
    wav = TMP / f'part{pnum}.wav'
    sf.write(wav, audio, SR)
    mp3 = OUT / 'listening' / f'part{pnum}.mp3'
    mp3.parent.mkdir(parents=True, exist_ok=True)
    encode_mp3(wav, mp3)
    print(f'Kokoro listening part {pnum}: {len(audio)/SR:.1f}s -> {mp3.relative_to(ROOT)}')

# Speaking examiner prompts, one file per question, plus intro/cue.
examiner_voice = 'bf_emma'
def examiner(text, name, speed=0.88):
    samples, sr = kokoro.create(text, voice=examiner_voice, speed=speed, lang='en-gb')
    wav = TMP / f'{name}.wav'
    sf.write(wav, np.asarray(samples, dtype=np.float32), sr)
    mp3 = OUT / 'speaking/examiner' / f'{name}.mp3'
    encode_mp3(wav, mp3, '80k')
    print(f'Kokoro speaking {name}: {len(samples)/sr:.1f}s')

examiner('Good morning. My name is Emma, and I will be your examiner today. This is the speaking test. I am going to ask you some questions about yourself, then give you a topic to talk about, and finally discuss some related ideas with you. Let us begin.', 'intro', 0.88)
parts = DATA['speaking']
for part in parts:
    for q in part.get('questions', []):
        examiner(q['text'], q['id'])
    if part.get('cueCard'):
        cue = part['cueCard']
        examiner(f"Now, I would like you to talk about a topic. Here is your cue card. {cue['topic']}", 'cue', 0.86)
        examiner("You have one minute to prepare. You can make some notes if you wish. I will tell you when to begin.", 'prep', 0.86)

shutil.rmtree(TMP, ignore_errors=True)
print('Done.')
