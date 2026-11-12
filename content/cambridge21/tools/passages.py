#!/usr/bin/env python3
"""Build clean reading passages from per-page layout text."""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "raw"
PDF = "/Users/tim2k/Downloads/Cambridge Ielts 21.pdf"

META = {
    "1": {
        "1": {"pages": [17, 18], "title": "The Davies Sisters",
              "subtitle": "Between 1908 and 1924, Gwendoline and Margaret Davies amassed one of the largest collections of late-nineteenth and early-twentieth-century French paintings in Britain"},
        "2": {"pages": [21, 22], "title": "Why we need silence", "subtitle": "", "labeled": True},
        "3": {"pages": [26, 27], "title": "Book review: The World of Sugar by Ulbe Bosma", "subtitle": ""},
    },
    "2": {
        "1": {"pages": [39, 40], "title": "Do animals dream?", "subtitle": ""},
        "2": {"pages": [43, 44], "title": "Mapungubwe",
              "subtitle": "Located in southern Africa just below the Limpopo River, the kingdom of Mapungubwe flourished between the 11th and 13th century CE", "labeled": True},
        "3": {"pages": [47, 48], "title": "Artificial Intelligence", "subtitle": "", "two_column": True,
              "starts": [
                  "In many countries in the West, hysteria",
                  "While it is undeniable that AI has opened up",
                  "In only a few years, AI solutionism",
                  "One of the most promising varieties",
                  "AI systems need a lot of data",
                  "For these reasons, the sensationalism",
                  "One of the many difficulties in deploying",
                  "If we are to reap the benefits",
                  "The medical profession has also recognised",
                  "Similar difficulties arose in the legal domain",
                  "There are some crucial lessons here",
              ]},
    },
    "3": {
        "1": {"pages": [61, 62], "title": "Saving the saiga", "subtitle": ""},
        "2": {"pages": [65, 66], "title": "The problems of getting around the city of Dar es Salaam", "subtitle": ""},
        "3": {"pages": [69, 70], "title": "Rethinking the Past", "subtitle": ""},
    },
    "4": {
        "1": {"pages": [82, 83], "title": "The problems and benefits created by the spread of the water hyacinth in Kenya", "subtitle": ""},
        "2": {"pages": [86, 87], "title": "How could multilingualism benefit India's poorest schoolchildren?", "subtitle": ""},
        "3": {"pages": [90, 91], "title": "The Globemakers: The Curious Story of an Ancient Craft",
              "subtitle": "A review of Peter Bellerby's book The Globemakers", "drop_first": 1},
    },
}

DROP_LINE = re.compile(r"^(Reading|READING|Test\s*\d+|Test\s*\d+.*)$")
FOOTER = re.compile(r"^(➔|.*[➔].*|.*\bp\.\s*\d+.*|\d{1,3})$")
LABEL = re.compile(r"^([A-I])\s{2,}(.*)$")


CORRECTIONS = {
    "UlbeBosma": "Ulbe Bosma",
    "Dares Salaam": "Dar es Salaam",
    "Sillicon": "Silicon",
    "Belferby": "Bellerby",
    "Cezanne": "Cézanne",
    "Franc;ois": "François",
    "Provenc;alLandscape": "Provençal Landscape",
    "lmow": "know",
    "well-lmown": "well-known",
    "contemporaiy": "contemporary",
    "everywhere.There": "everywhere. There",
    "weare": "we are",
    "willdestroy": "will destroy",
    "Similarly,adding": "Similarly, adding",
    "willbe": "will be",
    "havethe": "have the",
    "fewdigitised": "few digitised",
    "specificareas": "specific areas",
    "weneed": "we need",
    "advisedjudges": "advised judges",
    "Valleyin": "Valley in",
    "sugar- growing": "sugar-growing",
    "·while": "While",
}


def apply_corrections(text: str) -> str:
    for wrong, right in CORRECTIONS.items():
        text = text.replace(wrong, right)
    return text


def norm_title(text: str) -> str:
    return re.sub(r"\s+", "", text).lower()


def page_lines(n: int) -> list[str]:
    text = (RAW / f"page-{n:03d}.txt").read_text(encoding="utf-8")
    return [line.rstrip() for line in text.splitlines()]


def clean_line(line: str) -> str:
    line = line.replace("\u00ad", "")
    line = re.sub(r"[ \t]+", " ", line)
    return line.strip()


