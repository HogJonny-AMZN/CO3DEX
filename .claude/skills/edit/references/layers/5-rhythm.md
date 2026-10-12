# Layer 5 · Rhythm — Sonnet 5, after the script

Pure measurement, then pure paragraph breaks. **Zero word changes.** The coordinator has run
`measure.py rhythm` and `measure.py words` and gives you both outputs; it runs `words` again when you are done,
and the fingerprint must match.

## Inputs

- The draft.
- The rhythm map: every paragraph's word count in order, the flat runs (three or more consecutive paragraphs
  over 120 words), the isolation candidates (a paragraph of 100 or more words ending in a sentence under 25).
- `BASELINES.md`: the corpus's paragraph mass and its ratio of short paragraphs.

## What to do

1. In each flat run, find the seam that is already there and break it. Do not create one.
2. For an isolation candidate, the short verdict sentence already sits at the end; the weight in front of it is
   what earns the break. Break only where the weight is there. A one-line paragraph after 200 words of build
   works; after 20 words it reads choppy.
3. **Dosage.** Target the corpus ratio of short paragraphs. Isolating every punch destroys the contrast that
   makes the technique work.

## Output

- The draft, written back, with paragraph breaks moved and nothing else.
- Appended to the plan file:

```text
## Layer 5 — Rhythm (round r)

Breaks added: <n> at paragraphs <list> · breaks removed: <n> · fingerprint before = after: <yes>
Paragraph mass: <mean before> → <mean after> (corpus <range>)
```

## Rules

- Not one word changes. Not a comma. The fingerprint check is the gate.
- Reply with the breaks added and removed, nothing else.
