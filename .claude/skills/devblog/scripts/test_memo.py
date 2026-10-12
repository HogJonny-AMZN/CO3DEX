"""Tests for memo.py: the memo puts the draft first, ticks the cited ledger rows, carries the plan file whole."""

from __future__ import annotations

from pathlib import Path

import memo


# ----------------------------------------------------------------------------------------------------------------------
def _run(tmp_path: Path) -> Path:
    run = tmp_path / "run"
    (run / "sources" / "journal").mkdir(parents=True)
    (run / "sources" / "journal" / "a.md").write_text("j", encoding="utf-8")
    (run / "sources" / "commits.txt").write_text("c1\nc2\n", encoding="utf-8")
    (run / "sources" / "MANIFEST.md").write_text("1\tx\n2\ty\n", encoding="utf-8")
    (run / "draft.md").write_text(
        "# Title\n\n## Part one\n\nBody.[^1]\n\n```sh\n# not a heading\nmake check\n```\n\n[^1]: ledger #2 - src",
        encoding="utf-8",
    )
    (run / "2-angle.md").write_text("# Angle\n\n## Beats\n\n1. x", encoding="utf-8")
    (run / "1-ledger.md").write_text(
        "# Ledger\n\n## Entries\n\n| # | Kind | Text | Source |\n| --- | --- | --- | --- |\n| 1 | q | a | s |\n| 2 | q | b | s |\n\n## Candidate angles\n\nnone\n",
        encoding="utf-8",
    )
    (run / "4-reader.md").write_text("# Fresh reader\n\nlost once", encoding="utf-8")
    (run / "EDIT-PLAN.md").write_text(
        "# Edit plan\n\n## Round 1 — measured\n\nnumbers\n\n## Layer 8 — Scorecard (round 1)\n\n35/50", encoding="utf-8"
    )
    (run / "cost.md").write_text("pass, round, tokens\n1, 1, 10\n", encoding="utf-8")
    return run


# ----------------------------------------------------------------------------------------------------------------------
def test_demote_leaves_code_fences_alone() -> None:
    text = "# H1\n\n```python\n# a comment\n#!/usr/bin/env python3\n```\n\n## H2"
    out = memo.demote(text)
    assert out.splitlines()[0] == "### H1" and out.splitlines()[-1] == "#### H2"
    assert "\n# a comment\n" in out and "\n#!/usr/bin/env python3\n" in out


# ----------------------------------------------------------------------------------------------------------------------
def test_memo_draft_first_cited_rows_ticked_plan_whole(tmp_path: Path) -> None:
    text, cited = memo.build(
        _run(tmp_path), "2026-09-13", "2026-09-06", "2026-09-13", "35/50 after 1 round", "10", None
    )
    assert cited == 1
    assert (
        text.index("## Draft")
        < text.index("## Angle")
        < text.index("## Source ledger")
        < text.index("## Pass notes")
        < text.index("## Cost")
    )
    assert "| 2 ✓ |" in text and "| 1 |" in text
    assert "### Title" in text and "#### Part one" in text  # the draft's headings nest under the memo's
    assert "\n# not a heading\n" in text  # the draft's code fence survived demotion
    assert "2 sources (1 journal files, 0 sessions, 2 commits)" in text
    assert "Footnotes are breadcrumbs" in text
    assert "### Fresh reader (devblog pass 4)" in text
    assert "### Edit plan" in text and "#### Layer 8 — Scorecard (round 1)" in text  # the plan file, whole, nested


# ----------------------------------------------------------------------------------------------------------------------
def test_main_writes_the_file(tmp_path: Path, capsys) -> None:
    run = _run(tmp_path)
    out = tmp_path / "wip" / "devblog-2026-09-13.md"
    args = [
        "2026-09-13",
        "2026-09-06",
        "2026-09-13",
        "--run",
        str(run),
        "--out",
        str(out),
        "--score",
        "35/50",
        "--tokens",
        "10",
        "--note",
        "v2",
    ]
    assert memo.main(args) == 0
    assert out.exists() and "*v2*" in out.read_text(encoding="utf-8")
