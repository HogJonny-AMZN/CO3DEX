# Layer 3 · Fact check — Sonnet 5

Every load-bearing statistic, date, quotation and named source, checked. Runs before voice work because removing
or softening an unsupported claim rewrites sentences. Invoke `blog-factcheck` for its method; point it at the
sources the coordinator names — local files for a devblog memo, URLs for a post that cites the web.

## Inputs

- The draft.
- The sources: a source ledger and the files it cites, or the URLs the draft cites. Never a raw session log.
- The plan file.

## Output

- The draft, written back with fixes applied **only where the source says otherwise**. A claim with no source
  is marked `[unverified: ...]` for the author; that is a decision point, not an error.
- Appended to the plan file:

```text
## Layer 3 — Fact check (round r)

| # | Claim (quote) | Source | Verdict: verified · paraphrase · weak · not found · contradicted | Note |
| --- | --- | --- | --- | --- |

### Fixes applied
### Marked unverified
### Asserted from standing
- <claims the author can state flat as first-hand professional knowledge; a footnote here would read weaker
  than the assertion, and the citation count is over the corpus range>
```

## Rules

- Change nothing but facts and citation apparatus.
- Some claims are better uncited and asserted from standing. When the citation count is over the corpus range,
  propose which footnotes to drop on that basis; the author decides at Layer 9.
- A verbatim quotation must match its source character for character; fix the draft, not the source.
- Reply with the verdict counts, nothing else.
