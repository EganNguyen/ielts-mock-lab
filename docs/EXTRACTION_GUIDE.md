# Extraction & Import Guide — adding a new IELTS book

This is the repeatable playbook used to turn a scanned Cambridge IELTS book into seeded
Apex mock tests. Follow it top to bottom for Cambridge 22 or any similar book.

## Trigger phrase

When the user says **“extract this pdf for ielts mock test”** (or an equivalent short
request) and supplies a PDF path or attachment, do the whole job without asking design
questions:

1. Read this guide.
2. Derive the pack name from the book title (`cambridge22`, etc.) and keep the folder
   layout `content/<pack>/`.
3. Extract all four Academic tests, answer keys, transcripts, figures and page images.
4. Author/validate the content, generate audio, seed the API and run every gate in
   section 8.
5. Report coverage, fixes and any residual limitations.

Ask only if the PDF path is missing, the book is not an IELTS Academic practice-test
book, or the user has not confirmed they may use the content. Default to private local
use; never publish the extracted book content.

> **Rights check first.** These books prohibit reproduction without publisher permission.
> Only import a PDF you are allowed to use, keep the result private, and do not publish
> the repository or media. The app footer carries attribution.

---

## 0. The pipeline at a glance

```
PDF
 ├─ pdftotext -layout ──────► content/<pack>/raw/page-NNN.txt
 ├─ pdftoppm ───────────────► content/<pack>/pages/*.jpg
 │     └─ PIL crop ────────► content/<pack>/figures/*.jpg
 │
 ├─ tools/extract.py ──────► meta/transcripts.json + meta/keys.json
 ├─ tools/passages.py ─────► meta/passages.json
 ├─ tools/testN.py ────────► (authored groups/questions/writing/speaking)
 └─ tools/build_content.py ─► content/academic/<pack>-testN.json
                              └─ copy ─► services/api/internal/content/
                              └─ audio ─► apps/web/public/media/listening/<exam-id>/
                              └─ figures ► apps/web/public/media/figures/<pack>/
```

Four gates must pass:

1. **Key gate** — 40 listening + 40 reading answers, all numbered 1–40.
2. **Structure gate** — 4 listening parts, 3 passages, 2 writing tasks, 3 speaking parts.
3. **Audio gate** — 4 parts per test exist under `public/media/listening/<exam-id>/`.
4. **App gate** — `scripts/verify.sh` and Playwright pass.

---

## 1. Inspect the PDF and build a page map

```bash
pdfinfo "/path/to/book.pdf"
pdftotext -layout book.pdf - | sed -n '1,60p'      # contents page
```

Record:

- page count, page size, `Page rot` (scanned reprints are often rotated 270);
- whether an OCR text layer exists (`pdftotext` returning real words);
- where Introduction, each Test, Audioscripts, Answer keys, Sample Writing start.

Create a per-page index to find section boundaries quickly:

```bash
mkdir -p content/<pack>/raw
for p in $(seq 1 146); do
  pdftotext -f $p -l $p -layout book.pdf "content/<pack>/raw/page-$(printf %03d $p).txt"
done
```

Then print the first lines of every page and note the map:

```
Test 1  listening 11–16   reading 17–29   writing 30–31   speaking 32
Test 2  listening 33–38   reading 39–51   writing 52–53   speaking 54
...
Audioscripts 98–117, Answer keys 118–125
```

Put this map in `tools/passages.py` (`META`) and `tools/extract.py` (`PAGE_MAP`).
Keep PDF page numbers, not printed page numbers — they differ by a constant.

### Scanned PDFs without a usable text layer

If `pdftotext` returns blank pages (common with scanned reprints), OCR the page images
instead of relying on the text layer:

```bash
mkdir -p content/<pack>/ocr-tess content/<pack>/ocr-tess3
pdftoppm -jpeg -r 200 -jpegopt quality=88 book.pdf content/<pack>/pages/ocr
seq 1 139 | xargs -P 8 -I{} bash -c \
  'p={}; tesseract "content/<pack>/pages/ocr-$(printf %03d "$p").jpg" \
   "content/<pack>/ocr-tess/ocr-$(printf %03d "$p")" --psm 6 -l eng'
seq 1 139 | xargs -P 8 -I{} bash -c \
  'p={}; tesseract "content/<pack>/pages/ocr-$(printf %03d "$p").jpg" \
   "content/<pack>/ocr-tess3/ocr-$(printf %03d "$p")" --psm 3 -l eng'
```

