#!/usr/bin/env python3
"""Extract IELTS 20 audioscripts and page map from the per-page layout text."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "raw"

PAGE_MAP = {
    "1": {"listening": list(range(3, 10)), "reading": list(range(11, 27)),
          "writing": [28, 29], "speaking": [33]},
    "2": {"listening": list(range(39, 46)), "reading": list(range(47, 63)),
          "writing": [64, 65, 66], "speaking": [71]},
    "3": {"listening": list(range(77, 85)), "reading": list(range(86, 102)),
          "writing": [103, 104], "speaking": [108]},
    "4": {"listening": list(range(114, 121)), "reading": list(range(122, 137)),
          "writing": [138, 139], "speaking": [143]},
}

# The scripts begin after the sample speaking answers.
SCRIPT_PAGES = range(148, 183)

LABELS = [
    "Speaker 1 (Woman Carer)", "Speaker 2 (Friend)", "Speaker 1 (Woman)",
    "Speaker 1 (Tamara)", "Speaker 2 (Dev)", "Speaker 1 (Man)",
    "Speaker 2 (Sandra)", "Speaker (Guide)", "Narrator/Instructor",
    "Design and Technology Lecturer", "Steve Wayne Wright (Elmley Town Council)",
    "Archaeologist (Hayden)", "Heather McCallum", "House Owner", "Shelley Meyer",
    "Student 1", "Student 2", "Lecturer", "Rosie", "Colin", "Maya", "Finn",
]
LABEL_RE = re.compile(
    r"(" + "|".join(re.escape(label) for label in sorted(LABELS, key=len, reverse=True)) + r"):\s*"
)
FALLBACK = {
    ("1", "2"): "Heather McCallum", ("1", "4"): "Lecturer",
    ("2", "2"): "Steve Wayne Wright (Elmley Town Council)", ("2", "4"): "Lecturer",
    ("3", "2"): "Archaeologist (Hayden)", ("3", "4"): "Lecturer",
    ("4", "2"): "Speaker (Guide)", ("4", "4"): "Lecturer",
}
CORRECTIONS = {
    "popular ations": "populations",
    "Temps": "Thames",
    "smallcale": "small-scale",
    "ChBE": "Chembe",
    "Adelman": "Edelman",
    "Macllum": "McCallum",
    "Greenhill Abbottz": "Greenhill Abbots",
    "Duehurst": "Dunhurst",
    "in in": "in",
    "and and": "and",
    "the the": "the",
    "of of": "of",
    "to to": "to",
    "kils": "kilns",
    "Marketeers": "Marketers",
    "fastmoving": "fast-moving",
    "high voltage": "high-voltage",
    "longerterm": "longer-term",
    "small-scale farmers": "small-scale farmers",
    "on, on.": "on.",
    "object. object": "object",
    "odd name. themes": "odd names",
    "month. month": "month",
    "As a thank Thank you": "As a thank you",
    "Orley": "Audley",
    "£30 ahead": "£30 a head",
    "smoking 15 cigarettes a day. or similar": "smoking 15 cigarettes a day, or similar",
    "river temps": "river Thames",
    "Ruie Blass": "Ruy Blas",
    "Of Lancha": "Man of La Mancha",
    "Jane Shaw": "Jane Shore",
    "the tragedy of Jane Shore": "The Tragedy of Jane Shore",
}
HEADER = re.compile(r"(Cambridge University Press|978-1-009|ielts-thudang|© in this web|^CAMBRIDGE$)")
FOOTER = re.compile(r"^\s*\d{1,3}\s*$")


def pages_lines():
    for page in SCRIPT_PAGES:
        for raw in (RAW / f"page-{page:03d}.txt").read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or HEADER.search(line) or FOOTER.match(line):
                continue
            line = re.sub(r"[ \t]+", " ", line)
            # A part heading can be appended to the previous line by pdftotext.
            m = re.search(r"(?:^|\s)(Part [1-4])$", line)
            if m and line != m.group(1):
                yield line[:m.start(1)].strip()
                yield m.group(1)
            else:
                yield line


def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    for wrong, right in CORRECTIONS.items():
        text = text.replace(wrong, right)
    text = re.sub(r"\b(\w+) \1\b", r"\1", text)
    text = re.sub(r"\bkil\b", "kiln", text)
    text = re.sub(r"\bThank\.$", "Thank you.", text)
    return text


def parse_transcripts() -> dict:
    tests: dict[str, dict[str, list[dict]]] = {}
    test = part = None
    current: list[dict] = []
    for line in pages_lines():
        m = re.fullmatch(r"Test ([1-4])", line)
        if m:
            test, part = m.group(1), None
            tests.setdefault(test, {})
            continue
        if line in ("Audio scripts", "Audio Scripts"):
            continue
        m = re.fullmatch(r"Part ([1-4])", line)
        if m:
            part = m.group(1)
            current = []
            tests[test][part] = current
            continue
        if test is None or part is None:
            continue
        # Split any line containing one or more speaker labels.
        pos = 0
        matches = list(LABEL_RE.finditer(line))
        if matches:
            before = line[:matches[0].start()].strip()
            if before:
                if current:
                    current[-1]["text"] = clean_text(current[-1]["text"] + " " + before)
                else:
                    current.append({"speaker": "Narrator", "text": clean_text(before)})
            for i, match in enumerate(matches):
                end = matches[i + 1].start() if i + 1 < len(matches) else len(line)
                speaker = match.group(1)
                text = clean_text(line[match.end():end])
                if text:
                    current.append({"speaker": speaker, "text": text})
            continue
        if not current:
            narration = ("you will hear" in line or "you have some time" in line
                         or line.startswith("Now listen"))
            speaker = "Narrator" if narration else FALLBACK.get((test, part), "Narrator")
            current.append({"speaker": speaker, "text": clean_text(line)})
        else:
            current[-1]["text"] = clean_text(current[-1]["text"] + " " + line)
    # Repair two script openings truncated by the source book.
    repairs = {
        ("1", "3"): ("from our research into loneliness.",
                      "So, to return to our research into loneliness."),
        ("4", "4"): ("looking at different types of conflicts",
                      "In this lecture, I'm going to be looking at different types of conflicts"),
    }
    for (test_no, part_no), (old, new) in repairs.items():
        turns = tests.get(test_no, {}).get(part_no)
        if turns and turns[0]["text"].startswith(old):
            turns[0]["text"] = new + turns[0]["text"][len(old):]
    # Drop empty turns and collapse consecutive turns by the same speaker.
    for test_parts in tests.values():
        for part_no, turns in test_parts.items():
            merged = []
            for turn in turns:
                if not turn["text"]:
                    continue
                if merged and merged[-1]["speaker"] == turn["speaker"]:
                    merged[-1]["text"] = clean_text(merged[-1]["text"] + " " + turn["text"])
                else:
                    merged.append(turn)
            test_parts[part_no] = merged
    return tests


def main() -> None:
    out = ROOT / "meta"
    out.mkdir(exist_ok=True)
    transcripts = parse_transcripts()
    (out / "transcripts.json").write_text(json.dumps(transcripts, indent=2, ensure_ascii=False) + "\n")
    (out / "pages.json").write_text(json.dumps(PAGE_MAP, indent=2))
    for test in sorted(transcripts):
        for part in sorted(transcripts[test]):
            turns = transcripts[test][part]
            words = sum(len(t["text"].split()) for t in turns)
            speakers = sorted({t["speaker"] for t in turns})
            print(f"T{test} P{part}: {len(turns):2d} turns, {words:4d} words, {speakers}")
            print("   start:", turns[0]["text"][:90])
            print("   end:  ", turns[-1]["text"][-90:])


if __name__ == "__main__":
    main()
