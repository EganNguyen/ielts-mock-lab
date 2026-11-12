# Guide — extract a vocabulary pack from a new IELTS book

This is the repeatable pipeline used for **IELTS 19**, **IELTS 20** and **Cambridge IELTS 21**.
It produces sentence-first entries, direct Vietnamese translations, optional verified answer
evidence and relationship tags.

> **Rights first.** The books and transcripts are copyrighted. Use this only for private study
> on content you are allowed to process. Do not publish the extracted text or answer keys
> without permission.

## 0. Inputs and output

Input: one JSON file per test in `content/academic/`, with the same shape as the existing packs:

```text
{
  "title": "IELTS 19 · Academic Test 1",
  "listening": [ { "number": 1, "title": "...", "groups": [...],
                   "questions": [...], "transcript": [ { "text": "..." } ] } ],
  "reading":   [ { "number": 1, "title": "...", "paragraphs": [ { "text": "..." } ],
                   "groups": [...], "questions": [...] } ]
}
```

Questions need `number`, `prompt`, `answer`, optional `options`, optional `groupId`.
Question text inside a table/note/summary is stored in its group's `body` with `{{n}}` markers.

Output:

- `content/vocabulary/work/<book>_skeleton.json` — sentence entries before translation.
- `content/vocabulary/work/translate/output-*.json` — Vietnamese translations.
- `content/vocabulary/work/answers/answer-output-*.json` — verified answer evidence.
- `content/vocabulary/ielts19-learning-vocabulary.json` — merged pack (or whichever book).
- `apps/web/src/learning-vocabulary.json` — runtime copy for the page.
- XLSX / CSV / Anki exports.

## 1. Extract candidates

Copy `content/vocabulary/work/extract_ielts19_candidates.py` and change:

1. `FILES` / the `content/academic/ielts19-test*.json` glob to the new book.
2. `CURRENT` to the existing learning pack, so already-known terms are excluded.
3. The blocklist (if needed) for proper names and very basic words.

The script:

- sentence-tokenises every Listening transcript and Reading paragraph;
- POS-tags each sentence, drops proper nouns, stopwords and very short tokens;
- lemmatises and keeps Zipf frequency 2.0–5.25;
- finds one representative sentence per term (12–38 words preferred);
- scores terms by in-question presence, rarity, frequency and length;
- keeps up to 8 terms per section, globally de-duplicated.

```bash
python3 content/vocabulary/work/extract_ielts19_candidates.py
```

Review the printed sample. Terms that are proper names, fragments or purely topical nouns
should be removed before the next step.

## 2. Select and build the skeleton

Start from the candidate JSON. For each kept term, build one entry with:

- `id`: slugs + book suffix (`-i19`), unique across the whole pack;
- `term`, `pos`, `ipa`, `meaningEn`, `synonyms`;
- `sentenceText` copied from the book and `sentenceChunks` split into 2–4 meaningful chunks;
- `sentenceImportance`: Essential / Helpful / Optional;
- `questions`: every question where the term (lemma) appears in the prompt, options or the
  matching `body` segment;
- `references`: one object per section with those question numbers;
- `source`: `exam` when question links exist, otherwise `sentence`;
- empty `meaningVi` and empty `why`.

`prepare_ielts19_items.py` is the reference implementation. It uses NLTK POS, WordNet and
`eng_to_ipa`, then writes one translation input file per test.

```bash
python3 content/vocabulary/work/prepare_ielts19_items.py
```

**Always audit the automatic glosses.** WordNet often returns the wrong sense (`thick` →
“the thick of something”, `metabolism` → metamorphosis, `preserve` → a domain). Run a
two-pass semantic audit and store corrections in a `sense_fixes.json` keyed by item id, then
apply it in the assembler. Check:

- POS matches the sentence (`cheese` is a noun, `listen` is a verb);
- the gloss describes the sense actually used;
- synonyms belong to the same sense;
- IPA exists and is not malformed;
- no proper names, no “a key term used in this section” placeholders.

## 3. Translate directly — no API

Split the skeleton by test. Each input item has:

```json
{ "id": "...", "term": "...", "meaningEn": "...", "sentenceText": "...",
  "sentenceChunks": ["...", "..."], "meaningVi": "" }
```

Ask for exactly one output object per input item, in the same order:

```json
{ "id": "...", "meaningVi": "nghĩa tiếng Việt ngắn gọn",
  "translation": "bản dịch tự nhiên của sentenceText",
  "breakdown": [ { "text": "chunk gốc", "vi": "nghĩa chunk", "role": "main idea" } ] }
```

Rules to give the translator:

- translate directly, never call a translation API or web service;
- keep `______` placeholders and proper names;
- preserve existing non-empty `meaningVi` verbatim;
- one breakdown object per `sentenceChunks` entry, with the original chunk text unchanged;
- short English role labels (`main idea`, `contrast`, `relative clause`, `result`, …);
- do not add facts and do not mention answer keys.

Validate before merging:

