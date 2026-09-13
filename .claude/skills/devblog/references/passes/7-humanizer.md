# Pass 7 · Humanizer — Fable 5.1

The last rewrite, and the most voice-sensitive. Invoke the `humanizer` skill on the draft with the three
excerpts in `VOICE.md`'s *Three samples* section as the voice sample, and apply it in the owner's voice: the
patterns it flags come out, and what replaces them is how the owner would have said it, not a neutral sentence.

## Inputs

- The draft.
- `VOICE.md`: the described habits and the three samples. Read it before the draft.
- On a second or third round: the scorer's notes from pass 8.

## Output

- The draft, written back to its path (overwrite).
- A notes file at the second path the coordinator gives:

```text
# Humanizer — round <r>

## Patterns found and what replaced them
| Pattern (humanizer's name) | Count | Example before → after |
| --- | --- | --- |

## Left alone on purpose
- <a flagged construction the owner's voice actually uses, with the VOICE.md line that says so>

Words: <before> → <after>
```

## Rules

- Footnotes stay attached to their claims. Numbers, dates and verbatim quotations do not change.
- The owner's habits in `VOICE.md` outrank the skill's defaults where they conflict: the ellipsis, the
  "not X, it's Y" contrast when the owner uses it, the aside, the sentence-long heading. When the skill flags
  one of those, leave it and note it.
- No em dashes. No rule-of-three lists that were not there. No new summary or closing line.
- No absolute paths, URLs into private repositories, or email addresses.
- Reply with the total count of patterns changed, nothing else.
