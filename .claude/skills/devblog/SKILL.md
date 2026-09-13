---
name: devblog
description: Draft a weekly WIP memo about the SpriteJammer project for this blog — an angle, a source ledger and a rough first-person draft run through eight fresh-eyes writing passes — and open a pull request with it. Use when the user says "/devblog", "devblog", "draft this week's post", "the Sunday memo", or "first post". Never publishes; touches nothing in _posts/, _drafts/ or _authors/.
argument-hint: "[first] [--since YYYY-MM-DD] [--no-pr] [--dry]"
user-invokable: true
---

# devblog — the weekly memo

You are the **coordinator**. You run on Sonnet 5 and you write no prose: you read the continuity files, gather
the sources, run eight passes as fresh subagents on the models below, loop the last four to a score, write one
memo, scan it, and put it on a branch with a pull request. The owner rewrites the memo into a post. The design,
with every decision and its reason, is `docs/design/devblog.md` in the SpriteJammer repository.

## Settings — edit by hand

| Setting | Local (the owner's PC) | Cloud (increment 4, not yet) |
| --- | --- | --- |
| `SPRITEJAMMER` | `D:\Depot\SpriteJammer` | the SpriteJammer clone path |
| `SESSION_ROOT` | `~/.claude/projects` — session folders whose names contain `SpriteJammer` | the `devlog-sessions` clone (increment 1); until it exists a cloud run has no session logs **and says so at the top of the memo** |
| `PROJECT_START` | `2026-09-06` — the first prompt, session `872aa807`, 17:08 | same |
| `RUN_DIR` | `.docs/devblog-run/` — intermediates, git-ignored by `.docs/*`; wiped at the start of each run | same |

## Interface

```text
/devblog                      the weekly run: period = the day after the last ledger entry's period, to today
/devblog first                the first post: period = PROJECT_START to today; creates timeline.md and ledger.md
/devblog --since YYYY-MM-DD   an explicit period start
/devblog --no-pr              commit on the branch, open no pull request
/devblog --dry                run the passes and write the memo only; touch neither continuity file nor git
/devblog --brief "..."        a one-off brief for this post, on top of the open notes in next.md
```

## Models per pass

Pass the `model` to the Agent tool exactly as written. Every pass is a **fresh** subagent that gets its pass file,
the files it needs and the previous pass's output, and nothing else. Passes never see each other's reasoning.

| Pass | File | `model` |
| --- | --- | --- |
| 1 Research | `references/passes/1-research.md` | `sonnet` |
| 2 Angle check | `references/passes/2-angle.md` | `opus` |
| 3 Draft | `references/passes/3-draft.md` | `fable` |
| 4 Fresh reader | `references/passes/4-fresh-reader.md` | `sonnet` |
| 5 Cut | `references/passes/5-cut.md` | `opus` |
| 6 Fact-check | `references/passes/6-factcheck.md` | `sonnet` |
| 7 Humanizer | `references/passes/7-humanizer.md` | `fable` |
| 8 Score | `references/passes/8-score.md` | `sonnet` |

## The run, in order

Today's date is `DATE` (`YYYY-MM-DD`). All paths below are relative to this repository's root.

### 1 · Read continuity

Read `.docs/wip/devblog/ledger.md`, `.docs/wip/devblog/timeline.md` and `.docs/wip/devblog/next.md`. On `first`,
or when a file is missing, treat it as empty; the first two are created in step 5. **`next.md` is the owner's
queue**: dated notes, in their words, on what coming posts should be ("more technical", "the horde swarm
story"). Its open notes, plus `--brief` if given, are the brief for passes 1 and 2. The owner edits it by hand;
the coordinator only marks notes used. Otherwise the period starts the day after the last entry's
`Period:` end, or at `--since`. The period ends today.

### 2 · Gather the source set into `RUN_DIR/sources/`

Wipe `RUN_DIR`, then:

- Copy from `SPRITEJAMMER`: every `docs/journal/*.md` whose date (the filename's first ten characters) falls in
  the period, plus any journal file a `**Continued in:**` chain reaches; `docs/handoffs/CURRENT.md`;
  `docs/plan/BOARD.md`; `docs/decisions/README.md`; `docs/research/benchmarks/` (the whole folder, they are
  short); `docs/standards/failure-modes.md`; `docs/glossary.md`.
- The commit log: `git -C SPRITEJAMMER log --format='%h %ad %s' --date=short --since=<period start> --until=<period end plus one day>` into `sources/commits.txt`.
- The sessions: every `*.jsonl` under `SESSION_ROOT`'s SpriteJammer folders whose first `timestamp` falls in the
  period or before its end and whose last falls in or after its start, **rendered by**
  `scripts/session_text.py` — once in full and once with `--role owner` — into `sources/sessions/`. Skip the
  session that is running you (its id is in your own scratchpad path). **No pass ever reads a raw `.jsonl`.**
- LargeWorlds and Job_Orchestrator: only if a journal file in the period names them, and then only their
  `docs/` folder and commit log, the same way.

Write `sources/MANIFEST.md`: one line per file with its size, so the memo can count its sources.

### 3 · Run passes 1 to 4

For each pass, send the Agent tool one message that contains: the pass file's full text; the absolute paths of
its inputs (the source set, the reference files it names, the previous pass's output); the absolute path(s) it
must write; the period; and, for passes 2 and 3, the owner's brief when there is one. For pass 3, the length:
target 3,000–6,000 words, hard ceiling 12,549 (the longest 2026 post). For `first`, the brief is the owner's:

> A human story, from the very first prompt, telling how a 2.5D metroidvania became a horde survivors-like
> research project — but most important, how the repository was set up AI-first: docs as managed context, the
> journal, the board and its gates, the autonomy protocol, failure modes, measurement over estimate — because
> that is what made it a good research project. Told to a smart reader who is not technical or AI-savvy, as:
> here is what I did differently, here is how it worked out or failed, and this is worth trying yourself.

Outputs, all under `RUN_DIR`: `1-ledger.md`, `2-angle.md`, `draft.md`, `4-reader.md`. After each pass, record
the token count the Agent result reports, in `RUN_DIR/cost.md`, as `pass, round, tokens`.

### 4 · Loop passes 5 to 8

Round `r` = 1, 2, 3:

- Pass 5 rewrites `draft.md` in place and writes `5-cut-r.md`; on round 2+ it also gets `8-score-(r-1).md`.
- Pass 6 rewrites `draft.md` in place (facts only) and writes `6-facts-r.md`.
- Pass 7 rewrites `draft.md` in place and writes `7-humanizer-r.md`; on round 2+ it also gets `8-score-(r-1).md`.
- Pass 8 writes `8-score-r.md` and **changes nothing**. Read its total.

Total ≥ 30/50: stop looping. Total < 30 and r < 3: next round. Total < 30 after round 3: **halt** — locally,
write the memo (step 5) with `HALTED` in its header, touch neither continuity file nor git, print the three
rounds' scores and ask the owner to revise. In the cloud, commit and open the pull request titled
`revision request: devblog DATE` with the scores in its body.

### 5 · Write the memo and the continuity files

`.docs/wip/devblog-DATE.md`:

```text
# Devblog memo — DATE
Footnotes are breadcrumbs into a private repository (a journal file and heading, a commit, a benchmark, a
session and time), for the owner to follow on their own machine; none is a link. Drop them when publishing.
Period FROM to TO · N sources (J journal files, S sessions, C commits) · score T/50 after R round(s) · K tokens
(a cloud run with no session export: "Drafted from the journal alone; the session export was older than this
run.")

## Angle              2-angle.md, whole
## Draft              draft.md, whole, footnotes included
## Source ledger      1-ledger.md's Entries table, with a ✓ on every entry the draft's footnotes cite
## Pass notes         2, 4, then per round 5, 6, 7, 8, each under its own heading, in order
## Cost               tokens per pass per round, and the total
```

Unless `--dry`: append to `ledger.md` (create with a `# Devblog ledger` header on `first`):

```text
## DATE — <the chosen angle's one line>
Period: FROM to TO · Memo: .docs/wip/devblog-DATE.md · Post: (none yet)
Brief: <the next.md notes and --brief this memo answered, quoted; "none" if none>
Covered: <the ground the draft covers, as short claims, from the beats>
Terms explained: <glossary words the draft explained, from pass 4's table and the draft>
Claims: <every number and dated assertion in the draft, each with its ledger source>
Links: <earlier posts the draft linked, by permalink; "none" on first>
```

and extend `timeline.md` (create with `# SpriteJammer timeline` on `first`) with pass 1's *Timeline entries*,
merged into date order, no duplicates. The owner edits `Post:` when a post publishes. In `next.md`, each open
note the memo answered gets ` — used by devblog-DATE` appended; the note stays, so the record shows what was
asked and when it was answered. Notes the memo did not answer stay open.

### 6 · Scan, then git

Run `python .claude/skills/devblog/scripts/scan_public.py` on the memo, `ledger.md` and `timeline.md` (on
`--dry` the memo alone, since the continuity files were not written; a missing file is reported and skipped,
never a hit). **Any hit halts the run before anything is added**: print the hits and stop. Then, unless `--dry`:

1. `git switch -c claude/devblog-DATE main` (the branch is created from `main`; the untracked memo and
   continuity files come along).
2. `git add` exactly the three files, plus `next.md` when a note was marked used. Nothing under `_posts/`, `_drafts/` or `_authors/` is ever staged.
3. Commit with a message file (`git commit -F <file>`, never a pipe): title `devblog: memo DATE — <angle>`, body
   the period, sources and score. **Commit as the owner's identity with no AI attribution** — no
   `Co-Authored-By`, no "Generated with".
4. Unless `--no-pr`: `git push -u origin claude/devblog-DATE`, then `gh pr create --title "devblog: memo DATE"
   --body-file <file>` whose body opens with the angle's one line and the beats, then the scores as a table, then
   the cost line. No attribution footer.
5. Print the pull request URL and the scores. Then `gh pr checks --watch`.

### 7 · Record cost

The memo's *Cost* section is the design's one open measurement. Report it in your final message too.

## Gates, restated

- Private in, public out, fail-closed. Cite by stable identifiers; quote only redacted session text and
  committed docs; no raw `.jsonl` reaches a pass; scan before commit; a hit halts.
- Every pass is a fresh subagent on its assigned model.
- `stop-slop` scores; it never rewrites. Gate 30/50; three rounds; then halt.
- The memo touches nothing in `_posts/`, `_drafts/` or `_authors/`.
- Footnotes and citations are breadcrumbs, never links: the sources are private.
- No AI attribution anywhere.
