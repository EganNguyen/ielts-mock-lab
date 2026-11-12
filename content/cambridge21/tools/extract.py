#!/usr/bin/env python3
"""Deterministic extraction helpers for Cambridge IELTS 21.

Reads the per-page text produced by pdftotext -layout and produces:
  - transcripts.json : listening audioscripts split by test/part with speaker turns
  - keys.json        : listening/reading answer keys per test
  - pages.json       : page-number map for every test section
"""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "raw"
PDF = "/Users/tim2k/Downloads/Cambridge Ielts 21.pdf"

TEST_START = {1: 11, 2: 33, 3: 55, 4: 76}
TEST_END = {1: 32, 2: 54, 3: 75, 4: 97}

SPEAKER_LABEL = re.compile(r"^([A-Z][A-Z .'()/-]{1,24}):\s*(.*)$")
MARGIN_TAIL = re.compile(r"\s{2,}\d{2,6}\s*$")
PAGE_FOOTER = re.compile(r"^\s*\d{1,3}\s*$")


def page_text(n: int) -> str:
    return (RAW / f"page-{n:03d}.txt").read_text(encoding="utf-8")


def page_lines(n: int) -> list[str]:
    return page_text(n).splitlines()


def clean_transcript_line(line: str) -> str:
    line = line.rstrip()
    line = MARGIN_TAIL.sub("", line)
    # OCR sometimes splits a printed question marker into digit groups ("07 5").
    line = re.sub(r"\s{2,}[OQ©]?\s?\d[\d\s/]{0,12}$", "", line)
    return line.strip()


def parse_transcripts() -> dict:
    """Parse pages 98-117 into {test: {part: [{speaker,text}]}}."""
    tests: dict[int, dict[int, list[dict]]] = {}
    current_test = None
    current_part = None
    last_line_idx = None
    pages = range(98, 118)
    for page in pages:
        for raw_line in page_lines(page):
            line = raw_line.rstrip()
            stripped = line.strip()
            if not stripped:
                continue
            if PAGE_FOOTER.match(stripped):
                continue
            m_test = re.fullmatch(r"TEST\s+(\d)", stripped)
            if m_test:
                current_test = int(m_test.group(1))
                tests.setdefault(current_test, {})
                current_part = None
                last_line_idx = None
                continue
            if stripped in {"Audioscripts", "Audioscripts |"}:
                continue
            if re.fullmatch(r"Test\s+\d", stripped) or stripped == "Audioscripts":
                continue
            m_part = re.fullmatch(r"PART\s+(\d)", stripped)
            if m_part:
                current_part = int(m_part.group(1))
                if current_test is None:
                    raise RuntimeError(f"PART heading before TEST heading on page {page}")
                tests[current_test].setdefault(current_part, [])
                last_line_idx = None
                continue
            if current_test is None or current_part is None:
                # Front matter / running headers.
                continue
            m_speaker = SPEAKER_LABEL.match(line)
            if m_speaker:
                speaker = m_speaker.group(1).strip()
                text = clean_transcript_line(m_speaker.group(2))
                turns = tests[current_test][current_part]
                turns.append({"speaker": speaker, "text": text})
                last_line_idx = (current_test, current_part, len(turns) - 1)
                continue
            # Continuation of the previous speaker turn.
            if last_line_idx is None:
                # Unlabelled monologue (Listening Part 4 is a lecture).
                turns = tests[current_test][current_part]
                turns.append({"speaker": "Lecturer", "text": clean_transcript_line(line)})
                last_line_idx = (current_test, current_part, len(turns) - 1)
                continue
            continuation = clean_transcript_line(line)
            if not continuation:
                continue
            t, p, i = last_line_idx
            prev = tests[t][p][i]["text"]
            # Hyphenated line breaks are already handled by pdftotext.
            tests[t][p][i]["text"] = (prev + " " + continuation).strip()
    return {str(t): {str(p): turns for p, turns in parts.items()} for t, parts in tests.items()}


KEY_HEADING = re.compile(r"^(Part \d+, Questions|Reading Passage \d+,)$")
KEY_RANGE = re.compile(r"^(\d{1,2})(?:\s*(?:&|and)\s*(\d{1,2}))?\s+(.*)$")


def normalize_key_value(raw: str) -> tuple[list[str], bool]:
    """Return accepted spellings and whether the answer is a two-letter pick."""
    raw = raw.strip()
    raw = re.sub(r"\s{2,}IN EITHER ORDER.*$", "", raw, flags=re.I)
    raw = raw.strip(" .,")
    if not raw:
        return [], False
    if re.fullmatch(r"[A-J]", raw):
        return [raw], False
    # Keys use " / " or " I " (OCR of a slash) as spelling alternatives.
    parts = re.split(r"\s*(?:/|\bI\b|\|)\s*", raw)
    values = [p.strip().strip(".,") for p in parts if p.strip().strip(".,")]
    expanded: list[str] = []
    for value in values:
        expanded.append(value)
        # "(s)" marks an optional plural and parenthetical words mark optional
        # additions. Accept every reading a candidate could reasonably produce.
        if "(s)" in value:
            expanded.append(value.replace("(s)", "s"))
            expanded.append(value.replace("(s)", ""))
        if re.search(r"\([^)]*\)", value):
            no_paren = re.sub(r"\s*\([^)]*\)", "", value).strip()
            keep_paren = re.sub(r"\(([^)]*)\)", r"\1", value).strip()
            expanded.extend([no_paren, keep_paren])
    seen: list[str] = []
    for value in expanded:
        value = re.sub(r"\s+", " ", value).strip(" .,")
        if value and value not in seen:
            seen.append(value)
    two_letters = len(seen) == 2 and all(re.fullmatch(r"[A-Z]", v) for v in seen)
    return seen, two_letters


