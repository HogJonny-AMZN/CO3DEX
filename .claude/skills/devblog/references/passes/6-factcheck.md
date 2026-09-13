# Pass 6 · Fact-check — Sonnet 5

Every number, date, quotation and claim in the draft, checked against its ledger source. The sources are local
files, not web pages: invoke the `blog-factcheck` skill for its method (extract every load-bearing claim, match
it to its cited source, score the match) and point it at the files the coordinator names instead of URLs. Do not
fetch anything.

## Inputs

- The draft, with its `[^n]` footnotes.
- The source ledger from pass 1, which cites the files. When the ledger's text is not enough to settle a claim,
  open the cited file itself (journal, benchmark, ADR, rendered session text) at the path the coordinator gives
  for the source set. Never a raw `.jsonl`.

## Output

- The draft, written back to its path with fixes applied **only where the source says otherwise**: a wrong
  number, a misdated event, a quotation that differs from the source, a claim the source contradicts. Each fix
  is listed. A claim with no footnote gets one if the ledger supports it, or is marked in the draft with
  `[unverified: ...]` for the owner.
- A notes file at the second path the coordinator gives:

```text
# Fact-check — round <r>

| # | Claim (quote) | Footnote | Verdict | Note |
| --- | --- | --- | --- | --- |
| 1 | ... | [^3] | verified · paraphrase · weak · not found · contradicted | ... |

## Fixes applied
- <claim> — was "...", source says "...", now "..."

## Marked unverified
- ...

Verified n · paraphrase n · weak n · not found n · contradicted n
```

## Rules

- Change nothing but facts. Not a word of style, not a sentence's shape.
- A verbatim quotation must match its source character for character, typos included; fix the draft, not the
  source.
- A number's unit and what it measures are part of the number.
- If a source is private and the draft cites it by URL or absolute path, replace the citation with the ledger's
  stable identifier and list the fix.
- Reply with the verdict counts, nothing else.
