#!/usr/bin/env python3
"""Rebuild clean IELTS 19 reading passages from OCR line text."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OCR = ROOT / "ocr-tess3"

HEAD = re.compile(
    r"^(Cambridge University Press|978-1-009|with Resource Bank|Excerpt|More Information|Frontmatter|"
    r"Reading$|READING$|Test\s*\d+|TELEGRAM|Telegra|Telegram|@IELTS|© in this web|\d{1,3}$)"
)
FOOTNOTE = re.compile(r"^[\"“']?\s*(caravel|\*)\s*[:\-]|^\*\s")

META = {
    "1": {
        "1": {
            "pages": [16, 17],
            "title": "How tennis rackets have changed",
            "subtitle": "",
            "starts": [
                "In 2016, the British professional",
                "Of the changes that account",
                "The modification that Murray made",
                "The primary reason for these modifications",
                "Racket modifications mainly date",
                "Modifications can be divided",
                "At one time, all tennis rackets",
                "Of the synthetics, co-polyester",
                "However, many players go beyond",
                "Other changes to the frame",
                "Racket customisation and modification",
            ],
        },
        "2": {
            "pages": [21, 22],
            "title": "The pirates of the ancient Mediterranean",
            "subtitle": "In the first and second millennia BCE, pirates sailed around the Mediterranean, attacking ships and avoiding pursuers",
            "labels": list("ABCDEFG"),
            "starts": [
                "When one mentions pirates",
                "Although piracy in the Mediterranean",
                "One should also add",
                "The first known record",
                "The ancient Greek world's experience",
                "The rising power of ancient Rome",
                "By now, Rome was well aware",
            ],
        },
        "3": {
            "pages": [26, 27],
            "title": "The persistence and peril of misinformation",
            "subtitle": "Brian Southwell looks at how human brains verify information and discusses some of the challenges of battling widespread falsehoods",
            "starts": [
                "Misinformation - both deliberately",
                "However, we currently live",
                "The main worry regarding misinformation",
                "At least three observations",
                "Knowing what happens when people",
                "What about our second observation",
                "This leads us to our third observation",
                "We live at a time when widespread",
            ],
        },
    },
    "2": {
        "1": {
            "pages": [41, 42],
            "title": "The Industrial Revolution in Britain",
            "subtitle": "",
            "starts": [
                "The Industrial Revolution began",
                "The foundations of the Industrial Revolution",
                "The demand for coal",
                "Britain had produced textiles",
                "The British iron industry",
                "The latter part of the Industrial Revolution",
                "The impact of the Industrial Revolution",
                "Although industrialisation increased",
                "The first major instances of machine breaking",
            ],
        },
        "2": {
            "pages": [45, 46],
            "title": "Athletes and stress",
            "subtitle": "",
            "labels": list("ABCDEF"),
            "starts": [
                "It isn't easy being a professional athlete",
                "For athletes, some level of performance stress",
                "Each new demand or change",
                "Our challenge and threat responses",
                "That said, anxiety",
                "But there are many ways athletes",
            ],
        },
        "3": {
            "pages": [49, 50],
            "title": "An inquiry into the existence of the gifted child",
            "subtitle": "",
            "starts": [
                "Let us start by looking at a modern",
                "In adult life it is clear",
                "Is her background unusual?",
                "There has been a considerable amount",
                "While the jury is out on giftedness",
                "According to my colleague Prof Deborah",
                "Prof Anders Ericsson",
                "But it is perhaps the work of Benjamin Bloom",
                "Let us end with Einstein",
            ],
        },
    },
    "3": {
        "1": {
            "pages": [63, 64],
            "title": "Archaeologists discover evidence of prehistoric island settlers",
            "subtitle": "",
            "starts": [
                "In early April 2019",
                "The excavations were part",
                "Just inland from the village",
                "The oldest cultural layers",
                "Roughly 11,700 years ago",
                "Judging by the bones",
                "Shipton's team's excavation",
                "The excavations suggest",
                "Whatever the reason",
            ],
        },
        "2": {
            "pages": [67, 68],
            "title": "The global importance of wetlands",
            "subtitle": "",
            "labels": list("ABCDEFGH"),
            "starts": [
                "Wetlands are areas",
                "Throughout history",
                "They also serve",
                "The world's wetlands are",
                "The damage starts",
                "And while these industries",
                "Silvius also acknowledges",
                "The fortunes of wetlands",
            ],
        },
        "3": {
            "pages": [71, 72],
            "title": "Is the era of artificial speech translation upon us?",
            "subtitle": "Once the stuff of science fiction, technology that enables people to talk using different languages is now here. But how effective is it?",
            "starts": [
                "Noise, Alex Waibel tells me",
                "At Karlsruhe Institute",
                "The idea of artificial speech translation",
                "At this stage, however",
                "For a conversation, both speakers",
                "Waibel highlights the significance",
                "Systems not only need",
                "Professors and other professionals",
                "Whatever uses it is put to",
            ],
        },
    },
    "4": {
        "1": {
            "pages": [85, 86],
            "title": "The impact of climate change on butterflies in Britain",
            "subtitle": "",
            "starts": [
                "According to conservationists",
                "Butterflies prefer outdoor conditions",
                "These advances have been observed",
                "First, the researchers pulled together data",
                "Analysing the trends",
                "Other species, however",
                "Allis not lost, however",
                "More immediately",
            ],
        },
        "2": {
            "pages": [89, 90],
            "title": "Deep-sea mining",
            "subtitle": "Bacteria from the ocean floor can beat superbugs and cancer. But habitats are at risk from the hunger for marine minerals",
            "labels": list("ABCDEF"),
            "starts": [
                "When Professor Mat Upton",
                "'We're looking at the bioactive potential",
                "The deep sea contains more nickel",
                "But environmental and legal groups",
                "Scientific research",
                "The oceans occupy around 70%",
            ],
        },
        "3": {
            "pages": [93, 94],
            "title": "The Unselfish Gene",
            "subtitle": "A psychologist gives his view on how humans became self-centred",
            "starts": [
                "There has long been a general assumption",
                "This bleak view of human nature",
                "Prehistory is usually seen",
                "It's important to remember",
                "There is significant evidence",
                "The !Kung people of southern Africa",
                "Many anthropologists believe",
                "It makes more sense, then",
                "But if prehistoric life wasn't",
                "So, it could well be",
            ],
        },
    },
}

CORRECTIONS = {
    "Gongalo": "Gonçalo",
    "the /liad": "the Iliad",
    "a. . . thorough": "a thorough",
    "wellknown": "well-known",
    "respondsto": "responds to",
    "Secrets fiom": "Secrets from",
    "/Kung": "!Kung",
    "the !Kung": "the !Kung",
    'language. "1': "language.",
    "coLemMAN": "Coleman",
    "coteman": "Coleman",
    "Te st 1": "Test 1",
}


def clean(line: str) -> str:
    line = line.replace("\u00ad", "").replace("\u2019", "'").replace("\u2018", "'")
    line = line.replace("\u201c", '"').replace("\u201d", '"').replace("\u2014", " - ")
    line = re.sub(r"[ \t]+", " ", line).strip()
    line = re.sub(r"\s*\.\s*(?:\.\s*){2,}", "... ", line).strip()
    for wrong, right in CORRECTIONS.items():
        line = line.replace(wrong, right)
    return line


def page_lines(pages: list[int]) -> list[str]:
    out: list[str] = []
    for p in pages:
        for raw in (OCR / f"ocr-{p:03d}.txt").read_text(encoding="utf-8", errors="ignore").splitlines():
            line = clean(raw)
            if not line or HEAD.match(line):
                continue
            out.append(line)
    return out


def build(number: str, info: dict) -> dict:
    starts = info["starts"]
    labels = info.get("labels", [])
    paragraphs: list[dict] = []
    current: dict | None = None
    started = False
    for line in page_lines(info["pages"]):
        probe = line
        label = ""
        m = re.match(r"^([A-H])[\s_]+(.*)$", probe)
        if labels and m:
            label, probe = m.group(1), m.group(2)
        matched = None
        for i, start in enumerate(starts):
            if probe.lower().startswith(start.lower()):
                matched = i
                break
        if matched is not None:
            started = True
            current = {"label": label or (labels[matched] if labels and matched < len(labels) else ""), "text": probe}
            paragraphs.append(current)
            continue
        if not started or current is None:
            continue
        if re.match(r"^(Questions?\s+\d|Write your answers|Choose |Complete the|Do the following|Look at the following|Reading Passage \d)", line):
            break
        if FOOTNOTE.match(line) or line.startswith("*"):
            continue
        if line.endswith("-"):
            current["text"] = current["text"].rstrip() + line
        else:
            current["text"] = (current["text"] + " " + line).strip()
    for p in paragraphs:
        p["text"] = re.sub(r"\s+", " ", p["text"]).strip()
        p["text"] = re.sub(r"\s*\.\s*(?:\.\s*){2,}", "... ", p["text"]).strip()
        if not labels:
            p.pop("label", None)
    return {
        "title": info["title"],
        "subtitle": info.get("subtitle", ""),
        "paragraphs": paragraphs,
    }


def main() -> None:
    out = {}
    for test, passages in META.items():
        out[test] = {}
        for number, info in passages.items():
            data = build(number, info)
            out[test][number] = data
            words = sum(len(p["text"].split()) for p in data["paragraphs"])
            labels = "".join(p.get("label", "?") for p in data["paragraphs"])
            print(f"test {test} passage {number}: {len(data['paragraphs'])} paragraphs [{labels}], {words} words")
    path = ROOT / "meta" / "passages.json"
    path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