- Use `--psm 6` for answer keys, scripts and single-block question pages.
- Use `--psm 3` for reading passages: it preserves columns and paragraph gaps.
- Check key pages and cropped figures against the rendered image. OCR frequently drops
  small two-column key values; transcribe those directly if the count is not 40/40.
- Keep the rendered page images: they are the ground truth for figures and audit.

### Render page images and figures

```bash
pdftoppm -jpeg -r 120 -jpegopt quality=82 book.pdf content/<pack>/pages/p
```

Crop each figure with PIL and **look at every crop**. A good crop starts below the
“Write at least 150 words.” line and includes the whole chart/table.

```python
from PIL import Image, ImageOps
im = ImageOps.autocontrast(Image.open("pages/p-030.jpg").convert("L"), cutoff=1)
im.crop((180, 705, 900, 1110)).resize((1152, 648), Image.LANCZOS).save(
    "figures/test1-writing-task1.jpg", quality=92, optimize=True)
```

Watch for: stray text at the top, clipped legends/labels, table rows cut off at the
bottom. Adjust coordinates by 8–15 px and re-check.

---

## 2. Extract answer keys and audioscripts

`tools/extract.py` is deterministic and should be copied into the new pack folder.
Change `PDF`, `TEST_START`/`PAGE_MAP`, and the test range if the book has a different
layout.

```bash
cd content/<pack>
python3 tools/extract.py
```

Expected output:

```
keys test 1 listening: 40 answers
keys test 1 reading: 40 answers
...
```

### Answer keys

Most books print the keys in one back-of-book section. Some reprints (for example the
IELTS 20 PDF) print each Listening and Reading key immediately after the questions.
Check the page map first: if there are `Answer:` pages after each skill, transcribe
those pages directly into `meta/keys.json` rather than trying to reuse the Cambridge 21
parser unchanged.

For a back-of-book key printed in two columns, `-layout` interleaves the columns, so the
parser reads `pdftotext -raw` one page at a time. It understands:

- `Part 1, Questions 1-10` / `Reading Passage 1, Questions 1-13`;
- `21 &22 IN EITHERORDER` followed by two letters (choose-TWO);
- `10/ten`, `cafe I cafe`, `48 I forty-eight` (spelling alternatives);
- `metal(s)`, `holiday(s)` (optional plural expansion);
- `NOTGIVEN` → `NOT GIVEN`.

**Known failure:** a two-column page can still interleave a letter and a number on one
line (`A 8 67.50 I …`). The current pack fixes this in `build_content.py`:

```python
KEY_FIXUPS = {
    ("2", "listening"): {"8": ["67.50"], "25": ["A", "C"], "26": ["A", "C"]},
}
```

After parsing, diff the loaded keys against the printed page and add a fixup if any
number is missing or obviously wrong.

### Audioscripts

The parser splits on `TEST n` and `PART n`, treats `NAME:` lines as speaker turns and
joins wrapped lines. It strips printed question markers that OCR leaves in the margin.

Known marker shapes and the cleaning rules already in place:

| Raw shape | Fix |
|---|---|
| `text            023/24` | trailing `\s{2,}\d[\d\s/]{0,12}$` |
| `text          07 5` | same rule (allows spaces inside the marker) |
| `text          O 15` | same rule with optional `O`/`Q`/`©` prefix |

After extraction, assert no marker survives:

```python
assert not re.search(r"\b[OQ]\s?\d{1,3}\b", text)
assert not re.search(r"\d{2,6}/\d", text)
```

Check starts/ends of each part — they should read like natural speech, not page headers.

---

## 3. Clean the reading passages

`tools/passages.py` removes running heads, footers, titles, subtitles, glossary
footnotes and section labels, then merges continuation paragraphs.

Configure each passage in `META`:

```python
"1": {
    "pages": [17, 18],
    "title": "The Davies Sisters",
    "subtitle": "Between 1908 and 1924, …",
    "labeled": False,        # True when sections are A–G
},
"3": {
    "pages": [47, 48],
    "title": "Artificial Intelligence",
    "subtitle": "",
    "two_column": True,
    "starts": ["In many countries…", "While it is undeniable…", …],
},
```

Run:

```bash
python3 tools/passages.py
```

Rules that matter:

- **Labelled passages** (`A Humans are…`): set `labeled: True`; continuation paragraphs
  are merged into the previous section so `A–G` map one-to-one.
