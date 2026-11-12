#!/usr/bin/env python3
"""Submit a perfect IELTS 20 attempt through the API and assert 40/40 in both skills."""
from __future__ import annotations

import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
API = "http://127.0.0.1:8080/api/v1"


def req(method: str, path: str, data: dict | None = None):
    body = json.dumps(data).encode() if data is not None else None
    request = urllib.request.Request(API + path, data=body, method=method,
                                     headers={"content-type": "application/json"})
    with urllib.request.urlopen(request, timeout=30) as response:
        raw = response.read()
        return json.loads(raw) if raw else {}


def main() -> None:
    for test in range(1, 5):
        exam = json.loads((ROOT / f"content/academic/ielts20-test{test}.json").read_text())
        created = req("POST", f"/exams/{exam['id']}/attempts", {"mode": "full"})
        attempt = created["attempt"]["id"]
        for skill in ("listening", "reading"):
            req("POST", f"/attempts/{attempt}/sections/{skill}/start")
            part = exam[skill]
            for section in part:
                for q in section["questions"]:
                    req("PUT", f"/attempts/{attempt}/sections/{skill}/answers/{q['id']}",
                        {"value": q["answer"], "version": 0})
            req("POST", f"/attempts/{attempt}/sections/{skill}/submit")
        for skill in ("writing", "speaking"):
            req("POST", f"/attempts/{attempt}/sections/{skill}/start")
            req("POST", f"/attempts/{attempt}/sections/{skill}/submit")
        result = req("POST", f"/attempts/{attempt}/complete")
        assert result["listening"]["raw"] == 40, (test, "listening", result["listening"]["raw"])
        assert result["reading"]["raw"] == 40, (test, "reading", result["reading"]["raw"])
        print(f"test {test}: listening 40/40, reading 40/40, overall {result['overall']}")
    print("PASS: every IELTS 20 answer key scores perfectly.")


if __name__ == "__main__":
    main()
