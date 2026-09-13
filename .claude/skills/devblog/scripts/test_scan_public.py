"""Tests for scan_public.py — the pre-commit scan of every file the devblog generates."""

from __future__ import annotations

from pathlib import Path

import scan_public as sp


# ----------------------------------------------------------------------------------------------------------------------
def test_clean_text_has_no_hits() -> None:
    text = "Read journal/2026-09-06-project-kickoff.md, commit 2fc6100, at 17:08 on https://www.co3dex.com/blog/x/."
    assert sp.scan_text(text) == []


# ----------------------------------------------------------------------------------------------------------------------
def test_absolute_paths_are_hits() -> None:
    hits = sp.scan_text("see D:\\Depot\\Thing\\file.md and C:/Users/someone/x and /home/someone/y and /Users/z/w")
    assert [h.kind for h in hits] == ["absolute path"] * 4


# ----------------------------------------------------------------------------------------------------------------------
def test_doubled_backslash_drive_is_a_hit_and_url_scheme_is_not() -> None:
    assert [h.kind for h in sp.scan_text("kept as `D:\\Depot\\Thing` in a table")] == ["absolute path"]
    assert sp.scan_text("see https://www.co3dex.com/ and at 17:08/day") == []


# ----------------------------------------------------------------------------------------------------------------------
def test_private_repo_urls_are_hits() -> None:
    hits = sp.scan_text(
        "https://github.com/HogJonny-AMZN/SpriteJammer/pull/25 and github.com/HogJonny-AMZN/devlog-sessions"
    )
    assert [h.kind for h in hits] == ["private repository URL"] * 2


# ----------------------------------------------------------------------------------------------------------------------
def test_emails_and_secrets_are_hits() -> None:
    hits = sp.scan_text("mail me@example.com, token ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZabcdef012345")
    assert sorted(h.kind for h in hits) == ["email address", "secret"]


# ----------------------------------------------------------------------------------------------------------------------
def test_main_reports_file_and_line_and_fails(tmp_path: Path, capsys) -> None:
    bad = tmp_path / "memo.md"
    bad.write_text("fine\nsee D:\\Depot\\x\n", encoding="utf-8")
    good = tmp_path / "ok.md"
    good.write_text("fine\n", encoding="utf-8")
    assert sp.main([str(good)]) == 0
    assert sp.main([str(bad), str(good)]) == 1
    out = capsys.readouterr().out
    assert "memo.md:2" in out and "absolute path" in out
