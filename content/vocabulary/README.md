# Vocabulary data

Sentence-first learning pack: **663 entries** from all Listening parts and Reading passages in
the twelve IELTS 19 / IELTS 20 / Cambridge IELTS 21 tests. **242 entries** carry **357 verified
answer links**, each tagged where a relationship is verifiable (Correct Answer / Answer
Evidence / Paraphrase / Distractor).

| File | Contents |
|---|---|
| `ielts19-21-learning-vocabulary.json` | Source of truth: sentence block + answer evidence + relationship tags |
| `ielts19-21-learning-vocabulary.csv` | Flat spreadsheet export |
| `ielts19-21-learning-vocabulary.xlsx` | Formatted workbook (overview, entries, answers, sections) |
| `ielts19-21-learning-anki.csv` | Anki/Quizlet import (no answer keys) |
| `ielts19-21-exam-vocabulary.json` | Base 249-item IELTS 20/21 answer-focused pack (input for section references) |
| `ielts20-21-learning-vocabulary.json` | Previous 446-entry IELTS 20/21 pack (kept as a checkpoint) |
| `tools/verify_learning_vocabulary.py` | Validates 663 items and every verbatim answer link |
| `tools/build_learning_exports.py` | Rebuilds CSV, Anki CSV and XLSX |
| `work/learning_skeleton.json` | IELTS 20/21 skeleton before de-duplication and hand fixes |
| `work/ielts19_skeleton.json` | IELTS 19 skeleton after POS/sense fixes |
| `work/translate/` | Direct Vietnamese translations, one output per test (no translation API) |
| `work/answers/` | Answer evidence verified sentence by sentence against the book text |
| `work/sense_fixes.json`, `work/ielts19_sense_fixes.json` | Hand-checked POS / sense / synonym corrections |

The page imports `apps/web/src/learning-vocabulary.json`.

```bash
python3 content/vocabulary/work/assemble_learning_pack.py
cp content/vocabulary/ielts19-21-learning-vocabulary.json apps/web/src/learning-vocabulary.json
python3 content/vocabulary/tools/verify_learning_vocabulary.py
python3 content/vocabulary/tools/build_learning_exports.py
```

See [`docs/VOCABULARY.md`](../../docs/VOCABULARY.md) for coverage, interface and method, and
[`docs/VOCABULARY_EXTRACTION_GUIDE.md`](../../docs/VOCABULARY_EXTRACTION_GUIDE.md) for the
repeatable extraction pipeline. **Private study only; do not redistribute.**
