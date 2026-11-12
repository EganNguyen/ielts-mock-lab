# Scoring

## Listening and Reading
Raw answers are compared after case, whitespace and punctuation normalization, plus configured accepted alternatives and leading-article tolerance. Raw /40 is converted using the versioned public-style table in `services/api/internal/scoring/scoring.go`.

These tables are test-versioned (`scoring.listeningVersion`, `scoring.readingVersion`) and should be recalibrated when new content is authored.

## Writing
Task 1 and Task 2 are evaluated separately on four criteria:
- Task achievement / response
- Coherence and cohesion
- Lexical resource
- Grammatical range

Task 2 is weighted twice Task 1. The local provider measures word counts, paragraphing, linking, lexical diversity, sentence variety, overview presence, both-view discussion and opinion markers. It produces criterion bands and actionable feedback.

**This is an indicative local rubric, not an official IELTS examiner score.**

## Speaking
The local estimate uses prompt completion, recorded duration, transcript word count (when browser speech recognition is available) and words per minute. It is labelled completion-based and cannot assess pronunciation reliably.

**This is not an official IELTS Speaking score.**

## Overall
Overall = arithmetic mean of the four section bands, rounded to the nearest half band. Raw objective scores and the unrounded internal values remain available in the stored result details.