- **Two-column pages**: `pdftotext -layout` mixes columns. Use `two_column: True`
  (switches to `-raw`) and supply the first few words of each paragraph in `starts`.
- **Footnotes** (`* palisade: …`, `** …`): dropped automatically.
- **Subtitles**: exact text must match, or drop the first paragraph with
  `drop_first: 1` (useful when OCR misspells a name).
- **OCR corrections**: add to `CORRECTIONS` in `passages.py`, e.g.
  `"Dares Salaam" → "Dar es Salaam"`, `"UlbeBosma" → "Ulbe Bosma"`,
  `"Belferby" → "Bellerby"`, `"·while" → "While"`.

Inspect the JSON before authoring questions:

```bash
python3 -c "import json;d=json.load(open('meta/passages.json'));print([(k, [p['label'] for p in v['paragraphs']]) for k,v in d.items()])"
```

For every passage you expect `A…G` count, ~800–1000 words and no leftover titles.

---

## 4. Author the questions (`tools/testN.py`)

Use `common.py` helpers. One file per test, returning the exam dict.

```python
from common import apply_keys, group, passage, question

def build(passages, keys, transcripts):
    ...
```

### Group layouts

| Layout | Use | Rendering |
|---|---|---|
| `"notes"`, `"form"`, `"summary"`, `"flow"` | completion | `body` lines with `{{n}}` blanks, inline inputs |
| `"match"` | matching features/people | `sharedOptions`, one select per question |
| `"map"` | map labelling | `figure` + `figure`/`sharedOptions` letters |
| `""` | MCQ / TFNG / YNNG | one row per question |

Body line syntax:

```python
body=[
    "# Section heading",
    "## SUBHEAD",
    "• bullet with the {{31}} blank",
    "  – sub-bullet",
    "↓",                       # flow-chart arrow
]
```

- `{{n}}` must match a question number in the same group; `build_content.py`
  enforces this.
- Notes render in a single column; keep rows short and bullets parallel.
- For tables, flatten to labelled rows:
  `"• Bread making — 20 March — cost: £{{2}} — make white bread, sourdough and {{3}}"`.
- Use `figure` + `figureAlt` for real diagrams/maps instead of inventing HTML.
- Choose-TWO groups: two MCQ questions with the **same options**; the renderer collapses
  them into one option list with two letter selects.

### Question types

`short`, `mcq`, `tfng`, `ynng`, `match`, `select`, `heading`, `map`.

### Keys

```python
apply_keys(qs, keys["listening"], "l1")   # ids become l1-q1 … l1-q10
```

Then the exam needs:

```python
{
  "id": "cambridge22-test1",
  "title": "Cambridge IELTS 22 · Academic Test 1",
  "audioUrl": "/media/listening/cambridge22-test1",
  ...
}
```

Keep IDs unique across tests (`l1-q1`, `r2-q14`, `writing-task-1`, `s1`).

---

## 5. Build, validate, seed

`build_content.py` is the gatekeeper. It asserts:

- 4 listening parts, 3 passages, 2 writing tasks, 3 speaking parts;
- 40 + 40 questions, answer key on every question;
- unique question numbers 1–40 in each skill;
- every inline `{{n}}` has a matching question in the same group;
- every listening part has a transcript.

```bash
python3 tools/build_content.py
cp ../../content/academic/<pack>-test*.json ../../services/api/internal/content/
```

Restart the API so the embed and seed pick up the new JSON:

```bash
lsof -ti tcp:8080 | xargs kill
cd services/api && LOCAL_DEMO_MODE=true APP_ENV=development \
  DATABASE_URL='postgres://apex:apex@127.0.0.1:5433/apex?sslmode=disable' \
  MEDIA_DIR='./media' WEB_ORIGIN='http://127.0.0.1:3000' go run ./cmd/api &
```

Check the public payload:

```bash
curl -s localhost:8080/api/v1/exams/<exam-id> | python3 -c "
import sys,json; d=json.load(sys.stdin)
print(d['title'], d['audioUrl'])
print(sum(len(p['questions']) for p in d['listening']), 'listening')"
```

The dashboard lists every seeded exam automatically, ordered by ID in the UI.

---

## 6. Generate audio

Audio is the slowest step (~15–20 min per book when run serially, RTF ≈ 0.15).
Generate *after* transcripts are final, otherwise you will redo it.

