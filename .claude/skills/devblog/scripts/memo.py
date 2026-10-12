#!/usr/bin/env python3
"""Assemble a devblog memo from the run folder: the draft first, the apparatus after it.

Usage::

    python memo.py DATE FROM TO --run .docs/devblog-run --out .docs/wip/devblog-DATE.md
                   --score "35/50 after 1 round" --tokens 1034935 [--note "..."]

Reads from the run folder: ``draft.md``, ``2-angle.md``, ``1-ledger.md``, ``4-reader.md`` (the devblog's own
fresh-reader pass), ``EDIT-PLAN.md`` (the one store every editorial layer appends to), ``cost.md``,
``sources/MANIFEST.md``, ``sources/commits.txt``. Writes one Markdown file. Standard library only.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

__version__ = "1.1.0"

HEADER_NOTE = (
    "Footnotes are breadcrumbs into a private repository (a journal file and heading, a commit, a benchmark, a "
    "session and time), for the owner to follow on their own machine; none is a link. Drop them when publishing."
)


# ----------------------------------------------------------------------------------------------------------------------
def demote(text: str, levels: int = 2) -> str:
    """Push every Markdown heading down ``levels``, leaving fenced code blocks untouched."""
    out: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        elif not in_fence and line.startswith("#"):
            line = "#" * levels + line
        out.append(line)
    return "\n".join(out)


# ----------------------------------------------------------------------------------------------------------------------
def tick_cited(ledger_table: str, draft: str) -> tuple[str, int]:
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
def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip() if path.exists() else ""


# ----------------------------------------------------------------------------------------------------------------------
def _count_lines(path: Path) -> int:
    return sum(1 for _ in path.open(encoding="utf-8")) if path.exists() else 0


# ----------------------------------------------------------------------------------------------------------------------
def build(
    run: Path, date: str, period_from: str, period_to: str, score: str, tokens: str, note: str | None
) -> tuple[str, int]:
    sources = run / "sources"
    journal = len(list((sources / "journal").glob("*.md"))) if (sources / "journal").exists() else 0
    sessions = len(list((sources / "sessions").glob("*.md"))) // 2 if (sources / "sessions").exists() else 0
    commits = _count_lines(sources / "commits.txt")
    n_files = _count_lines(sources / "MANIFEST.md")
    draft = _read(run / "draft.md")
    angle = _read(run / "2-angle.md")
    ledger = _read(run / "1-ledger.md")
    m = re.search(r"## Entries\s*\n(.*?)(?=\n## )", ledger, re.DOTALL)
    table, cited = tick_cited(m.group(1).strip() if m else ledger, draft)
    cost = _read(run / "cost.md") or "(not recorded)"
    notes = []
    reader = _read(run / "4-reader.md")
    if reader:
        notes.append("# Fresh reader (devblog pass 4)\n\n" + reader)
    plan = _read(run / "EDIT-PLAN.md")
    if plan:
        notes.append(plan)
    lines = [
        f"# Devblog memo — {date}",
        "",
        HEADER_NOTE,
        "",
        f"Period {period_from} to {period_to} · {n_files} sources ({journal} journal files, {sessions} sessions, "
        f"{commits} commits) · {score} · {tokens} tokens",
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
        demote("\n\n".join(notes)),
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
