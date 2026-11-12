#!/usr/bin/env python3
"""Extract IELTS 19 audioscripts and answer keys from OCR text."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OCR = ROOT / "ocr-tess"

TEST_RANGES = {
    1: {"listening": [10, 15], "reading": [16, 30], "writing": [31, 32], "speaking": [33]},
    2: {"listening": [34, 40], "reading": [41, 54], "writing": [53, 54], "speaking": [55]},
    3: {"listening": [56, 62], "reading": [63, 77], "writing": [76, 77], "speaking": [78]},
    4: {"listening": [79, 84], "reading": [85, 98], "writing": [97, 98], "speaking": [99]},
}
TRANSCRIPT_PAGES = range(100, 121)
MONOLOGUE = {(1, 2): "SPEAKER", (1, 4): "LECTURER", (2, 2): "DAVID", (2, 4): "STUDENT",
             (3, 4): "LECTURER", (4, 2): "LIZ", (4, 4): "LECTURER"}

SPEAKER = re.compile(r"^([A-Za-z][A-Za-z .'()/-]{1,24})[:.!?\]]\s*(.*)$")
NAMES = {"SALLY", "JOHN", "MARIE", "COLIN", "COLEMAN", "COLEMMAN", "COTEMAN", "WOMAN", "MAN", "BELLA", "DON", "LEON", "SHANNON", "PRESENTER", "JENNY", "JAKE", "KAEDEN", "KIERAN", "JANE", "CHARLOTTE", "CLARE", "LIZ", "NARRATOR", "LECTURER"}
SKIP = re.compile(
    r"^(Audioscripts|Test\s*\d+|TEST\s*\d+|PART\s*\d+|Listening|Reading|TELEGRAM.*|@cambridge_library|\d{1,3})$"
)
MARKER = re.compile(r"\s+(?:Q\s?[lI]?\d{1,3}|[OQ©]\s?\d{1,3}|Q[lI])\s*$")


def page_text(n: int) -> str:
    return (OCR / f"ocr-{n:03d}.txt").read_text(encoding="utf-8", errors="ignore")


def clean_line(line: str) -> str:
    line = line.replace("|", "I")
    line = line.replace("\u00ad", "").replace("\u2019", "'").replace("\u2018", "'")
    line = line.replace("\u201c", '"').replace("\u201d", '"').replace("\u2014", " - ")
    line = re.sub(r"\s+", " ", line).strip()
    line = MARKER.sub("", line).strip()
    line = re.sub(r"\s*@?Q\s?[lI]?\d{1,3}\b", " ", line).strip()
    line = re.sub(r"\bQ[a-zA-Z]{1,2}\b", " ", line).strip()
    line = line.replace("We invoice you afterwards", "We'll invoice you afterwards")
    line = line.replace("thenit'son", "then it's on").replace("fellonthe", "fell on the")
    line = re.sub(r"@\d+", " ", line)
    line = re.sub(r"\s+", " ", line)
    line = re.sub(r"\s*\.\s*(?:\.\s*){2,}", "... ", line).strip()
    line = re.sub(r"^\.\.\s*", "... ", line)
    line = re.sub(r"^[_\-\u2014]\s*", "", line).strip()
    return line


def parse_transcripts() -> dict:
    tests: dict[int, dict[int, list[dict]]] = {}
    test = None
    part = None
    for page in TRANSCRIPT_PAGES:
        for raw in page_text(page).splitlines():
            line = raw.rstrip()
            stripped = line.strip()
            if not stripped:
                continue
            m = re.fullmatch(r"TEST\s+(\d)", stripped)
            if m:
                test = int(m.group(1))
                tests.setdefault(test, {})
                part = None
                continue
            m = re.match(r"PART\s+([1-4])\b\D*$", stripped)
            if m:
                part = int(m.group(1))
                if test is None:
                    raise RuntimeError(f"PART before TEST on page {page}")
                tests[test].setdefault(part, [])
                continue
            if SKIP.match(stripped):
                continue
            if test is None or part is None:
                continue
            turns = tests[test][part]
            m = SPEAKER.match(line)
            if m and m.group(1).strip().upper() in NAMES:
                name = m.group(1).strip().upper().rstrip(".!?")
                if name in {"COLEMAN", "COTEMAN"}:
                    name = "COLEMAN"
                text = clean_line(m.group(2))
                turns.append({"speaker": name, "text": text})
                continue
            text = clean_line(line)
            if not text or text.lower().startswith(("cambridge university", "978-", "with resource bank")):
                continue
            if turns:
                turns[-1]["text"] = (turns[-1]["text"] + " " + text).strip()
            else:
                turns.append({"speaker": MONOLOGUE.get((test, part), "Lecturer"), "text": text})
    return {str(t): {str(p): turns for p, turns in parts.items()} for t, parts in tests.items()}


if __name__ == "__main__":
    transcripts = parse_transcripts()
    out = ROOT / "meta" / "transcripts.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(transcripts, indent=2, ensure_ascii=False) + "\n")
    for t in sorted(transcripts):
        for p in sorted(transcripts[t]):
            turns = transcripts[t][p]
            words = sum(len(x["text"].split()) for x in turns)
            print(f"test {t} part {p}: {len(turns)} turns, {words} words | {turns[0]['text'][:70]!r} ... {turns[-1]['text'][-70:]!r}")
