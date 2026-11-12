# Extraction Report — Cambridge IELTS 21

## Source inspected

- File: `/Users/tim2k/Downloads/Cambridge Ielts 21.pdf`
- PDF: 146 pages, image scan with an Adobe Paper Capture OCR layer, page rotation 270.
- Title: Cambridge IELTS 21 (Academic), Cambridge University Press & Assessment / Qunyan Press reprint, 2026.

## Copyright finding

The source copyright page states:

> "No part of this publication may be reproduced or distributed by any means, or stored in a database or retrieval system, without the prior written permission of Cambridge University Press & Assessment and Qunyan Press."

The four tests were nevertheless extracted at the user's explicit direction, for **private local study** in this repository. The material is not licensed. Do not publish, redistribute or monetise this repository or its `content/`, `apps/web/public/media/` or `services/api/internal/content/` Cambridge assets without written permission from the rights holders. The application footer carries a visible attribution.

## What was extracted

| Asset | Location | Count |
|---|---|---|
| Page text (layout preserving) | `content/cambridge21/raw/page-*.txt` | 146 pages |
| Page images (120 dpi JPEG) | `content/cambridge21/pages/` | 146 pages |
| Structured exam JSON | `content/academic/cambridge21-test1..4.json` | 4 tests |
| Embedded API copy | `services/api/internal/content/cambridge21-test*.json` | 4 tests |
| Task 1 figures + listening map | `content/cambridge21/figures/` and `apps/web/public/media/figures/cambridge21/` | 5 crops |
| Listening audio (Kokoro) | `apps/web/public/media/listening/<exam-id>/part1-4.mp3` | 16 parts |
| Examiner audio (Kokoro) | `apps/web/public/media/speaking/examiner/<exam-id>/` | 52 clips |
| Extracted metadata | `content/cambridge21/meta/` | transcripts, keys, passages, page map |

Per test: 40 Listening questions (4 parts), 40 Reading questions (3 passages), 2 Writing tasks, 3 Speaking parts. Total 320 objective questions.

## Pipeline

```
PDF ──pdftotext -layout──> raw/page-*.txt
    ──pdftoppm / PIL──────> pages/*.jpg ──crop──> figures/*.jpg

raw ──tools/extract.py───> meta/transcripts.json + meta/keys.json
raw ──tools/passages.py──> meta/passages.json (OCR corrections, sections)
meta + tools/testN.py ──tools/build_content.py──> content/academic/*.json
content ──tools/generate_audio.py / generate_speaking.py──> public/media/**
```

Rebuild commands:

```bash
cd content/cambridge21
python3 tools/extract.py
python3 tools/passages.py
python3 tools/build_content.py
cp ../../content/academic/cambridge21-test*.json ../../services/api/internal/content/
# audio (only needed when transcripts change)
../../.venv-kokoro/bin/python tools/generate_audio.py
../../.venv-kokoro/bin/python tools/generate_speaking.py
```

The build step validates: four listening parts, three passages, two writing tasks,
three speaking parts, 40 listening and 40 reading answers, unique question numbers,
answer keys present for every objective question and every inline blank resolved to a
question in the same group.

## Reusable workflow

For importing another book or adding a test, use [`docs/EXTRACTION_GUIDE.md`](docs/EXTRACTION_GUIDE.md). It covers the page map, key/transcript parsing, passage cleaning, question authoring, figure crops, audio generation, validation gates and troubleshooting.

## Known limitations

- OCR typos in source text were corrected selectively (names, two-column passages,
  stray margin question numbers); reading passages may retain minor original OCR
  artefacts.
- The book's audioscripts are shorter than a full IELTS recording; generated parts run
  about 4–6 minutes each rather than 8–10.
- Writing and Speaking scores are local rubric estimates, not official IELTS results.
- Sample Writing answers, sample answer sheets and the Introduction/Acknowledgements
  pages were extracted as text/images but are not wired into the app.

---

# Addendum — IELTS 20 Academic (second pack)

## Source inspected

