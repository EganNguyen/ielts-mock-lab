#!/usr/bin/env python3
"""Verify the IELTS 19 static pack: JSON shape, keys, transcripts and media."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ACADEMIC = ROOT / "content" / "academic"
MEDIA = ROOT / "apps/web/public/media"


def main() -> None:
    total = 0
    for test in range(1, 5):
        exam = json.loads((ACADEMIC / f"ielts19-test{test}.json").read_text())
        assert exam["id"] == f"ielts19-test{test}"
        assert exam["audioUrl"] == f"/media/listening/{exam['id']}"
        lq = [q for p in exam["listening"] for q in p["questions"]]
        rq = [q for p in exam["reading"] for q in p["questions"]]
        assert len(lq) == len(rq) == 40
        assert sorted(q["number"] for q in lq) == list(range(1, 41))
        assert sorted(q["number"] for q in rq) == list(range(1, 41))
        exam_ids: set[str] = set()
        for q in lq + rq:
            assert q["id"] not in exam_ids, f"duplicate id {q['id']}"
            exam_ids.add(q["id"])
            assert q.get("answer"), q["id"]
        assert len(exam["writing"]) == 2 and len(exam["speaking"]) == 3
        for part in exam["listening"]:
            assert sum(len(t["text"].split()) for t in part["transcript"]) > 400, part["id"]
        for part in exam["reading"]:
            assert sum(len(p["text"].split()) for p in part["paragraphs"]) > 600, part["id"]
        for part in range(1, 5):
            audio = MEDIA / "listening" / exam["id"] / f"part{part}.mp3"
            assert audio.exists() and audio.stat().st_size > 1_000_000, audio
        for clip in ("intro", "cue", "prep", "s1", "s10"):
            path = MEDIA / "speaking/examiner" / exam["id"] / f"{clip}.mp3"
            assert path.exists() and path.stat().st_size > 10_000, path
        figure = MEDIA / "figures/ielts19" / f"test{test}-writing-task1.jpg"
        assert figure.exists() and figure.stat().st_size > 20_000, figure
        total += 80

    map_path = MEDIA / "figures/ielts19/test1-listening-map.jpg"
    assert map_path.exists() and map_path.stat().st_size > 20_000, map_path

    index_path = ROOT / "apps/web/public/data/exams/index.json"
    if index_path.exists():
        index = json.loads(index_path.read_text())["exams"]
        assert len(index) == 12, len(index)
        assert {e["id"] for e in index} >= {f"ielts19-test{i}" for i in range(1, 5)}

    print(f"PASS: 4 IELTS 19 tests, {total} objective questions, audio, examiner clips and figures verified.")


if __name__ == "__main__":
    main()
