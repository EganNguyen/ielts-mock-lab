# Content Fidelity Report — Cambridge IELTS 21 pack

Audit date: 2026-11-12. Scope: the four seeded Cambridge IELTS 21 Academic tests.

## Coverage

| Item | Result |
|---|---|
| Tests extracted | 4 / 4 |
| Listening parts | 16 / 16 (4 per test) |
| Listening questions | 160 / 160 |
| Reading passages | 12 / 12 |
| Reading questions | 160 / 160 |
| Writing tasks | 8 / 8 |
| Speaking parts | 12 / 12 |
| Answer keys | 320 / 320, checked against `meta/keys.json` |
| Listening transcripts | 16 / 16, every authored word found in the book audioscripts |
| Writing figures | 4 / 4 + Test 2 listening map |
| Listening audio | 16 parts, Kokoro generated from the extracted transcripts |
| Examiner audio | 52 clips, 13 per test |

No PDF test section was left out. The only book sections not wired into the mock engine are
ancillary: Introduction, Sample Writing answers, sample answer sheets and
Acknowledgements. Their text/images remain in `content/cambridge21/raw/` and `pages/`.

## Verification layers

1. **Answer keys.** Every authored `answer`/`accepted` value was compared with the book
   key parser output (including two-column fixups). Result: 320/320 match.
2. **Question text.** TFNG/YNNG statements, matching items, MCQ stems and options were
   normalized and checked for containment in the relevant book pages. Result: all
   in-book text found; the only non-contained strings are the intentionally prefixed
   Speaking topic labels and OCR-normalized spellings (`AI`, `Dar es Salaam`).
3. **Instructions.** Every group instruction has ≥90% token overlap with the book page;
   most are verbatim.
4. **Passages.** Every paragraph has ≥97% token overlap with the book passage pages.
   Known corrections: `Dares Salaam`, `UlbeBosma`, `Belferby`, `Sillicon`,
   `contemporaiy`, `·while`, footnote removal.
5. **Body prompts.** Every completion body line was checked against the book page; all
   note/table/summary lines are present. Test 4 Part 4 was re-checked after a metadata fix.
6. **API.** A full empty attempt was created for each test, all four sections submitted,
   and the review payload checked for 40+40 questions, transcripts, writing prompts and
   speaking parts. No answer key or transcript appears in the public exam payload.
7. **Assets.** All 16 listening parts and all four figures return HTTP 200 through the web
   proxy; file sizes are sane.

## Fixes made during this audit

| Issue | Fix |
|---|---|
| Test 4 Listening Part 4 still had the working title “Sleep and the elderly” and prompts “Sleep notes N” while the body was Music therapy | Retitled the part and prompts; rebuilt content |
| Test 2 Reading Passage 3 word list stopped at H; the book also offers “approval” as I | Added `I approval`, range text A–I |
| Test 2 Reading summary missed punctuation after two blanks | Restored full stops |
| Page map for Test 4 listening/reading and Test 3 reading was off by one page | Corrected in `extract.py` and the audit/guide maps |
| Test 2 listening Part 4 audio was generated before transcript margin-marker cleanup | Regenerated that part |
| Test 2 Writing Task 1 crop cut off the barbecue and outdoor seating | Recropped the plans to include the full ground floor |

The remaining fuzzy-audit findings are generic labels used only for internal navigation
(“The first point”, “The second feature”), not visible question content.

## Intentional differences and residual limitations

- Reading passages keep the book wording but correct OCR errors (`Cezanne` is left as the
  scanned spelling in places, `café` may appear as `cafe`).
- Listening tables are flattened into labelled rows with `{{n}}` blanks; the answer and
  wording are preserved, the multi-column layout is not.
- The book’s audioscripts are shorter than a full 30-minute recording; generated parts run
  about 3.7–5.8 minutes each.
- Glossary footnotes (e.g. *philanthropic*, *palisade*) are not rendered; the passage text
  is otherwise complete.
- Writing and Speaking scores remain local rubric estimates, not official IELTS results.

## Re-running the audit

```bash
cd /Users/tim2k/test/ielts-mock-lab
python3 content/cambridge21/tools/audit_fidelity.py
python3 content/cambridge21/tools/verify_pack.py
bash scripts/verify.sh
cd apps/web && pnpm exec playwright test --trace=off
```

---

# Addendum — IELTS 20 Academic pack

Audit date: 2026-11-12. Scope: the four seeded IELTS 20 Academic tests.

## Coverage

| Item | Result |
|---|---|
| Tests extracted | 4 / 4 |
| Listening parts / questions | 16 / 16 · 160 / 160 |
| Reading passages / questions | 12 / 12 · 160 / 160 |
| Writing tasks / Speaking parts | 8 / 8 · 12 / 12 |
| Answer keys | 320 / 320, transcribed from the inline key pages |
| Listening transcripts | 16 / 16, cleaned of page headers, footers and margin numbers |
| Figures | 4 Writing Task 1 figures + Test 3 listening map |
| Listening audio | 16 parts, Kokoro generated |
| Examiner audio | 52 clips, 13 per test |

## Checks

- `tools/score_check.py` submits a perfect attempt for every test through the API and
  asserts **40/40 Listening and 40/40 Reading**.
- `tools/audit_fidelity.py` compares every authored statement, option, passage paragraph,
  writing prompt and speaking question with the raw book pages. Result: **0 substantive
  mismatches**; the only findings were three generic completion prompt labels
  (“First thing Heather explains about kilns”, etc.) that do not quote the book.
- All 12 passages have 97–100% token overlap with the book text after footnote removal.
- Every completion group’s `{{n}}` blanks resolve to a question in the same group;
  `build_content.py` enforces this.

## Repaired source faults

- Test 1 Listening Q17–18 option letters D–H → A–E; Q19–20 heading duplication removed.
- Test 3 Reading Q22–23 option letters A–F → A–E; stray stem label removed.
- Test 1 Reading Passage 2 title reconstructed from “to Britain”.
- Transcript name/spelling fixes: Orley → Audley, temps → Thames, kil → kiln,
  £30 ahead → £30 a head.

## Residual limitations

- Listening scripts run 3–6 minutes per part, as printed in the book.
- Tables are rendered as labelled bullet rows rather than multi-column tables.
- Minor OCR spellings may remain in long passages; proper nouns were spot-checked.
- Sample answers, answer sheets and front matter are extracted but not wired into the app.
