"""Shared helpers for building exam content from extracted IELTS 19 material."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
META = ROOT / "meta"


def load(name: str):
    return json.loads((META / name).read_text())


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def group(gid, label, instructions, nums, layout="", shared=None, body=None, figure=None, figureAlt=None, note=None):
    data = {
        "id": gid,
        "label": label,
        "instructions": instructions,
        "range": [nums[0], nums[-1]],
        "layout": layout,
    }
    if shared:
        data["sharedOptions"] = shared
    if body:
        data["body"] = body
    if figure:
        data["figure"] = figure
    if figureAlt:
        data["figureAlt"] = figureAlt
    if note:
        data["note"] = note
    return data


def question(num, gid, prompt, qtype="short", options=None):
    data = {"number": num, "groupId": gid, "type": qtype, "prompt": prompt}
    if options:
        data["options"] = options
    return data


def apply_keys(questions, key_map, prefix):
    """Attach answer keys to authored questions using their numbers."""
    by_number = {q["number"]: q for q in questions}
    for number, values in key_map.items():
        q = by_number.get(int(number))
        if q is None:
            continue
        q["answer"] = values[0]
        if len(values) > 1:
            q["accepted"] = values[1:]
    missing = [n for n in by_number if "answer" not in by_number[n]]
    if missing:
        raise KeyError(f"{prefix}: questions without keys: {missing}")
    for q in questions:
        q.setdefault("id", f"{prefix}-q{q['number']}")
    return questions


def passage(number, data):
    return {
        "id": f"r{number}",
        "number": number,
        "title": data["title"],
        "subtitle": data["subtitle"],
        "paragraphs": data["paragraphs"],
        "groups": [],
        "questions": [],
    }
