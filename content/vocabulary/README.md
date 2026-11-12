# Vocabulary data

Sentence-first learning pack: **446 entries** from all Listening parts and Reading passages in
the eight IELTS 20 / Cambridge IELTS 21 tests. **145 entries** carry **196 verified answer
links**, each tagged where a relationship is verifiable (Correct Answer / Answer Evidence /
Paraphrase / Distractor).

| File | Contents |
|---|---|
| `ielts20-21-learning-vocabulary.json` | Source of truth: sentence block + answer evidence + relationship tags |
| `ielts20-21-learning-vocabulary.csv` | Flat spreadsheet export |
| `ielts20-21-learning-vocabulary.xlsx` | Formatted workbook (overview, entries, answers, sections) |
| `ielts20-21-learning-anki.csv` | Anki/Quizlet import (no answer keys) |
| `ielts20-21-exam-vocabulary.json` | Base 249-item answer-focused pack (input for section references) |
| `tools/verify_learning_vocabulary.py` | Validates 446 items and every verbatim answer link |
| `tools/build_learning_exports.py` | Rebuilds CSV, Anki CSV and XLSX |
| `work/learning_skeleton.json` | 451-item skeleton before de-duplication and hand fixes |
| `work/translate/` | Direct Vietnamese translations, one output per test (no translation API) |
| `work/answers/` | Answer evidence verified sentence by sentence against the book text |
| `work/sense_fixes.json` | Hand-checked POS / sense / synonym corrections |

The page imports `apps/web/src/learning-vocabulary.json`.

```bash
python3 content/vocabulary/work/assemble_learning_pack.py
cp content/vocabulary/ielts20-21-learning-vocabulary.json apps/web/src/learning-vocabulary.json
python3 content/vocabulary/tools/verify_learning_vocabulary.py
python3 content/vocabulary/tools/build_learning_exports.py
```

See [`docs/VOCABULARY.md`](../../docs/VOCABULARY.md) for coverage, interface, method and the
copyright note. **Private study only; do not redistribute.**