def extract_passage(info: dict) -> list[dict]:
    if info.get("two_column"):
        raw = subprocess.run(
            ["pdftotext", "-f", str(info["pages"][0]), "-l", str(info["pages"][-1]), "-raw", PDF, "-"],
            capture_output=True, text=True, check=True,
        ).stdout
        lines = raw.splitlines()
    else:
        lines = []
        for page in info["pages"]:
            lines.extend(page_lines(page))

    cleaned: list[str] = []
    body_started = False
    for line in lines:
        s = clean_line(line)
        if not body_started:
            if "Passage" in s and "below" in s:
                body_started = True
            continue
        if s and (DROP_LINE.match(s) or FOOTER.match(s)):
            continue
        cleaned.append(s)

    text = "\n".join(cleaned)
    text = re.sub(r"\n{2,}", "\n\n", text)
    for target in (info["title"], info["subtitle"]):
        if not target:
            continue
        pattern = re.compile(r"\s*".join(re.escape(part) for part in re.split(r"\s+", target)), re.I)
        text = pattern.sub("", text, count=1)
    text = re.sub(r"[ \t]+", " ", text).strip()

    text = apply_corrections(text)

    if info.get("starts"):
        text = text.replace("\n", " ")
        text = re.sub(r"\s+", " ", text)
        positions = []
        for start in info["starts"]:
            idx = text.find(start)
            if idx < 0:
                raise RuntimeError(f"paragraph start not found: {start!r}")
            positions.append(idx)
        paras = []
        for i, idx in enumerate(positions):
            end = positions[i + 1] if i + 1 < len(positions) else len(text)
            paras.append({"label": "", "text": text[idx:end].strip()})
        return paras

    blocks = re.split(r"\n\s*\n", text)
    paras: list[dict] = []
    labeled = bool(info.get("labeled"))
    for block in blocks:
        block = " ".join(part.strip() for part in block.splitlines() if part.strip())
        if not block:
            continue
        m = re.match(r"^([A-I])\s+(?=[A-Z])", block) if labeled else None
        if m:
            paras.append({"label": m.group(1), "text": block[m.end():].strip()})
        else:
            paras.append({"label": "", "text": block})
    # Drop glossary footnotes and stray subtitle fragments.
    drop = []
    for p in paras:
        t = p["text"].lstrip()
        if t.startswith("*") or t.startswith("•"):
            drop.append(p)
            continue
        if info["subtitle"] and norm_title(t)[:30] == norm_title(info["subtitle"])[:30] and not p["label"]:
            drop.append(p)
    paras = [p for p in paras if p not in drop]
    if info.get("drop_first"):
        paras = paras[1:]
    if labeled:
        # Merge continuation paragraphs into their section so A-G map one-to-one.
        merged: list[dict] = []
        for p in paras:
            if not p["label"] and merged:
                merged[-1]["text"] += " " + p["text"]
            elif p["label"]:
                merged.append(dict(p))
        paras = merged
    else:
        # Join lines split by a footnote or column break.
        merged = []
        for p in paras:
            if merged and p["text"][:1].islower():
                merged[-1]["text"] += " " + p["text"]
            else:
                merged.append(dict(p))
        paras = merged
    return paras


def split_paragraphs(text: str) -> list[str]:
    # pdftotext -layout keeps page columns and paragraphs; blank lines are lost in
    # the joined body, so split on paragraph-sized gaps encoded by double spaces
    # is not possible. Use sentence-boundary heuristics on known section breaks.
    if "\n\n" in text:
        return [p.strip() for p in text.split("\n\n") if p.strip()]
    return [text.strip()]


def main() -> None:
    out = {}
    for test, passages in META.items():
        out[test] = {}
        for number, info in passages.items():
            out[test][number] = {
                "title": info["title"],
                "subtitle": info["subtitle"],
                "paragraphs": extract_passage(info),
            }
    (ROOT / "meta" / "passages.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    for test in out:
        for number, data in out[test].items():
            words = sum(len(p["text"].split()) for p in data["paragraphs"])
            print(f"T{test}P{number}: {len(data['paragraphs'])} paragraphs, {words} words: {data['paragraphs'][0]['text'][:90]!r}")


if __name__ == "__main__":
    main()
