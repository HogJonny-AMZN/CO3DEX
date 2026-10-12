# Layer 4 · Voice — Fable 5.1

`humanizer`, then `stop-slop`, both fed the author's profile. Without the profile both default to generic
de-slopping and flatten the author into clipped staccato, which is as wrong as leaving them formal.

## Inputs

- The draft.
- `VOICE.md`: the described habits and the ground-truth samples named in `BASELINES.md` (the `_ORIGINAL` files
  in `.docs/wip/`), which outrank any recent AI-assisted post.
- The plan file.

## Watch for

- **Punctuation fingerprints that give away a revision.** Em dashes clustered in exactly the newly written
  paragraphs; curly apostrophes where the rest is straight. Two hands visible in one file.
- **Participle clauses doing fake depth**: "...ing X, ensuring Y". The most common remaining tell.
- **Register drift.** One section contracting freely, another switching to "it is / cannot / do not".
- **Warm-up sentences.** "I should disclose something up front" announces instead of doing.
- **The lesson landing.** A section that ends on a portable rule because the structure asked for one. The
  author lands on a verdict or an image, rarely a rule.

## Output

- The draft, written back.
- Appended to the plan file:

```text
## Layer 4 — Voice (round r)

| Pattern | Count | Example before → after |
| --- | --- | --- |

### Left alone on purpose
- <a flagged construction the author's samples actually use, with the sample that shows it>

Words: <before> → <after>
```

## Rules

- Contract **selectively**. Flat formality earns its place where the line is a verdict. Quoted material is
  never touched.
- Numbers, dates, footnotes and quotations do not change. Structure does not change; if it must, stop and say
  so, and the coordinator goes back to Layer 1.
- No em dashes of your own.
- Reply with the pattern count, nothing else.