```bash
cd /path/to/ielts-mock-lab
.venv-kokoro/bin/python content/<pack>/tools/generate_audio.py
.venv-kokoro/bin/python content/<pack>/tools/generate_speaking.py
```

`generate_audio.py` handles listening; `generate_speaking.py` handles examiner prompts.
Together they:

- chunk long turns at sentence boundaries (~240 chars);
- map speakers to distinct British voices (`bf_*` / `bm_*`);
- add a narrator intro (`Test N. Listening. Part N.`) and short gaps;
- write MP3s under `apps/web/public/media/listening/<exam-id>/partN.mp3`;
- write examiner clips under `public/media/speaking/examiner/<exam-id>/`.

Sound check: open the file, confirm speech is intelligible, the first sentence is the
narrator, and no spoken “zero two one slash two four” artifacts remain. Re-run only
if transcripts changed — the generator skips existing files > 1 MB.

Add duration/size logging to spot truncated parts:

```bash
for f in apps/web/public/media/listening/<exam-id>/*.mp3; do
  ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$f"
done
```

---

## 7. Figures and app wiring

Most content works with no code changes. Touch the app only when the schema grows:

| Need | File |
|---|---|
| New group/question field | `services/api/internal/model/model.go`, `apps/web/src/lib/api.ts` |
| How a new type renders | `apps/web/src/components/exam/Questions.tsx` |
| Writing Task 1 figure | `apps/web/app/exam/[attemptId]/page.tsx` |
| Audio base URL | `Exam.audioUrl` (`/media/listening/<exam-id>`) |
| Figures | `apps/web/public/media/figures/<pack>/*.jpg` |

If you add a new exam format (e.g. diagram labelling with drag/drop), add the type to
both the Go model and the TS union, then render it in `QuestionSets`.

---

## 8. Verify

```bash
bash scripts/verify.sh
cd services/api && go test ./...
cd apps/web && pnpm exec playwright test --trace=off
python3 content/<pack>/tools/verify_pack.py      # content + API + assets, all four tests
python3 content/<pack>/tools/audit_fidelity.py   # fuzzy text match against raw pages
```

`verify.sh` checks the four exams, every part MP3, figures and examiner clips. The
Playwright suite includes a perfect-answer attempt that asserts 40/40 → Band 9 and a
refresh/autosave test.

Also test the UI transition once: start a test → submit Listening → **Start Reading**
(note: after submission it is a “Start Reading” button, not “Continue”).

---

## 9. Checklist for the next book

```
[ ] Rights confirmed; content is private
[ ] pdfinfo + page map recorded
[ ] raw/page-*.txt for every page
[ ] pages/*.jpg rendered, figures cropped and visually checked
[ ] keys: 40/40 per test; two-column fixups applied
[ ] transcripts: speakers detected, no margin markers, sensible starts/ends
[ ] passages: titles, A–G labels, no footnotes/subtitles, OCR spot-check
[ ] testN.py authored; build_content.py passes
[ ] JSON copied to services/api/internal/content; API restarted and reseeded
[ ] listening audio + speaking audio generated; spot-check one part
[ ] verify.sh PASS; Go tests PASS; Playwright PASS
[ ] verify_pack.py PASS (API review + audio/figures)
[ ] audit_fidelity.py reviewed; every finding explained (generic labels are fine)
[ ] screenshots captured for docs
```

---

## 9a. When the source PDF is defective

Digitised reprints sometimes contain editing faults that are not OCR noise. Check each
question block rather than trusting the lettering:

- a “Choose TWO letters, A–E” question whose options are printed D–H;
- a repeated or wrong question-range heading above a group;
- option lists that start at B–F because the stem was mislabelled A;
- answer keys that use `T/F/NG` for one task and `Y/N/NG` for another;
- transcript names that disagree with the printed spelling or the key.

Fix the lettering to match the instruction and key (`A–E` options, keys re-lettered),
record the change in the pack doc, and note the reconstruction. Do not silently keep an
unusable option set.

## 10. Troubleshooting

