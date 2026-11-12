#!/usr/bin/env python3
"""Build clean reading passages for IELTS 20 from the per-page layout text."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "raw"

META = {
 "1": {
  "1": {
   "pages": [11, 12, 13],
   "title": "The kākāpō",
   "subtitle": "The kākāpō is a nocturnal, flightless parrot that is critically endangered and one of New Zealand's unique treasures",
   "first": "The kākāpō, also known as the owl parrot",
   "starts": [
    "The kākāpō, also known as the owl parrot",
    "Kakap6 breed in summer and autumn",
    "Before humans arrived",
    "In 1894, the New Zealand government",
    "From 1949 to 1973",
    "Unfortunately, predation by feral cats",
    "In 1996, a new Recovery Plan",
    "Today, kākāpō management continues",
   ],
  },
  "2": {
   "pages": [16, 17, 18],
   "title": "The return of the elm to Britain",
   "subtitle": "Mark Rowe investigates attempts to reintroduce elms to Britain",
   "first": "Around 25 million elms",
   "labels": list("ABCDEFG"),
   "starts": [
    "Around 25 million elms",
    "The disease is caused by a fungus",
    "Today, elms still exist",
    "For centuries, elm ran a close second",
    "Given how ingrained elm",
    "Any prospect of the elm returning",
    "All of this raises questions",
   ],
  },
  "3": {
   "pages": [21, 22, 23],
   "title": "How stress affects our judgement",
   "subtitle": "",
   "first": "Some of the most important decisions",
   "starts": [
    "Some of the most important decisions",
    "My colleague and I",
    "We found that perceived threat",
    "Back in our lab",
    "When we experience stressful events",
    "Such neural engineering",
    "It is also important to realise",
    "In some ways, many of us now live",
    "The fact that stress increases",
    "The good news, however",
   ],
  },
 },
 "2": {
  "1": {
   "pages": [47, 48, 49],
   "title": "Manatees",
   "subtitle": "",
   "first": "Manatees, also known as sea cows",
   "starts": [
    "Manatees, also known as sea cows",
    "Unlike most mammals",
    "Seagrasses and other marine plants",
    "Manatees' teeth are all molars",
    "Manatees are fully aquatic",
    "The West Indian manatee reaches",
    "The African manatee is also",
    "The Amazonian manatee is the smallest",
    "All three manatee species",
    "The two subspecies of West Indian",
   ],
  },
  "2": {
   "pages": [52, 53, 54],
   "title": "Procrastination",
   "subtitle": "A psychologist explains why we put off important tasks and how we can break this habit",
   "first": "Procrastination is the habit",
   "stop": "Questions 14-16",
   "labels": list("ABCDEF"),
   "starts": [
    "Procrastination is the habit",
    "Contrary to popular belief",
    "Tasks that are emotionally loaded",
    "So why is this such a problem",
    "Procrastination also correlates",
    "Finding better ways of managing",
   ],
  },
  "3": {
   "pages": [57, 58, 59],
   "title": "Invasion of the Robot Umpires",
   "subtitle": "",
   "first": "A few years ago, Fred DeJesus",
   "starts": [
    "A few years ago, Fred DeJesus",
    "Major League Baseball",
    "For a hundred and fifty years",
    "During the first robo-umpire season",
    "A human, at least, yells back",
    "The executive tasked",
    "Sword's team brainstormed",
    "In the past twenty years",
    "I decided to email Alva Noe",
   ],
  },
 },
 "3": {
  "1": {
   "pages": [86, 87, 88],
   "title": "Frozen Food",
   "subtitle": "A US perspective on the development of the frozen food industry",
   "first": "At some point in history",
   "starts": [
    "At some point in history",
    "Natural ice remained",
    "Finally, in 1870",
    "Initially, this process",
    "The modern frozen food industry",
    "Birdseye returned to the USA",
    "Birdseye was responsible",
    "But there were still obstacles",
    "Sales increased in the early 1940s",
    "1950s families were also looking",
    "Today, the US frozen food industry",
   ],
  },
  "2": {
   "pages": [91, 92, 93],
   "title": "Can the planet's coral reefs be saved?",
   "subtitle": "",
   "first": "Conservationists have put the final touches",
   "stop": "Reading Passage 2 has six sections",
   "labels": list("ABCDEF"),
   "starts": [
    "Conservationists have put the final touches",
    "Corals are composed of tiny animals",
    "As a result, coral reefs are often described",
    "Unfortunately, these majestic sights",
    "However, scientists are trying to pinpoint",
    "Research in these fields",
   ],
  },
  "3": {
   "pages": [96, 97, 98, 99],
   "title": "Robots and us",
   "subtitle": "Three leaders in their fields answer questions about our relationships with robots",
   "first": "When asked 'Should robots be used",
   "stop": "Look at the following statements",
   "starts": [
    "When asked 'Should robots be used",
    "On the question of using robots",
    "Meanwhile, for anthropology",
    "In response to the second question",
    "Wolpert's response to the question",
    "Richardson believes that our fear",
    "This led on to the third question",
    "Wolpert's response was to say",
    "Richardson's response to this question",
    "In answer to the fourth question",
    "As his response, Wolpert commented",
    "Finally, on the question of science fiction",
   ],
  },
 },
 "4": {
  "1": {
   "pages": [122, 123, 124],
   "title": "Georgia O'Keeffe",
   "subtitle": "",
   "first": "For seven decades, Georgia O'Keeffe",
   "stop": "Questions 1-7",
   "starts": [
    "For seven decades, Georgia O'Keeffe",
    "Born in 1887",
    "During this period",
    "Stieglitz was impressed",
    "With Stieglitz's encouragement",
    "By the mid-1920s",
    "In 1929, O'Keeffe made",
    "There, O'Keeffe found new inspiration",
    "However, it was the region's spectacular",
    "O'Keeffe eventually owned two homes",
    "From the 1950s into the 1970s",
    "The last two decades",
   ],
  },
  "2": {
   "pages": [126, 127, 128],
   "title": "Adapting to the effects of climate change",
   "subtitle": "",
   "first": "All around the world, nations",
   "labels": list("ABCDEF"),
   "starts": [
    "All around the world, nations",
    "In Miami Beach, Florida",
    "Seawalls are a staple strategy",
    "As the floodwaters rose",
    "Bangladesh is especially vulnerable",
    "Greg Spotts from Los Angeles",
   ],
  },
  "3": {
   "pages": [131, 132, 133],
   "title": "A new role for livestock guard dogs",
   "subtitle": "Livestock guard dogs, traditionally used to protect farm animals from predators, are now being used to protect the predators themselves",
   "first": "For thousands of years, livestock guard dogs",
   "labels": list("ABCDEFG"),
   "starts": [
    "For thousands of years, livestock guard dogs",
    "Today there are around 50 breeds",
    "The evidence indicates that guard dogs",
    "But today's guard dogs also have a new role",
    "Looking at all the published evidence",
    "Another concern is whether there may be",
    "The evidence so far, however",
   ],
  },
 },
}

CORRECTIONS = {
    "Kakap6": "Kākāpō", "kakap6": "kākāpō",
    "robe-umpire": "robo-umpire", "robe-umpires": "robo-umpires",
    "to colonies other planets": "to colonise other planets",
    "powerplants": "power plants",
    "140,000. ": "140,000 ",
    "8'desof": "sides of",
    "wasd1:1elared": "was declared",
    "arriver": "a river",
    "a a": "a",
    "the the": "the",
    "in in": "in",
    "of of": "of",
    "sealong": "sea along",
    "Amazon Basin Brazil": "Amazon Basin in Brazil",
    "value-if": "value - if",
    'with it." "': 'with it."',
}

BAD_LINE = re.compile(
    r"^(Reading|READING|Test\s*\d+|Test\s*\d+\s*$|\d{1,3}|[A-G]|[A-G]\s+\d{1,3})\s*$"
)
HEADER = re.compile(r"(Cambridge University Press|978-1-009|ielts-thudang|© in this web|^CAMBRIDGE$)")
FOOTNOTE = re.compile(r"^\s*\*{1,2}\s")


def clean_line(line: str) -> str:
    line = line.replace("\u00ad", "")
    line = line.replace("’", "'").replace("‘", "'")
    line = line.replace("“", '"').replace("”", '"')
    line = re.sub(r"[ \t]+", " ", line)
    return line.strip()


def extract(info: dict) -> list[dict]:
    lines: list[str] = []
    for page in info["pages"]:
        for raw in (RAW / f"page-{page:03d}.txt").read_text(encoding="utf-8").splitlines():
            line = clean_line(raw)
            if not line or HEADER.search(line) or BAD_LINE.match(line):
                continue
            if info.get("stop") and info["stop"].lower() in line.lower():
                break
            lines.append(line)
        else:
            continue
        break

    joined = " ".join(lines)
    joined = re.sub(r"\s+", " ", joined)
    for marker in ("* horticultural analogue", "* strike:", "* terraforming:", "** singularity:"):
        cut = joined.find(marker)
        if cut > 0:
            joined = joined[:cut].rstrip()

    # Drop everything before the first paragraph.
    idx = joined.lower().find(info["first"].lower())
    if idx < 0:
        raise RuntimeError(f"{info['title']}: first paragraph not found: {info['first']!r}")
    joined = joined[idx:]

    positions = []
    for start in info["starts"]:
        idx = joined.lower().find(start.lower(), positions[-1] + 1 if positions else 0)
        if idx < 0:
            raise RuntimeError(f"{info['title']}: paragraph start not found: {start!r}")
        positions.append(idx)

    labels = info.get("labels") or [""] * len(positions)
    paras = []
    for i, idx in enumerate(positions):
        end = positions[i + 1] if i + 1 < len(positions) else len(joined)
        text = joined[idx:end].strip()
        if i + 1 < len(labels) and labels[i + 1]:
            text = re.sub(r"\s+" + re.escape(labels[i + 1]) + r"$", "", text).strip()
        for wrong, right in CORRECTIONS.items():
            text = text.replace(wrong, right)
        text = re.sub(r"\s+([.,;:])", r"\1", text)
        paras.append({"label": labels[i], "text": text})
    return paras


def main() -> None:
    out = {}
    for test, passages in META.items():
        out[test] = {}
        for number, info in passages.items():
            paras = extract(info)
            out[test][number] = {
                "title": info["title"],
                "subtitle": info["subtitle"],
                "paragraphs": paras,
            }
    (ROOT / "meta" / "passages.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    for test in out:
        for number, data in out[test].items():
            words = sum(len(p["text"].split()) for p in data["paragraphs"])
            labels = "".join(p["label"] for p in data["paragraphs"] if p["label"])
            print(f"T{test}P{number}: {len(data['paragraphs']):2d} paras, {words:4d} words, "
                  f"labels={labels or '-'}: {data['paragraphs'][0]['text'][:70]!r}")


if __name__ == "__main__":
    main()
