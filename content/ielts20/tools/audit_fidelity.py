#!/usr/bin/env python3
"""Audit the authored IELTS 20 content against the extracted book pages."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "raw"
PACK = ROOT.parent.parent
ACADEMIC = PACK / "content" / "academic"

PAGES = {
    "1": {"listening": (3, 9), "reading": (11, 26), "writing": (28, 29), "speaking": (33, 33)},
    "2": {"listening": (39, 45), "reading": (47, 62), "writing": (64, 66), "speaking": (71, 71)},
    "3": {"listening": (77, 84), "reading": (86, 101), "writing": (103, 104), "speaking": (108, 108)},
    "4": {"listening": (114, 120), "reading": (122, 136), "writing": (138, 139), "speaking": (143, 143)},
}


def norm(text: str) -> str:
    text = text.lower()
    text = text.replace("’", "'").replace("‘", "'").replace("–", "-").replace("—", "-")
    text = re.sub(r"[^a-z0-9£%]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def page_text(test: str, section: str) -> str:
    start, end = PAGES[test][section]
    out = [(RAW / f"page-{page:03d}.txt").read_text(encoding="utf-8")
           for page in range(start, end + 1)]
    return norm(" ".join(out))


def overlap(needle: str, haystack: str) -> float:
    words = [w for w in norm(needle).split() if len(w) > 2]
    if not words:
        return 1.0
    hits = sum(1 for w in words if w in haystack)
    return hits / len(words)


def audit_test(number: str) -> list[dict]:
    exam = json.loads((ACADEMIC / f"ielts20-test{number}.json").read_text())
    book = {s: page_text(number, s) for s in ("listening", "reading", "writing", "speaking")}
    findings: list[dict] = []

    for part in exam["listening"]:
        for q in part["questions"]:
            score = overlap(q["prompt"], book["listening"])
            if score < 0.7 and q["type"] not in ("short", "map"):
                findings.append({"kind": "listening prompt", "id": q["id"],
                                 "score": round(score, 2), "text": q["prompt"]})
            for option in q.get("options", []):
                s = overlap(option, book["listening"])
                if s < 0.8:
                    findings.append({"kind": "listening option", "id": q["id"],
                                     "score": round(s, 2), "text": option})

    for passage in exam["reading"]:
        for q in passage["questions"]:
            score = overlap(q["prompt"], book["reading"])
            if score < 0.8 and q["type"] not in ("short", "select", "heading"):
                findings.append({"kind": "reading prompt", "id": q["id"],
                                 "score": round(score, 2), "text": q["prompt"]})
            for option in q.get("options", []):
                s = overlap(option, book["reading"])
                if s < 0.8:
                    findings.append({"kind": "reading option", "id": q["id"],
                                     "score": round(s, 2), "text": option})
        for paragraph in passage["paragraphs"]:
            score = overlap(paragraph["text"], book["reading"])
            if score < 0.97:
                findings.append({"kind": "passage text", "id": f"r{passage['number']}-{paragraph['label'] or '?'}",
                                 "score": round(score, 3), "text": paragraph["text"][:70]})

    for task in exam["writing"]:
        score = overlap(task["prompt"], book["writing"])
        if score < 0.8:
            findings.append({"kind": "writing prompt", "id": task["id"],
                             "score": round(score, 2), "text": task["prompt"][:100]})

    for part in exam["speaking"]:
        for q in part["questions"]:
            score = overlap(q["text"], book["speaking"])
            if score < 0.8:
                findings.append({"kind": "speaking question", "id": q["id"],
                                 "score": round(score, 2), "text": q["text"]})
        if part.get("cueCard"):
            score = overlap(part["cueCard"]["topic"], book["speaking"])
            if score < 0.8:
                findings.append({"kind": "cue card", "id": part["id"],
                                 "score": round(score, 2), "text": part["cueCard"]["topic"]})

    return findings


def main() -> None:
    total = 0
    for number in ("1", "2", "3", "4"):
        findings = audit_test(number)
        total += len(findings)
        print(f"== Test {number}: {len(findings)} findings")
        for f in findings:
            print(f"  [{f['kind']}] {f['id']} overlap={f['score']}  {f['text'][:90]}")
    print(f"\nTOTAL: {total} findings")


if __name__ == "__main__":
    main()