| Symptom | Cause / fix |
|---|---|
| `KeyError: questions without keys: [...]` | The authored question numbers do not all exist in `keys.json`; check the key parse and the question numbering. |
| 39/40 in scoring | A key is not being matched. Inspect the review payload and add accepted variants (`metal(s)` → `metal`, `metals`). |
| Answer keys look interleaved | Two-column key page. Use `-raw` per page; add `KEY_FIXUPS` for residual lines. |
| Reading text mixes two columns | Set `two_column: True` and provide `starts`; verify paragraph count. |
| Section labels missing | Set `labeled: True`; labels need a capitalised next word. |
| Blank renders as `[31]` | Missing question number in the same group; `build_content` should have caught it. |
| Audio 404 | `exam.audioUrl` must be `/media/listening/<exam-id>` and files must exist under `public/media/listening/<exam-id>/`. |
| Exam not in dashboard | API was not restarted after copying JSON into `internal/content/`; restart and check `/api/v1/exams`. |
| Figure top text/clipped table | Recrop; leave 8–15 px padding; check at 100% and in the app. |
| e2e timeout at audio overlay | Browser autoplay blocked; click “Play exam audio” in the test or accept the overlay. |
| `sf.write … System error` during generation | The temp directory was removed under the run. Write WAVs to `tempfile.mkdtemp()` (already fixed). |
| Playwright trace `ENOENT … recording.network` | Stale `test-results/` from parallel runs; `rm -rf test-results` and rerun with `--trace=off`. |
| `audit_fidelity.py` flags a prompt | Low token overlap usually means a generic label (“The first point”) rather than a book quote. Only fix flags for statements/options/passages. |

---

## 11. Minimal authoring skeleton

```python
from common import apply_keys, group, passage, question

def build(passages, keys, transcripts):
    # --- Listening part 1 -------------------------------------------------
    qs = [question(n, "l1-g1", f"Note {n}") for n in range(1, 11)]
    apply_keys(qs, keys["listening"], "l1")
    l1 = {
        "id": "l1", "number": 1,
        "title": "A booking enquiry",
        "context": "A telephone conversation about a course.",
        "groups": [group(
            "l1-g1", "Questions 1–10",
            "Complete the notes below. Write ONE WORD ONLY for each answer.",
            list(range(1, 11)), layout="notes",
            body=["# Course notes",
                  "• name: {{1}}", "• address: {{2}}", "• cost: £{{3}}", "• date: {{4}}",
                  "• time: {{5}}", "• bring: {{6}}", "• lunch: {{7}}", "• book: {{8}}",
                  "• email: {{9}}", "• phone: {{10}}"],
        )],
        "questions": qs,
        "transcript": transcripts["1"],
    }

    # --- Reading passage 1 ------------------------------------------------
    r1 = passage(1, passages["1"])
    rq = [question(n, "r1-g1", f"Note {n}") for n in range(1, 4)]
    apply_keys(rq, keys["reading"], "r1")
    r1["groups"] = [group(
        "r1-g1", "Questions 1–3",
        "Complete the notes below. Choose ONE WORD ONLY from the passage.",
        list(range(1, 4)), layout="notes",
        body=["# Section heading", "• first answer: {{1}}", "• second: {{2}}", "• third: {{3}}"],
    )]
    r1["questions"] = rq

    return {
        "id": "cambridge22-test1",
        "title": "Cambridge IELTS 22 · Academic Test 1",
        "module": "Academic",
        "version": "cambridge22.1",
        "listening": [l1] + other_listening_parts(),
        "reading": [r1] + other_passages(),
        "writing": writing_tasks(),
        "speaking": speaking_parts(),
        "audioUrl": "/media/listening/cambridge22-test1",
        "scoring": {
            "listeningVersion": "ielts-academic-2026",
            "readingVersion": "ielts-academic-2026",
            "rubricVersion": "apex-local-rubric-v1",
        },
    }
```

Every `{{n}}` must have a question in the same group; questions without a blank render
as ordinary answer rows. `build_content.py` fails if a blank has no question or a
question has no key.

## 12. Reusing this pack as a template

1. Copy `content/cambridge21/` to `content/cambridge22/`.
2. Change `PDF`, `TEST_START`, `PAGE_MAP`, and page ranges.
3. Update `META` titles/pages and `CORRECTIONS`.
4. Rename test modules/IDs (`cambridge22-test1`, etc.) and update `build_content.py`’s
   glob/constants if the pack name changes.
5. Copy the new JSON into `services/api/internal/content/` — `content.go` embeds
   `*-test*.json`, so every `<pack>-testN.json` is picked up automatically.
6. Generate audio and run the gates above.

For a different exam format, keep the same four-skill envelope so the Go validator,
scoring tables and UI timing continue to work.
