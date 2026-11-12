#!/usr/bin/env python3
"""Compile Cambridge IELTS 21 extracted material into the Apex exam content schema."""
from __future__ import annotations

import importlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from common import load  # noqa: E402

OUT = ROOT.parent.parent / "content" / "academic"
PACK = ROOT

# Corrections where the raw two-column answer-key extraction interleaved columns.
KEY_FIXUPS = {
    ("2", "listening"): {"8": ["67.50"], "25": ["A", "C"], "26": ["A", "C"]},
}


def validate(exam: dict) -> None:
    assert len(exam["listening"]) == 4, "four listening parts"
    assert len(exam["reading"]) == 3, "three reading passages"
    assert len(exam["writing"]) == 2, "two writing tasks"
    assert len(exam["speaking"]) == 3, "three speaking parts"
    lq = [q for part in exam["listening"] for q in part["questions"]]
    rq = [q for p in exam["reading"] for q in p["questions"]]
    assert len(lq) == 40, f"listening questions: {len(lq)}"
    assert len(rq) == 40, f"reading questions: {len(rq)}"
    for q in lq + rq:
        assert q.get("answer"), f"missing answer key: {q['id']}"
        assert 1 <= q["number"] <= 40, q
    # Question numbers must be unique within each skill.
    assert sorted(q["number"] for q in lq) == list(range(1, 41))
    assert sorted(q["number"] for q in rq) == list(range(1, 41))
    # Every blank in a body must belong to a question in the same group.
    for part in exam["listening"] + exam["reading"]:
        group_ids = {g["id"] for g in part["groups"]}
        for q in part["questions"]:
            assert q["groupId"] in group_ids, q["id"]
        for g in part["groups"]:
            for line in g.get("body", []):
                for number in re.findall(r"\{\{(\d+)\}\}", line):
                    assert any(q["number"] == int(number) and q["groupId"] == g["id"] for q in part["questions"]), \
                        f"blank {number} in {g['id']} has no question"
    for part in exam["listening"]:
        assert len(part.get("transcript", [])) > 0, part["id"]


def main() -> None:
    passages = load("passages.json")
    keys = load("keys.json")
    transcripts = load("transcripts.json")
    for (test, skill), fix in KEY_FIXUPS.items():
        keys[test][skill].update(fix)

    OUT.mkdir(parents=True, exist_ok=True)
    built = 0
    for number in range(1, 5):
        module_name = f"test{number}"
        module_path = PACK / "tools" / f"{module_name}.py"
        if not module_path.exists():
            continue
        module = importlib.import_module(module_name)
        exam = module.build(
            passages[str(number)],
            {skill: keys[str(number)][skill] for skill in ("listening", "reading")},
            transcripts[str(number)],
        )
        validate(exam)
        exam.setdefault("audioUrl", f"/media/listening/{exam['id']}")
        path = OUT / f"cambridge21-test{number}.json"
        path.write_text(json.dumps(exam, indent=2, ensure_ascii=False) + "\n")
        size = path.stat().st_size
        print(f"test {number}: {path.name} ({size/1024:.0f} KB)")
        built += 1
    print(f"built {built} exam(s)")


if __name__ == "__main__":
    main()
