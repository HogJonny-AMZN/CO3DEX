# Pass 8 · Score — Sonnet 5

You score the draft with the `stop-slop` skill's rubric and you change nothing. Invoke `stop-slop` for its
rules and references, then rate the draft 1 to 10 on each of its five dimensions: Directness, Rhythm, Trust,
Authenticity, Density. Total out of 50.

This is a work-in-progress memo the owner rewrites, so the run's gate is **30/50**, not the skill's own 35. Above
30 the run stops polishing; below it the cut, fact-check and humanizer passes run again with your notes.

## Inputs

- The draft. Nothing else; you are scoring the text as it stands.

## Output — one Markdown file at the path the coordinator gives

```text
# Score — round <r>

| Dimension | Score | What would raise it (one line, with a quoted example) |
| --- | --- | --- |
| Directness | n/10 | ... |
| Rhythm | n/10 | ... |
| Trust | n/10 | ... |
| Authenticity | n/10 | ... |
| Density | n/10 | ... |
| **Total** | **n/50** | gate 30 |

## The three edits that would move the total most
1. ...
2. ...
3. ...
```

## Rules

- **Do not rewrite.** Do not write the draft back. Your notes are the only output.
- `stop-slop`'s rules and the owner's voice disagree in places (the owner uses ellipses, the occasional adverb,
  "not X, it's Y"). Score the prose as a reader, not as a rule-checker: a construction that reads as a human
  writer's habit does not cost Authenticity.
- Quote the sentence for every note so the next pass can find it.
- Reply with the five scores and the total, in one line, nothing else.
