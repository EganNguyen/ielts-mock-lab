"""Validate the vocabulary pack against the extracted reading passages."""
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PROJECT = ROOT.parents[1]

data = json.loads((ROOT / "ielts20-21-vocabulary.json").read_text(encoding="utf-8"))
sources = {
    "IELTS 20": json.loads((PROJECT / "content/ielts20/meta/passages.json").read_text(encoding="utf-8")),
    "IELTS 21": json.loads((PROJECT / "content/cambridge21/meta/passages.json").read_text(encoding="utf-8")),
}

errors = []
words = data["words"]
passages = data["passages"]

if len(words) != 360:
    errors.append(f"expected 360 words, found {len(words)}")
if len(passages) != 24:
    errors.append(f"expected 24 passages, found {len(passages)}")

ids = [w["id"] for w in words]
dupes = [value for value, count in Counter(ids).items() if count > 1]
if dupes:
    errors.append(f"duplicate ids: {dupes[:5]}")

by_id = {w["id"]: w for w in words}
for passage in passages:
    key = f"{passage['book']} {passage['test']} {passage['passage']}"
    if len(passage["words"]) != 15:
        errors.append(f"{key}: expected 15 words, found {len(passage['words'])}")
    source = sources[passage["book"]][str(passage["test"])][str(passage["passage"])]
    text = " ".join(p["text"] for p in source["paragraphs"]).lower()
    if source["title"] != passage["title"]:
        errors.append(f"{key}: passage title mismatch")
    for word_id in passage["words"]:
        word = by_id.get(word_id)
        if not word:
            errors.append(f"{key}: unknown word id {word_id}")
            continue
        if word["book"] != passage["book"] or word["test"] != passage["test"] or word["passage"] != passage["passage"]:
            errors.append(f"{key}: source metadata mismatch for {word['word']}")
        if word["surface"].lower() not in text:
            errors.append(f"{key}: surface '{word['surface']}' not found in passage")
        if word["surface"].lower() not in word["example"].lower():
            errors.append(f"{key}: example does not contain '{word['surface']}'")
        if not word["definition"] or len(word["definition"]) < 8:
            errors.append(f"{key}: weak definition for {word['word']}")
        if word["level"] not in {"B1", "B2", "C1", "C2"}:
            errors.append(f"{key}: bad level for {word['word']}: {word['level']}")
        if not word["ipa"] or not word["ipa"].startswith("/"):
            errors.append(f"{key}: bad IPA for {word['word']}: {word['ipa']}")
        if not word["pos"]:
            errors.append(f"{key}: missing part of speech for {word['word']}")

levels = Counter(w["level"] for w in words)
print(f"Words: {len(words)} | Passages: {len(passages)} | Tests: {len({(w['book'], w['test']) for w in words})}")
print("Levels:", ", ".join(f"{k} {v}" for k, v in sorted(levels.items())))
print("Parts of speech:", ", ".join(f"{k} {v}" for k, v in Counter(w["pos"] for w in words).most_common()))

if errors:
    print(f"\nFAIL — {len(errors)} problem(s):")
    for error in errors[:30]:
        print(" -", error)
    sys.exit(1)
print("\nOK — vocabulary pack is consistent with the 24 source passages.")