```bash
python3 - <<'PY'
import json, glob, os
for f in sorted(glob.glob('content/vocabulary/work/translate/input-*.json')):
    tag = os.path.basename(f)[6:-5]
    src = json.load(open(f)); out = json.load(open(f.replace('input-', 'output-')))
    assert [x['id'] for x in src] == [x['id'] for x in out]
    for a, b in zip(src, out):
        assert set(b) == {'id', 'meaningVi', 'translation', 'breakdown'}
        assert b['meaningVi'].strip() and b['translation'].strip()
        assert [c for c in a['sentenceChunks']] == [d['text'] for d in b['breakdown']]
print('translation OK')
PY
```

## 4. Verify answer evidence (optional but recommended)

Answer selection is **optional**. Include a link only when one complete sentence really
supports the recorded answer.

Build request files with the full section text plus, for each item, every question ref:

```text
content/vocabulary/work/answers/request-ielts19-t1.json
{
  "book": "IELTS 19", "test": 1,
  "sections": { "l1": { "skill": "Listening", "text": "..." }, ... },
  "items": [ { "id": "...", "term": "...", "refs": [
      { "key": "<id>|l1|q1", "section": "l1", "questionNumber": 1,
        "question": "...", "options": [], "answerText": "..." } ] } ]
}
```

The verifier must return, per key, exactly one verbatim sentence plus the connection:

```json
{ "tag": "ielts19-t1", "links": {
  "<key>": { "support": "sentence copied from the section text",
             "connection": "how the question links to this sentence",
             "paraphrasing": "the actual word/phrase swap" } } }
```

Acceptance rules:

- support must be a whitespace-normalised substring of that section's text;
- support should be a complete sentence;
- omit NOT GIVEN, heading matches whose evidence spans a paragraph, and cases where the
  answer needs two separate sentences;
- never change the question or answer;
- do not guess to increase coverage.

Programmatic gate:

```bash
python3 - <<'PY'
import json, re
def norm(s): return re.sub(r'\s+', ' ', s).strip().lower()
req = json.load(open('content/vocabulary/work/answers/request-ielts19-t1.json'))
out = json.load(open('content/vocabulary/work/answers/answer-output-ielts19-t1.json'))
keys = {r['key']: r for i in req['items'] for r in i['refs']}
for key, link in out['links'].items():
    ref = keys[key]
    assert norm(link['support']) in norm(req['sections'][ref['section']]['text'])
print('evidence OK')
PY
```

Then keep only links where the item's term or a synonym is visibly present in the **blank
segment** (the part of the row containing `{{n}}`) or the support sentence. This prevents a
term elsewhere in the same table row from being attached to an unrelated blank.

## 5. Assemble

The assembler merges:

1. the original skeleton(s);
2. all `translate/output-*.json`;
3. all `answers/answer-output-*.json`;
4. hand fixes for duplicate terms, morphology (`carers`/`carer`) and wrong senses;
5. importance and relationship tags.

For each answer link it derives four independent tags:

- **Correct Answer** — term appears in the verified answer;
- **Answer Evidence** — term appears in the verbatim support;
- **Paraphrase** — term/synonym is the bridge between question and evidence;
- **Distractor** — term appears in an incorrect option.

Tags may overlap; no tag is assigned when no relationship is verifiable.

```bash
python3 content/vocabulary/work/assemble_learning_pack.py
cp content/vocabulary/ielts19-21-learning-vocabulary.json apps/web/src/learning-vocabulary.json
```

## 6. Page wiring for a new book

- `testIndex(book, test)` controls order; IELTS 19 → 1–4, IELTS 20 → 5–8, Cambridge 21 → 9–12.
- The test dropdown is generated from `DATA.meta.totalTests`.
- Book labels and the copyright footer name every source book.
- `meta.totalItems`, `meta.totalTests`, `meta.totalSections`, `answerItems` and
  `answerReferences` must match the data.

## 7. Validate and export

```bash
python3 content/vocabulary/tools/verify_learning_vocabulary.py
/Users/tim2k/.dsh/dsh-runtimes/dsh-primary-runtime/dependencies/python/bin/python3 \
  content/vocabulary/tools/build_learning_exports.py
```

The validator checks structure, non-empty fields, unique ids/terms, every support sentence
against the source text, answer importance and relationship tags, and meta counts. Warnings for
entries without answer evidence are expected.

Then:

```bash
pnpm --dir apps/web exec tsc --noEmit
pnpm --dir apps/web build
BASE_PATH=/ielts-mock-lab bash scripts/export-static.sh
```

## 8. Deploy to GitHub Pages

```bash
git add apps/web content/vocabulary docs
git commit -m "Add IELTS 19 vocabulary pack"
git push origin main
gh workflow run pages.yml --ref main
gh run watch --exit-status
```

Verify the live URL, for example:

```text
https://egannguyen.github.io/ielts-mock-lab/vocabulary/
```

Check: page 200, entry count, test filter reaches the new tests, relationship filter, unlock
flow hides evidence/tags/answers before confirmation, and no asset 404.

## Quality gates

- [ ] Every term appears in the book text; no invented words.
- [ ] Every entry has IPA, POS, EN meaning, VI meaning, synonyms, sentence, translation,
      breakdown, why and risk.
- [ ] Breakdown text matches the sentence chunks exactly.
- [ ] POS and gloss describe the sense used in the sentence.
- [ ] No duplicate term, no plural/singular duplicate.
- [ ] Every answer support is verbatim and complete.
- [ ] No answer key, tag or support visible before unlock.
- [ ] Validator, typecheck and both builds pass.