def parse_keys() -> dict:
    keys: dict[str, dict[str, dict[str, list[str]]]] = {}
    current_test = None
    current_skill = None
    pending_pair: tuple[int, int] | None = None
    pending_letters: list[str] = []
    for page in range(118, 126):
        raw = subprocess.run(
            ["pdftotext", "-f", str(page), "-l", str(page), "-raw", PDF, "-"],
            capture_output=True, text=True, check=True,
        ).stdout
        lines = [line.strip() for line in raw.splitlines()]
        for stripped in lines:
            if not stripped:
                continue
            m = re.fullmatch(r"TEST\s+(\d)", stripped)
            if m:
                current_test = m.group(1)
                continue
            if stripped in ("LISTENING", "READING"):
                current_skill = stripped.lower()
                continue
            if current_test is None or current_skill is None:
                continue
            if stripped.startswith("If you score") or "answer key" in stripped.lower():
                continue
            if re.match(r"^(Part \d|Reading Passage)", stripped):
                continue
            pair = re.fullmatch(r"(\d{1,2})\s*&\s*(\d{1,2})\s+IN\s*EITHER\s*ORDER", stripped, re.I)
            if pair:
                pending_pair = (int(pair.group(1)), int(pair.group(2)))
                pending_letters = []
                continue
            if pending_pair and re.fullmatch(r"[A-Z]", stripped):
                pending_letters.append(stripped)
                if len(pending_letters) == 2:
                    a, b = pending_pair
                    bucket = keys.setdefault(current_test, {}).setdefault(current_skill, {})
                    bucket[str(a)] = list(pending_letters)
                    bucket[str(b)] = list(pending_letters)
                    pending_pair = None
                continue
            m = re.match(r"^(\d{1,2})\s+(.+)$", stripped)
            if not m:
                continue
            num = int(m.group(1))
            if not (1 <= num <= 40):
                continue
            values, _two = normalize_key_value(m.group(2))
            if values:
                if len(values) == 1 and values[0].upper() == "NOTGIVEN":
                    values = ["NOT GIVEN"]
                if len(values) == 1 and values[0].upper() == "INTHEEITHERORDER":
                    continue
                keys.setdefault(current_test, {}).setdefault(current_skill, {})[str(num)] = values
    return keys


def repair_two_letter_keys(keys: dict) -> dict:
    """Re-parse pages to attach both letters for 'choose TWO' groups."""
    current_test = None
    current_skill = None
    for page in range(118, 126):
        lines = page_lines(page)
        text = "\n".join(lines)
        m = re.search(r"TEST\s+(\d)", text)
        if m:
            current_test = m.group(1)
        head = "\n".join(lines[:8])
        if re.search(r"^LISTENING$", head, re.M):
            current_skill = "listening"
        elif re.search(r"^READING$", head, re.M):
            current_skill = "reading"
        if current_test is None or current_skill is None:
            continue
        bucket = keys.setdefault(current_test, {}).setdefault(current_skill, {})
        i = 0
        while i < len(lines):
            stripped = lines[i].strip()
            m_pair = re.fullmatch(r"(\d{1,2})\s*&\s*(\d{1,2})\s+IN EITHER ORDER", stripped, re.I)
            if m_pair:
                a, b = int(m_pair.group(1)), int(m_pair.group(2))
                collected = []
                j = i + 1
                while j < len(lines) and len(collected) < 2:
                    candidate = lines[j].strip()
                    if re.fullmatch(r"[A-Z]", candidate):
                        collected.append(candidate)
                    elif candidate:
                        break
                    j += 1
                if len(collected) == 2:
                    bucket[str(a)] = [collected[0], collected[1]]
                    bucket[str(b)] = [collected[0], collected[1]]
                    i = j - 1
            i += 1
    for test in keys.values():
        for skill in test.values():
            skill.pop("_pending", None)
    return keys


PAGE_MAP = {
    "1": {
        "listening": list(range(11, 17)),
        "reading": list(range(17, 30)),
        "writing": [30, 31],
        "speaking": [32],
    },
    "2": {
        "listening": list(range(33, 39)),
        "reading": list(range(39, 52)),
        "writing": [52, 53],
        "speaking": [54],
    },
    "3": {
        "listening": list(range(55, 61)),
        "reading": list(range(61, 73)),
        "writing": [73, 74],
        "speaking": [75],
    },
    "4": {
        "listening": list(range(76, 82)),
        "reading": list(range(82, 95)),
        "writing": [95, 96],
        "speaking": [97],
    },
}


def main() -> None:
    out = ROOT / "meta"
    out.mkdir(exist_ok=True)
    transcripts = parse_transcripts()
    (out / "transcripts.json").write_text(json.dumps(transcripts, indent=2, ensure_ascii=False))
    keys = parse_keys()
    (out / "keys.json").write_text(json.dumps(keys, indent=2, ensure_ascii=False))
    (out / "pages.json").write_text(json.dumps(PAGE_MAP, indent=2))
    for test in sorted(transcripts):
        for part in sorted(transcripts[test]):
            turns = transcripts[test][part]
            words = sum(len(t["text"].split()) for t in turns)
            print(f"test {test} part {part}: {len(turns)} turns, {words} words")
    for test in sorted(keys):
        for skill in sorted(keys[test]):
            got = len([k for k in keys[test][skill] if k.isdigit()])
            print(f"keys test {test} {skill}: {got} answers")


if __name__ == "__main__":
    main()
