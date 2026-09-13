"""Tests for scan_public.py: the pre-commit scan of every file the devblog generates."""

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
    escaped = (
        "kept as `D:" + "\\\\" + "Depot" + "\\\\" + "Thing` in a table"
    )  # D:\\Depot\\Thing, as Markdown escapes it
    assert [h.kind for h in sp.scan_text(escaped)] == ["absolute path"]
    assert sp.scan_text("see https://www.co3dex.com/ and at 17:08/day and 12:30/14:00") == []


# ----------------------------------------------------------------------------------------------------------------------
def test_other_roots_and_unc_shares_are_hits() -> None:
    text = (
        "wrote /tmp/x, /var/log/y, /workspace/repo/z, /mnt/d/w and " + "\\\\" + "server" + "\\" + "share" + "\\" + "f"
    )
    assert [h.kind for h in sp.scan_text(text)] == ["absolute path"] * 5
    assert sp.scan_text("a relative docs/journal/file.md and src/x/y.py and 1/2") == []


# ----------------------------------------------------------------------------------------------------------------------
def test_private_repo_urls_are_hits() -> None:
    hits = sp.scan_text(
        "https://github.com/HogJonny-AMZN/SpriteJammer/pull/25 and github.com/HogJonny-AMZN/devlog-sessions"
    )
    assert [h.kind for h in hits] == ["private repository URL"] * 2


# ----------------------------------------------------------------------------------------------------------------------
def test_emails_and_secrets_are_hits() -> None:
    hits = sp.scan_text(
        "mail me@example.com, token ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZabcdef012345, AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG"
    )
    assert sorted(h.kind for h in hits) == ["email address", "secret", "secret"]
    assert all(h.match == sp.SECRET_MARKER for h in hits if h.kind == "secret")
    assert not any("ghp_" in h.match or "wJalr" in h.match for h in hits)


# ----------------------------------------------------------------------------------------------------------------------
def test_private_key_block_spanning_lines_is_one_hit_at_its_first_line() -> None:
    text = "line one\nline two\n-----BEGIN RSA PRIVATE KEY-----\nMIIEow==\nAAAA\n-----END RSA PRIVATE KEY-----\nafter"
    hits = sp.scan_text(text)
    assert [(h.line, h.kind) for h in hits] == [(3, "secret")]


# ----------------------------------------------------------------------------------------------------------------------
def test_quoted_secret_with_spaces_is_one_hit() -> None:
    hits = sp.scan_text('password="my secret phrase" and then text')
    assert [h.kind for h in hits] == ["secret"]


# ----------------------------------------------------------------------------------------------------------------------
def test_main_reports_file_and_line_and_fails(tmp_path: Path, capsys) -> None:
    bad = tmp_path / "memo.md"
    bad.write_text("fine\nsee D:\\Depot\\x\n", encoding="utf-8")
    good = tmp_path / "ok.md"
    good.write_text("fine\n", encoding="utf-8")
    assert sp.main([str(good)]) == 0
    assert sp.main([str(bad), str(good), str(tmp_path / "absent.md")]) == 1
    out = capsys.readouterr().out
    assert "memo.md:2" in out and "absolute path" in out and "absent.md: missing" in out


# ----------------------------------------------------------------------------------------------------------------------
def test_no_hit_is_echoed_and_a_missing_file_fails(tmp_path: Path, capsys) -> None:
    hits = sp.scan_text("mail me@example.com at /home/someone and github.com/HogJonny-AMZN/SpriteJammer")
    assert [h.match for h in hits] == [sp.MARKERS[h.kind] for h in hits]
    assert sp.main([str(tmp_path / "absent.md")]) == 1
    out = capsys.readouterr().out
    assert "absent.md: missing" in out and "HALT" in out
