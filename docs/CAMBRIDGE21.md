# Cambridge IELTS 21 — extracted mock pack

Four complete Academic practice tests extracted from the user-provided Cambridge IELTS 21 PDF and compiled into the Apex exam schema.

> **Private study only.** The source book prohibits reproduction without permission from Cambridge University Press & Assessment and Qunyan Press. Do not redistribute this pack. See [`extraction-report.md`](../extraction-report.md).

## Tests

| Test | Listening | Reading | Writing | Speaking | Listening audio |
|---|---|---|---|---|---|
| Test 1 | 4 parts / 40 Q | 3 passages / 40 Q | 2 tasks | 3 parts | 17:17 |
| Test 2 | 4 parts / 40 Q | 3 passages / 40 Q | 2 tasks | 3 parts | 18:53 |
| Test 3 | 4 parts / 40 Q | 3 passages / 40 Q | 2 tasks | 3 parts | 18:34 |
| Test 4 | 4 parts / 40 Q | 3 passages / 40 Q | 2 tasks | 3 parts | 17:38 |

320 objective questions, all with answer keys and accepted variants. Every test is seeded into PostgreSQL by the API on start-up.

## Reading passages

| Test | Passage 1 | Passage 2 | Passage 3 |
|---|---|---|---|
| 1 | The Davies Sisters | Why we need silence | Book review: The World of Sugar |
| 2 | Do animals dream? | Mapungubwe | Artificial Intelligence |
| 3 | Saving the saiga | Getting around Dar es Salaam | Rethinking the Past |
| 4 | Water hyacinth in Kenya | Multilingualism in Delhi | The Globemakers |

## Assets

- Listening audio (Kokoro-82M, one voice per speaker): `apps/web/public/media/listening/<exam-id>/part1–4.mp3`
- Examiner prompts (Kokoro): `apps/web/public/media/speaking/examiner/<exam-id>/`
- Writing Task 1 figures: `apps/web/public/media/figures/cambridge21/test1–4-writing-task1.jpg`
- Listening map (Test 2 Part 2): `apps/web/public/media/figures/cambridge21/test2-listening-map.jpg`

## Source materials

- Full text: `content/cambridge21/raw/full.txt` (and per-page `page-NNN.txt`)
- Page images: `content/cambridge21/pages/`
- Figure crops: `content/cambridge21/figures/`
- Transcripts, answer keys, cleaned passages: `content/cambridge21/meta/`
- One-file archive of text + images: `content/cambridge21/cambridge21-extracted.zip`
- Build tools: `content/cambridge21/tools/`

## Rebuilding content

See the full [Extraction & Import Guide](EXTRACTION_GUIDE.md) for the reusable workflow, schema notes and troubleshooting.


```bash
cd content/cambridge21
python3 tools/extract.py        # transcripts + answer keys
python3 tools/passages.py       # cleaned reading passages
python3 tools/build_content.py  # validates and writes content/academic/*.json
cp ../../content/academic/cambridge21-test*.json ../../services/api/internal/content/
```

Restart the API to reseed the database. Regenerate listening or examiner audio with
`generate_audio.py` / `generate_speaking.py` only if transcripts change.

## Known limitations

- OCR corrections are selective; minor source artefacts may remain in very long passages.
- Book audioscripts run 3.7–5.8 minutes per part (about 17–19 minutes per test) rather than a full 30-minute recording.
- Writing and Speaking bands are local rubric estimates, not official IELTS results.
- Sample Writing answers, answer sheets and front matter are extracted but not wired into the app.
- A full content audit and known residual differences are recorded in
  [`FIDELITY_REPORT.md`](FIDELITY_REPORT.md).
