#!/usr/bin/env python3
"""End-to-end pack verification: content shape + API + assets.

Usage (API and web running):
    python3 content/cambridge21/tools/verify_pack.py
"""
from __future__ import annotations

import json
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ACADEMIC = ROOT / "content" / "academic"
WEB = "http://127.0.0.1:3000"
API = "http://127.0.0.1:8080/api/v1"


def req(method: str, url: str, data: dict | None = None):
    body = json.dumps(data).encode() if data is not None else None
    request = urllib.request.Request(url, data=body, method=method, headers={"content-type": "application/json"})
    with urllib.request.urlopen(request, timeout=20) as response:
        raw = response.read()
        return json.loads(raw) if raw else {}


def http_status(url: str) -> int:
    try:
        with urllib.request.urlopen(url, timeout=20) as response:
            return response.status
    except Exception:
        return 0


def content_checks(test: int) -> dict:
    path = ACADEMIC / f"cambridge21-test{test}.json"
    exam = json.loads(path.read_text())
    lq = [q for p in exam["listening"] for q in p["questions"]]
    rq = [q for p in exam["reading"] for q in p["questions"]]
    assert len(lq) == len(rq) == 40, (test, len(lq), len(rq))
    assert sorted(q["number"] for q in lq) == list(range(1, 41))
    assert sorted(q["number"] for q in rq) == list(range(1, 41))
    assert len(exam["writing"]) == 2 and len(exam["speaking"]) == 3
    assert exam.get("audioUrl", f"/media/listening/cambridge21-test{test}") == f"/media/listening/cambridge21-test{test}"
    for part in exam["listening"]:
        assert part["transcript"] and sum(len(t["text"].split()) for t in part["transcript"]) > 400, part["id"]
        assert part["title"] and part["context"]
    for passage in exam["reading"]:
        assert passage["title"] and passage["paragraphs"]
        assert sum(len(p["text"].split()) for p in passage["paragraphs"]) > 600, passage["id"]
    for q in lq + rq:
        assert q["answer"], q["id"]
    for task in exam["writing"]:
        assert task["prompt"] and task["instructions"]
    for part in exam["speaking"]:
        assert part["questions"] or part.get("cueCard")
    return {"questions": len(lq) + len(rq), "tracks": len(exam["listening"])}


def api_checks(test: int) -> dict:
    exam_id = f"cambridge21-test{test}"
    public = req("GET", f"{API}/exams/{exam_id}")
    assert public["id"] == exam_id
    assert public["audioUrl"] == f"/media/listening/{exam_id}"
    for part in public["listening"]:
        assert part.get("transcript") in (None, [])
        for q in part["questions"]:
            assert "answer" not in q or not q["answer"]
    assert all("answer" not in q or not q["answer"] for p in public["reading"] for q in p["questions"])
    assert all(t.get("modelAnswer") in (None, "") for t in public["writing"])

    created = req("POST", f"{API}/exams/{exam_id}/attempts", {"mode": "full"})
    attempt_id = created["attempt"]["id"]
    for skill in ("listening", "reading", "writing"):
        req("POST", f"{API}/attempts/{attempt_id}/sections/{skill}/start")
        req("POST", f"{API}/attempts/{attempt_id}/sections/{skill}/submit")
    req("POST", f"{API}/attempts/{attempt_id}/sections/speaking/start")
    req("POST", f"{API}/attempts/{attempt_id}/sections/speaking/submit")
    req("POST", f"{API}/attempts/{attempt_id}/complete")
    review = req("GET", f"{API}/attempts/{attempt_id}/review")
    assert review["exam"]["id"] == exam_id
    assert sum(len(p["questions"]) for p in review["exam"]["listening"]) == 40
    assert sum(len(p["questions"]) for p in review["exam"]["reading"]) == 40
    assert review["exam"]["writing"][0]["prompt"]
    assert review["exam"]["speaking"][0]["questions"]
    return {"attempt": attempt_id, "review_questions": 80}


def asset_checks(test: int) -> dict:
    exam_id = f"cambridge21-test{test}"
    checked = 0
    for part in range(1, 5):
        path = ROOT / f"apps/web/public/media/listening/{exam_id}/part{part}.mp3"
        assert path.exists() and path.stat().st_size > 1_000_000, path
        assert http_status(f"{WEB}/media/listening/{exam_id}/part{part}.mp3") == 200
        checked += 1
    for asset in ("intro", "cue", "prep", "s1", "s10"):
        path = ROOT / f"apps/web/public/media/speaking/examiner/{exam_id}/{asset}.mp3"
        assert path.exists() and path.stat().st_size > 10_000, path
        checked += 1
    figure = ROOT / f"apps/web/public/media/figures/cambridge21/test{test}-writing-task1.jpg"
    assert figure.exists() and figure.stat().st_size > 20_000, figure
    assert http_status(f"{WEB}/media/figures/cambridge21/test{test}-writing-task1.jpg") == 200
    if test == 2:
        map_path = ROOT / "apps/web/public/media/figures/cambridge21/test2-listening-map.jpg"
        assert map_path.exists() and map_path.stat().st_size > 20_000
    return {"assets": checked + 1}


def main() -> None:
    total = 0
    for test in range(1, 5):
        content = content_checks(test)
        api = api_checks(test)
        assets = asset_checks(test)
        total += content["questions"]
        print(f"test {test}: OK  {content['questions']} questions, attempt {api['attempt'][:8]}…, {assets['assets']} assets")
    print(f"PASS: 4 tests, {total} objective questions, API review and all media assets verified.")


if __name__ == "__main__":
    main()
