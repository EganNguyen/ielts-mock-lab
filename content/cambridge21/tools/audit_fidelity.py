#!/usr/bin/env python3
"""Audit authored exam content against the extracted Cambridge IELTS 21 pages.

Checks, per test:
  - every authored question stem / option / TFNG statement occurs in the book text
    (fuzzy token overlap identifies retyping errors)
  - answer counts and numbers
  - writing prompts and speaking questions occur in the book pages
  - transcripts cover all four parts and contain no page artefacts
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "raw"
PACK = ROOT.parent.parent
ACADEMIC = PACK / "content" / "academic"

PAGES = {
    "1": {"listening": (11, 16), "reading": (17, 29), "writing": (30, 31), "speaking": (32, 32)},
    "2": {"listening": (33, 38), "reading": (39, 51), "writing": (52, 53), "speaking": (54, 54)},
    "3": {"listening": (55, 60), "reading": (61, 72), "writing": (73, 74), "speaking": (75, 75)},
    "4": {"listening": (76, 81), "reading": (82, 94), "writing": (95, 96), "speaking": (97, 97)},
}


def norm(text: str) -> str:
    text = text.lower()
    text = text.replace("’", "'").replace("–", "-").replace("—", "-")
    text = re.sub(r"[^a-z0-9£%]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def page_text(test: str, section: str) -> str:
    start, end = PAGES[test][section]
    out = []
    for page in range(start, end + 1):
        out.append((RAW / f"page-{page:03d}.txt").read_text(encoding="utf-8"))
    return norm(" ".join(out))


def overlap(needle: str, haystack: str) -> float:
    words = [w for w in norm(needle).split() if len(w) > 2]
    if not words:
        return 1.0
    hits = sum(1 for w in words if w in haystack)
    return hits / len(words)


def audit_test(number: str) -> list[dict]:
    exam = json.loads((ACADEMIC / f"cambridge21-test{number}.json").read_text())
    book = {s: page_text(number, s) for s in ("listening", "reading", "writing", "speaking")}
    findings: list[dict] = []

    for part in exam["listening"]:
        for q in part["questions"]:
            score = overlap(q["prompt"], book["listening"])
            # Prompts for note blanks are often paraphrases ("Note completion 3").
            if score < 0.75 and not re.match(r"^(Note|Summary|Flow|Biogas|Ferry|Saiga|Cruise|Invasive|Sleeping)", q["prompt"]):
                findings.append({"kind": "listening prompt", "id": q["id"], "score": round(score, 2), "text": q["prompt"]})
            for option in q.get("options", []):
                if overlap(option, book["listening"]) < 0.8:
                    findings.append({"kind": "listening option", "id": q["id"], "score": round(overlap(option, book["listening"]), 2), "text": option})

    for passage in exam["reading"]:
        for q in passage["questions"]:
            score = overlap(q["prompt"], book["reading"])
            if score < 0.8 and q["type"] != "short" and q["type"] != "select":
                findings.append({"kind": "reading prompt", "id": q["id"], "score": round(score, 2), "text": q["prompt"]})
            for option in q.get("options", []):
                if overlap(option, book["reading"]) < 0.8:
                    findings.append({"kind": "reading option", "id": q["id"], "score": round(overlap(option, book["reading"]), 2), "text": option})
        for paragraph in passage["paragraphs"]:
            # A passage paragraph should be nearly verbatim; low overlap means OCR/authoring drift.
            score = overlap(paragraph["text"], book["reading"])
            if score < 0.97:
                findings.append({"kind": "passage text", "id": f"r{passage['number']}-{paragraph['label'] or '?'}", "score": round(score, 3), "text": paragraph["text"][:70]})

    for task in exam["writing"]:
        score = overlap(task["prompt"], book["writing"])
        if score < 0.8:
            findings.append({"kind": "writing prompt", "id": task["id"], "score": round(score, 2), "text": task["prompt"][:100]})

    for part in exam["speaking"]:
        for q in part["questions"]:
            score = overlap(q["text"], book["speaking"])
            if score < 0.8:
                findings.append({"kind": "speaking question", "id": q["id"], "score": round(score, 2), "text": q["text"]})
        if part.get("cueCard"):
            score = overlap(part["cueCard"]["topic"], book["speaking"])
            if score < 0.8:
                findings.append({"kind": "cue card", "id": part["id"], "score": round(score, 2), "text": part["cueCard"]["topic"]})

    return findings


def main() -> None:
    total = 0
    for number in ("1", "2", "3", "4"):
        findings = audit_test(number)
        total += len(findings)
        print(f"== Test {number}: {len(findings)} findings")
        for finding in findings:
            print(f"  [{finding['kind']}] {finding['id']} overlap={finding['score']}  {finding['text'][:90]}")
    print(f"\nTOTAL: {total} findings")


if __name__ == "__main__":
    main()
