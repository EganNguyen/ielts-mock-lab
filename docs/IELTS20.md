# IELTS 20 Academic — extracted mock pack

Four complete Academic practice tests extracted from the user-provided
`IELTS 20 Academic.pdf` and compiled into the Apex exam schema.

> **Private study only.** The source book prohibits reproduction without permission from
> Cambridge University Press & Assessment. Do not redistribute this pack. See
> [`extraction-report.md`](../extraction-report.md).

## Tests

| Test | Listening | Reading | Writing | Speaking | Listening audio |
|---|---|---|---|---|---|
| Test 1 | 4 parts / 40 Q | 3 passages / 40 Q | 2 tasks | 3 parts | 19:22 |
| Test 2 | 4 parts / 40 Q | 3 passages / 40 Q | 2 tasks | 3 parts | 16:45 |
| Test 3 | 4 parts / 40 Q | 3 passages / 40 Q | 2 tasks | 3 parts | 18:49 |
| Test 4 | 4 parts / 40 Q | 3 passages / 40 Q | 2 tasks | 3 parts | 20:11 |

320 objective questions with keys, accepted spelling variants and cleaned transcripts.
All four tests are seeded into PostgreSQL by the API on start-up.

## Reading passages

| Test | Passage 1 | Passage 2 | Passage 3 |
|---|---|---|---|
| 1 | The kākāpō | The return of the elm to Britain | How stress affects our judgement |
| 2 | Manatees | Procrastination | Invasion of the Robot Umpires |
| 3 | Frozen Food | Can the planet's coral reefs be saved? | Robots and us |
| 4 | Georgia O'Keeffe | Adapting to the effects of climate change | A new role for livestock guard dogs |

## Assets

- Listening audio (Kokoro-82M): `apps/web/public/media/listening/ielts20-test1..4/part1–4.mp3`
- Examiner prompts (Kokoro): `apps/web/public/media/speaking/examiner/ielts20-test1..4/`
- Writing Task 1 figures: `apps/web/public/media/figures/ielts20/test1–4-writing-task1.jpg`
- Listening map (Test 3 Part 2): `apps/web/public/media/figures/ielts20/test3-listening-map.jpg`

## Screenshots

- [Dashboard](screenshots/ielts20/dashboard.png)
- [Listening runner](screenshots/ielts20/listening.png)
- [Reading runner](screenshots/ielts20/reading.png)
- [Results and answer review](screenshots/ielts20/results.png)

## Source materials

- Page text: `content/ielts20/raw/page-001..183.txt`
- Page images: `content/ielts20/pages/`
- Figure crops: `content/ielts20/figures/`
- Transcripts, keys, passages and page map: `content/ielts20/meta/`
- Build tools: `content/ielts20/tools/`
- One-file archive of text, images, metadata and tools: `content/ielts20/ielts20-extracted.zip`

## Page map (PDF pages)

| | Listening | Reading | Writing | Speaking |
|---|---|---|---|---|
| Test 1 | 3–9 | 11–26 | 28–29 | 33 |
| Test 2 | 39–45 | 47–62 | 64–66 | 71 |
| Test 3 | 77–84 | 86–101 | 103–104 | 108 |
| Test 4 | 114–120 | 122–136 | 138–139 | 143 |
| Audio scripts | 148–182 | | | |

Answer keys are printed inline after each Listening and Reading section
(pages 10, 27, 46, 63, 85, 102, 121, 137) rather than in a back-of-book key section.

## Rebuilding

```bash
cd content/ielts20
python3 tools/make_keys.py       # transcribed answer keys (inline in this book)
python3 tools/extract.py         # audioscripts + page map
python3 tools/passages.py        # cleaned reading passages
python3 tools/build_content.py   # validates and writes content/academic/*.json
cp ../../content/academic/ielts20-test*.json ../../services/api/internal/content/
```

Restart the API to reseed. Regenerate audio only when transcripts change:

```bash
../../.venv-kokoro/bin/python tools/generate_audio.py
../../.venv-kokoro/bin/python tools/generate_speaking.py
```

Gates:

```bash
python3 tools/verify_pack.py
python3 tools/score_check.py
python3 tools/audit_fidelity.py
bash ../../scripts/verify.sh
```

## Source defects repaired during extraction

The supplied PDF is a reflowed/OCR edition with several layout faults. These were
repaired so the tests are usable:

- **Test 1 Listening Part 2, Q17–18:** the book prints options D–H under a
  “Choose TWO letters, A–E” heading and repeats the Q19–20 heading before Q17–18.
  The options were relabelled A–E; the book key `AE` then maps correctly.
- **Test 3 Reading Passage 2, Q22–23:** the book prints options A–F under an A–E
  heading and labels the question stem “A”. Options were relabelled A–E; key `BD`.
- **Test 1 Reading Passage 2 title:** only the words “to Britain” survive in the PDF.
  The title is reconstructed as “The return of the elm to Britain” from the subtitle
  and passage content.
- **Test 1 Listening Part 1:** the third restaurant is spelled “Orley” in the
  transcript but “Audley” in the printed spelling and key; the transcript was corrected.
- **Test 1 Listening Part 4:** lower-case “temps” in the transcript corrected to
  “Thames”.
- Margin question numbers, running heads and footers were stripped from passages and
  scripts; italic glossary footnotes were removed from the rendered passages.

## Known limitations

- Book audioscripts are shorter than a full IELTS recording; generated parts run
  roughly 3–5 minutes each rather than 8–10.
- Some table layouts are flattened into labelled bullet rows for the on-screen runner.
- Writing Task 1 is delivered as a high-resolution crop of the book figure/table.
- Writing and Speaking bands are local rubric estimates, not official IELTS results.
- Sample Writing answers, sample Speaking answers and answer sheets are extracted but
  not wired into the app.
