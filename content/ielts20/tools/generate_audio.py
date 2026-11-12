#!/usr/bin/env python3
"""Generate IELTS 20 listening audio with Kokoro-82M."""
from __future__ import annotations

import json
import re
import subprocess
import tempfile
from pathlib import Path

import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

ROOT = Path(__file__).resolve().parents[3]
MODEL = ROOT / "models/kokoro/kokoro-v1.0.onnx"
VOICES = ROOT / "models/kokoro/voices-v1.0.bin"
OUT = ROOT / "apps/web/public/media/listening"
TMP = Path(tempfile.mkdtemp(prefix="ielts20-listening-"))
SR = 24000

FEMALE = ["bf_emma", "bf_alice", "bf_isabella", "bf_lily"]
MALE = ["bm_george", "bm_lewis", "bm_fable", "bm_daniel"]
FEMALE_KEYS = ("WOMAN", "CARER", "SANDRA", "TAMARA", "SHELLEY", "HEATHER",
               "ROSIE", "MAYA", "NARRATOR", "STUDENT 1")
MALE_KEYS = ("MAN", "FRIEND", "COLIN", "FINN", "STEVE", "ARCHAEOLOGIST",
             "LECTURER", "GUIDE", "HOUSE OWNER", "STUDENT 2")


def voice_for(speaker: str, used: dict[str, str]) -> tuple[str, float]:
    if speaker in used:
        voice = used[speaker]
        return voice, 0.90 if voice.startswith("bf") else 0.92
    key = speaker.upper()
    pool = FEMALE if any(k in key for k in FEMALE_KEYS) else MALE
    index = len([v for v in used.values() if v in pool]) % len(pool)
    voice = pool[index]
    speed = [0.90, 0.94, 0.88, 0.92][len(used) % 4]
    used[speaker] = voice
    return voice, speed


def speech_text(text: str) -> str:
    text = text.replace("£", "")
    text = re.sub(r"\bE\.g\.", "For example,", text)
    text = re.sub(r"\be\.g\.", "for example", text)
    text = re.sub(r"\bi\.e\.", "that is", text)
    text = re.sub(r"\betc\.", "etcetera", text)
    text = re.sub(r"\.{3,}", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def chunks(text: str, limit: int = 240) -> list[str]:
    sentences = re.split(r"(?<=[.!?])\s+", text)
    out, buf = [], ""
    for sentence in sentences:
        if len(buf) + len(sentence) + 1 <= limit or not buf:
            buf = (buf + " " + sentence).strip()
        else:
            out.append(buf)
            buf = sentence
    if buf:
        out.append(buf)
    final: list[str] = []
    for chunk in out:
        while len(chunk) > limit * 1.6:
            cut = chunk.rfind(",", 0, limit)
            if cut < 80:
                cut = limit
            final.append(chunk[:cut].strip())
            chunk = chunk[cut:].strip()
        if chunk:
            final.append(chunk)
    return final


def main() -> None:
    exams = sorted((ROOT / "content/academic").glob("ielts20-test*.json"))
    if not exams:
        raise SystemExit("no IELTS 20 exam content found")
    kokoro = Kokoro(str(MODEL), str(VOICES))
    for exam_path in exams:
        exam = json.loads(exam_path.read_text())
        exam_dir = OUT / exam["id"]
        exam_dir.mkdir(parents=True, exist_ok=True)
        print(f"== {exam['id']}", flush=True)
        for part in exam["listening"]:
            number = part["number"]
            mp3 = exam_dir / f"part{number}.mp3"
            if mp3.exists() and mp3.stat().st_size > 1_000_000:
                print(f"  part {number}: exists, skipping", flush=True)
                continue
            pieces = [np.zeros(int(SR * 0.6), dtype=np.float32)]
            used: dict[str, str] = {}
            intro = f"Test {exam['id'][-1]}. Listening. Part {number}."
            samples, _ = kokoro.create(intro, voice="bf_emma", speed=0.88, lang="en-gb")
            pieces.append(np.asarray(samples, dtype=np.float32))
            pieces.append(np.zeros(int(SR * 1.4), dtype=np.float32))
            previous = None
            for turn in part["transcript"]:
                voice, speed = voice_for(turn["speaker"], used)
                gap = 0.50 if previous and previous != turn["speaker"] else 0.22
                if previous:
                    pieces.append(np.zeros(int(SR * gap), dtype=np.float32))
                for chunk in chunks(speech_text(turn["text"])):
                    samples, sr = kokoro.create(chunk, voice=voice, speed=speed, lang="en-gb")
                    if sr != SR:
                        raise RuntimeError(f"unexpected sample rate {sr}")
                    pieces.append(np.asarray(samples, dtype=np.float32))
                    pieces.append(np.zeros(int(SR * 0.20), dtype=np.float32))
                previous = turn["speaker"]
            pieces.append(np.zeros(int(SR * 1.8), dtype=np.float32))
            audio = np.concatenate(pieces)
            wav = TMP / f"{exam['id']}-part{number}.wav"
            sf.write(wav, audio, SR)
            subprocess.run(["ffmpeg", "-y", "-i", str(wav), "-c:a", "libmp3lame",
                            "-b:a", "96k", str(mp3)], check=True, capture_output=True)
            wav.unlink(missing_ok=True)
            print(f"  part {number}: {len(audio)/SR/60:.1f} min, {mp3.stat().st_size//1024} KB", flush=True)
    print("done", flush=True)


if __name__ == "__main__":
    main()
