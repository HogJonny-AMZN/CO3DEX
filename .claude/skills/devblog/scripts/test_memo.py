"""Tests for memo.py: the memo puts the draft first and ticks the ledger rows the draft cites."""

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
    (run / "draft.md").write_text("# Title\n\n## Part one\n\nBody.[^1]\n\n[^1]: ledger #2 - src", encoding="utf-8")
    (run / "2-angle.md").write_text("# Angle\n\n## Beats\n\n1. x", encoding="utf-8")
    (run / "1-ledger.md").write_text(
        "# Ledger\n\n## Entries\n\n| # | Kind | Text | Source |\n| --- | --- | --- | --- |\n| 1 | q | a | s |\n| 2 | q | b | s |\n\n## Candidate angles\n\nnone\n",
        encoding="utf-8",
    )
    (run / "4-reader.md").write_text("# Fresh reader\n\nlost once", encoding="utf-8")
    (run / "L8-1.md").write_text("# Scorecard\n\n35/50", encoding="utf-8")
    (run / "cost.md").write_text("pass, round, tokens\n1, 1, 10\n", encoding="utf-8")
    return run


# ----------------------------------------------------------------------------------------------------------------------
def test_memo_draft_first_and_cited_rows_ticked(tmp_path: Path) -> None:
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
    assert "### Title" in text and "#### Part one" in text  # demoted under the memo's headings
    assert "2 sources (1 journal files, 0 sessions, 2 commits)" in text
    assert "Footnotes are breadcrumbs" in text
    assert "### Layer 8 · round 1" in text and "### Fresh reader" in text


# ----------------------------------------------------------------------------------------------------------------------
def test_main_writes_the_file(tmp_path: Path, capsys) -> None:
    run = _run(tmp_path)
    out = tmp_path / "wip" / "devblog-2026-09-13.md"
    assert (
        memo.main(
            [
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
        )
        == 0
    )
    assert out.exists() and "*v2*" in out.read_text(encoding="utf-8")