- File: `/Users/tim2k/Downloads/IELTS 20 Academic.pdf`
- PDF: 183 pages, A4, text layer present (Microsoft Word 2016 + A-PDF Watermark).
- Book: IELTS 20 Academic, Cambridge University Press & Assessment, 2025 printing.
- Pack folder: `content/ielts20/`; exam IDs `ielts20-test1` … `ielts20-test4`.

## What was extracted

| Asset | Location | Count |
|---|---|---|
| Page text (layout preserving) | `content/ielts20/raw/page-*.txt` | 183 pages |
| Page images (120 dpi JPEG) | `content/ielts20/pages/` | 183 pages |
| Structured exam JSON | `content/academic/ielts20-test1..4.json` | 4 tests |
| Embedded API copy | `services/api/internal/content/ielts20-test*.json` | 4 tests |
| Task 1 figures + listening map | `content/ielts20/figures/` and `apps/web/public/media/figures/ielts20/` | 5 crops |
| Listening audio (Kokoro) | `apps/web/public/media/listening/<exam-id>/part1-4.mp3` | 16 parts |
| Examiner audio (Kokoro) | `apps/web/public/media/speaking/examiner/<exam-id>/` | 52 clips |
| Metadata | `content/ielts20/meta/` | transcripts, keys, passages, page map |

Per test: 40 Listening (4 parts), 40 Reading (3 passages), 2 Writing tasks, 3 Speaking
parts. Total: 320 objective questions.

## Page map

| | Listening | Reading | Writing | Speaking |
|---|---|---|---|---|
| Test 1 | 3–9 | 11–26 | 28–29 | 33 |
| Test 2 | 39–45 | 47–62 | 64–66 | 71 |
| Test 3 | 77–84 | 86–101 | 103–104 | 108 |
| Test 4 | 114–120 | 122–136 | 138–139 | 143 |

Answer keys are inline after each skill section on pages 10, 27, 46, 63, 85, 102, 121 and
137. Audio scripts occupy pages 148–182.

## Pipeline changes for this pack

- `tools/make_keys.py` transcribes the inline keys (the Cambridge 21 back-of-book key
  parser does not apply).
- `tools/extract.py` parses scripts from pages 148–182, including inline `Part N`
  headings and inline speaker labels, and repairs two truncated script openings.
- `tools/passages.py` uses explicit paragraph starts for all 12 passages, plus label
  letters A–G where the passage is sectioned.
- `tools/build_content.py` targets `ielts20-testN.json` and writes to
  `content/academic/`.
- `services/api/internal/content/content.go` now embeds `*-test*.json`, so both packs
  seed from one binary.

## Source defects repaired

- Test 1 Listening Part 2 Q17–18: options printed D–H under an A–E instruction and the
  Q19–20 heading repeated above Q17–18. Relabelled A–E; key `AE`.
- Test 3 Reading Passage 2 Q22–23: options printed A–F under an A–E instruction and the
  stem mislabelled A. Relabelled A–E; key `BD`.
- Test 1 Reading Passage 2: only “to Britain” survives as the printed title. Reconstructed
  as “The return of the elm to Britain”.
- Test 1 Listening transcript: “Orley” corrected to the printed/key spelling “Audley”;
  “£30 ahead” → “£30 a head”; “temps” → “Thames”; “kil” → “kiln”.
- Margin numbers, running heads, page footers and book footnotes removed from passages.

## Verification

```bash
python3 content/ielts20/tools/verify_pack.py   # content + API + assets
python3 content/ielts20/tools/score_check.py   # 40/40 listening and reading, all tests
python3 content/ielts20/tools/audit_fidelity.py
bash scripts/verify.sh
cd services/api && go test ./...
cd apps/web && pnpm exec playwright test --trace=off
```

`score_check.py` submits every correct key through the API and asserts 40/40 for both
objective skills in all four tests. `audit_fidelity.py` compares authored stems, options,
passages and prompts with the raw pages; residual findings are generic paraphrased
completion prompts, not content differences.
