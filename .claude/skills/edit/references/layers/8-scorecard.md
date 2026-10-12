# Layer 8 · Scorecard — Sonnet 5, after the script

Every score cites the measurement that produced it. The coordinator has run `measure.py scorecard` and
`measure.py draft` and gives you both; the numbers are yours to cite, not to re-estimate.

## Inputs

- The draft.
- The measured half: AI vocabulary count, em dashes, paragraph mass against the corpus, participle tells,
  citation density against the corpus, register drift across sections, body length against the corpus.
- `stop-slop`, invoked for its five-dimension rubric; its total is one row here, gate 35.
- The plan file, with earlier rounds' scorecards.

## Output — appended to the plan file

```text
## Layer 8 — Scorecard (round r)

| Dimension | Score /10 | History | Measurement cited |
| --- | --- | --- | --- |
| AI vocabulary | | 8.5 → 8.8 | <n> words in <k> body words |
| Em dash discipline | | | <n>, corpus <range> |
| Voice fingerprint | | | <which samples it matches, which it does not> |
| Formatting tells | | | <lists, bold labels, headers as labels> |
| Register consistency | | | drift <x> across <n> sections |
| Negative parallelism | | | <count of "not X, it's Y" and whether they carry a distinction> |
| Rhythm | | | mass <mean>, corpus <range>; short-paragraph ratio |
| Personality | | | <where the author is present as a person, not a narrator> |
| Opening hook | | | <which paragraph the real hook is in> |
| Structural clarity | | | <sections, one argument each?> |
| Thesis consistency | | | <competing theses found> |
| Argument integrity | | | <Layer 7 findings, if run> |
| Ending | | | <fires once?> |
| Evidence texture | | | <citations n, corpus <range>; asserted-from-standing count> |
| Emotional pulse | | | <where the reader feels something, quoted> |
| stop-slop total | /50 | | gate 35 |

**Gates (numbers):** body words <in/OUT>, words per paragraph <in/OUT>, citations <in/OUT>, stop-slop <≥35?>.
**Length trend:** <words by round>.
**Flat across three passes:** <dimensions, named as structural trades, not defects>.
```

## Rules

- A dimension that has not moved across three passes is a structural trade. Say so and stop trying to fix it.
- Track total length as a trend even though it is not a scored dimension; drafts grow in every pass unless
  someone is watching.
- You change nothing in the draft.
- Reply with the four gate verdicts and the stop-slop total in one line, nothing else.
