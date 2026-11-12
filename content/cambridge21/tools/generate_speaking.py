#!/usr/bin/env python3
"""Generate examiner speech for the speaking section, one set per exam."""
from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "apps/web/public/media/speaking/examiner"
TMP = Path(tempfile.mkdtemp(prefix="ielts-speaking-"))
SR = 24000
INTRO = "Good morning. My name is Emma, and I will be your examiner today. This is the speaking test. Let us begin."
PREP = "You have one minute to prepare. You can make some notes if you wish. I will tell you when to begin."


def main() -> None:
    kokoro = Kokoro(str(ROOT / "models/kokoro/kokoro-v1.0.onnx"), str(ROOT / "models/kokoro/voices-v1.0.bin"))
    exams = sorted((ROOT / "content/academic").glob("cambridge21-test*.json"))
    for path in exams:
        exam = json.loads(path.read_text())
        target = OUT / exam["id"]
        target.mkdir(parents=True, exist_ok=True)
        jobs: dict[str, str] = {"intro": INTRO, "prep": PREP}
        for part in exam["speaking"]:
            for question in part.get("questions", []):
                jobs[question["id"]] = question["text"]
            cue = part.get("cueCard")
            if cue:
                jobs["cue"] = (
                    f"Now I would like you to talk about a topic. Here is your cue card. {cue['topic']} "
                    f"You should say: {'. '.join(cue['bullets'])}. {cue['rounding']}"
                )
        for name, text in jobs.items():
            samples, sr = kokoro.create(text, voice="bf_emma", speed=0.9, lang="en-gb")
            wav = TMP / f"{exam['id']}-{name}.wav"
            sf.write(wav, np.asarray(samples, dtype=np.float32), sr)
            mp3 = target / f"{name}.mp3"
            subprocess.run(["ffmpeg", "-y", "-i", str(wav), "-c:a", "libmp3lame", "-b:a", "80k", str(mp3)],
                           check=True, capture_output=True)
            wav.unlink(missing_ok=True)
        print(f"{exam['id']}: {len(jobs)} examiner clips", flush=True)
    print("done", flush=True)


if __name__ == "__main__":
    main()
