# Academic content

The `cambridge21-test1.json` … `cambridge21-test4.json` files are the local seed pack for the four Cambridge IELTS 21 Academic tests. `test001.json` is the original Apex fallback content and is no longer embedded by the running API.

- Candidate-visible fields and answer keys are stored together here.
- The API strips `answer`, `accepted`, `explanation`, `transcript` and `modelAnswer` before sending content to the browser.
- Regenerate this file and the API embed copy with:

```bash
node --experimental-strip-types scripts/export-content.mjs
```

## Adding another exam

1. Obtain licensed or original content.
2. Add the exam to the typed content layer or create a new JSON definition using the same schema.
3. Extend the seed loader to publish each exam version.
4. Add audio under `apps/web/public/media/listening/<exam-id>/`.
5. Add the exam to the dashboard through `GET /exams`.

Do not add Cambridge IELTS passages, questions, images or recordings without written permission from the rights holder.
