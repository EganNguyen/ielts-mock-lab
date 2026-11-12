#!/usr/bin/env python3
"""Compile the IELTS 20 pack into the Apex exam content schema."""
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


def split_choose_two(exam: dict) -> None:
    """Give each question in a choose-TWO pair a distinct key.

    apply_keys stores the full pair on both rows (answer=A, accepted=[B]), which
    lets a candidate choose the same letter twice and score two marks. Split the
    pair so either order is accepted but a duplicate letter loses one mark.
    """
    for part in exam["listening"] + exam["reading"]:
        for group in part["groups"]:
            qs = [q for q in part["questions"] if q["groupId"] == group["id"]]
            if (len(qs) == 2 and all(q["type"] == "mcq" for q in qs)
                    and qs[0].get("accepted") and qs[0].get("accepted") == qs[1].get("accepted")
                    and qs[0].get("answer") == qs[1].get("answer")):
                first = qs[0]["answer"]
                second = qs[0]["accepted"][0]
                qs[1]["answer"] = second
                qs[1]["accepted"] = [first]


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
    assert sorted(q["number"] for q in lq) == list(range(1, 41))
    assert sorted(q["number"] for q in rq) == list(range(1, 41))
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
        split_choose_two(exam)
        validate(exam)
        exam.setdefault("audioUrl", f"/media/listening/{exam['id']}")
        path = OUT / f"ielts20-test{number}.json"
        path.write_text(json.dumps(exam, indent=2, ensure_ascii=False) + "\n")
        print(f"test {number}: {path.name} ({path.stat().st_size/1024:.0f} KB)")
        built += 1
    print(f"built {built} exam(s)")


if __name__ == "__main__":
    main()
