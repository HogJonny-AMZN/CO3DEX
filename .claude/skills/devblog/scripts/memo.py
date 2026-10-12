#!/usr/bin/env python3
"""Assemble a devblog memo from the run folder: the draft first, the apparatus after it.

Usage::

    python memo.py DATE FROM TO --run .docs/devblog-run --out .docs/wip/devblog-DATE.md
                   --score "35/50 after 1 round" --tokens 1034935 [--note "..."]

Reads from the run folder: ``draft.md``, ``2-angle.md``, ``1-ledger.md``, ``4-reader.md``, the per-round
layer notes (``5-*.md`` … ``8-*.md`` or ``L1-*.md`` … ``L8-*.md``), ``cost.md``, ``sources/MANIFEST.md``,
``sources/commits.txt``. Writes one Markdown file. Standard library only.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

__version__ = "1.0.0"

HEADER_NOTE = (
    "Footnotes are breadcrumbs into a private repository (a journal file and heading, a commit, a benchmark, a "
    "session and time), for the owner to follow on their own machine; none is a link. Drop them when publishing."
)


# ----------------------------------------------------------------------------------------------------------------------
def demote(text: str) -> str:
    """Push every heading down two levels so a section's own headings nest under the memo's."""
    return re.sub(r"^(#+)", r"##\1", text, flags=re.MULTILINE)


# ----------------------------------------------------------------------------------------------------------------------
def tick_cited(ledger_table: str, draft: str) -> str:
    """Mark every ledger row the draft's footnotes cite (``ledger #k``) with a check."""
    cited = {int(k) for k in re.findall(r"ledger #(\d+)", draft)}
    rows = []
    for line in ledger_table.splitlines():
        m = re.match(r"\|\s*(\d+)\s*\|", line)
        if m and int(m.group(1)) in cited:
            line = line.replace(f"| {m.group(1)} |", f"| {m.group(1)} ✓ |", 1)
        rows.append(line)
    return "\n".join(rows), len(cited)


# ----------------------------------------------------------------------------------------------------------------------
def pass_notes(run: Path) -> list[tuple[str, str]]:
    """Every pass-note file in the run folder, in pipeline order, as (title, text)."""
    order = [
        ("4-reader.md", "Fresh reader"),
        *[(f"L{i}-{r}.md", f"Layer {i} · round {r}") for r in (1, 2, 3) for i in range(1, 9)],
        *[
            (f"{i}-{name}-{r}.md", f"Pass {i} · {name} · round {r}")
            for r in (1, 2, 3)
            for i, name in ((5, "cut"), (6, "facts"), (7, "humanizer"), (8, "score"))
        ],
    ]
    found = []
    for name, title in order:
        path = run / name
        if path.exists():
            found.append((title, path.read_text(encoding="utf-8").strip()))
    return found


# ----------------------------------------------------------------------------------------------------------------------
def build(
    run: Path, date: str, period_from: str, period_to: str, score: str, tokens: str, note: str | None
) -> tuple[str, int]:
    sources = run / "sources"
    journal = len(list((sources / "journal").glob("*.md"))) if (sources / "journal").exists() else 0
    sessions = len(list((sources / "sessions").glob("*.md"))) // 2 if (sources / "sessions").exists() else 0
    commits = (
        sum(1 for _ in (sources / "commits.txt").open(encoding="utf-8")) if (sources / "commits.txt").exists() else 0
    )
    n_files = (
        sum(1 for _ in (sources / "MANIFEST.md").open(encoding="utf-8")) if (sources / "MANIFEST.md").exists() else 0
    )
    draft = (run / "draft.md").read_text(encoding="utf-8").strip()
    angle = (run / "2-angle.md").read_text(encoding="utf-8").strip() if (run / "2-angle.md").exists() else ""
    ledger = (run / "1-ledger.md").read_text(encoding="utf-8") if (run / "1-ledger.md").exists() else ""
    m = re.search(r"## Entries\s*\n(.*?)(?=\n## )", ledger, re.DOTALL)
    table, cited = tick_cited(m.group(1).strip() if m else ledger, draft)
    cost = (run / "cost.md").read_text(encoding="utf-8").strip() if (run / "cost.md").exists() else "(not recorded)"
    notes = "\n\n".join(f"### {title}\n\n{text}" for title, text in pass_notes(run))
    lines = [
        f"# Devblog memo — {date}",
        "",
        HEADER_NOTE,
        "",
        f"Period {period_from} to {period_to} · {n_files} sources ({journal} journal files, {sessions} sessions, {commits} commits) · {score} · {tokens} tokens",
    ]
    if note:
        lines += ["", f"*{note}*"]
    lines += [
        "",
        "## Draft",
        "",
        demote(draft),
        "",
        "## Angle",
        "",
        demote(angle),
        "",
        "## Source ledger",
        "",
        "Entries the draft's footnotes cite are marked ✓.",
        "",
        table,
        "",
        "## Pass notes",
        "",
        demote(notes),
        "",
        "## Cost",
        "",
        cost,
        "",
    ]
    return "\n".join(lines), cited


# ----------------------------------------------------------------------------------------------------------------------
def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("date")
    parser.add_argument("period_from")
    parser.add_argument("period_to")
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--score", required=True)
    parser.add_argument("--tokens", required=True)
    parser.add_argument("--note")
    args = parser.parse_args(argv)
    memo, cited = build(args.run, args.date, args.period_from, args.period_to, args.score, args.tokens, args.note)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(memo, encoding="utf-8")
    print(f"{args.out}\t{len(memo.split())} words\t{cited} ledger entries cited")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
