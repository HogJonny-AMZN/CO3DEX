"""Tests for session_text.py — run with ``uv run --with pytest pytest .claude/skills/devblog/scripts/``."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import session_text as st


# ----------------------------------------------------------------------------------------------------------------------
def _record(kind: str, content, *, ts: str = "2026-09-06T17:08:41.133Z", **extra) -> str:
    """One session record as a JSON line."""
    rec = {"type": kind, "timestamp": ts, "message": {"role": kind, "content": content}}
    rec.update(extra)
    return json.dumps(rec)


# ----------------------------------------------------------------------------------------------------------------------
def _write(tmp_path: Path, lines: list[str]) -> Path:
    path = tmp_path / "abcd1234-0000-0000-0000-000000000000.jsonl"
    path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    return path


# ----------------------------------------------------------------------------------------------------------------------
def test_tool_call_and_result_are_omitted(tmp_path: Path) -> None:
    lines = [
        _record("user", "Build the thing."),
        _record(
            "assistant",
            [
                {"type": "thinking", "thinking": "private reasoning"},
                {"type": "tool_use", "id": "t1", "name": "Bash", "input": {"command": "ls"}},
            ],
        ),
        _record("user", [{"type": "tool_result", "tool_use_id": "t1", "content": "file.py"}]),
        _record("assistant", [{"type": "text", "text": "Built it."}]),
    ]
    doc = st.render(st.iter_turns(_write(tmp_path, lines)), "abcd1234")
    assert "Build the thing." in doc
    assert "Built it." in doc
    assert "file.py" not in doc
    assert "private reasoning" not in doc
    assert "Bash" not in doc and "tool_use" not in doc


# ----------------------------------------------------------------------------------------------------------------------
def test_secrets_and_emails_are_redacted(tmp_path: Path) -> None:
    reply = (
        "Use token ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZabcdef012345 and mail someone@example.com; "
        "also AKIAABCDEFGHIJKLMNOP and password=hunter2secret and xoxb-1234567890-abcdefghij"
    )
    lines = [_record("user", "hi"), _record("assistant", [{"type": "text", "text": reply}])]
    doc = st.render(st.iter_turns(_write(tmp_path, lines)), "abcd1234")
    assert "ghp_" not in doc
    assert "example.com" not in doc
    assert "AKIA" not in doc
    assert "hunter2secret" not in doc
    assert "xoxb-" not in doc
    assert doc.count(st.REDACTED) >= 5


# ----------------------------------------------------------------------------------------------------------------------
def test_private_key_block_is_redacted() -> None:
    text = "before\n-----BEGIN RSA PRIVATE KEY-----\nMIIEow==\n-----END RSA PRIVATE KEY-----\nafter"
    out = st.redact(text)
    assert "MIIEow" not in out
    assert out.startswith("before") and out.endswith("after")


# ----------------------------------------------------------------------------------------------------------------------
def test_empty_file_renders_empty_document(tmp_path: Path) -> None:
    doc = st.render(st.iter_turns(_write(tmp_path, [])), "abcd1234")
    assert doc.startswith("# Session abcd1234")
    assert "## " not in doc


# ----------------------------------------------------------------------------------------------------------------------
def test_sidechain_meta_and_non_message_records_are_skipped(tmp_path: Path) -> None:
    lines = [
        json.dumps({"type": "bridge-session", "sessionId": "x"}),
        _record("user", "subagent prompt", isSidechain=True),
        _record("assistant", [{"type": "text", "text": "subagent reply"}], isSidechain=True),
        _record("user", "meta line", isMeta=True),
        _record("user", "real prompt"),
        "not json at all",
    ]
    turns = list(st.iter_turns(_write(tmp_path, lines)))
    assert [t.text for t in turns] == ["real prompt"]


# ----------------------------------------------------------------------------------------------------------------------
def test_harness_tags_are_stripped_from_prompts() -> None:
    text = (
        "<ide_opened_file>The user opened x</ide_opened_file>Hello there\n"
        "<system-reminder>\nstuff\n</system-reminder>\nmore"
    )
    assert st.clean(text) == "Hello there\nmore"


# ----------------------------------------------------------------------------------------------------------------------
def test_render_carries_timestamps_and_roles(tmp_path: Path) -> None:
    lines = [_record("user", "q", ts="2026-09-06T17:08:41.133Z"), _record("assistant", [{"type": "text", "text": "a"}])]
    doc = st.render(st.iter_turns(_write(tmp_path, lines)), "abcd1234")
    assert "## 2026-09-06 17:08 · owner" in doc
    assert "## 2026-09-06 17:08 · assistant" in doc


# ----------------------------------------------------------------------------------------------------------------------
def test_stats_re_derive_the_design_figures(tmp_path: Path) -> None:
    lines = [
        _record("user", "mail a@b.co and c@d.org"),
        _record("assistant", [{"type": "text", "text": "AKIAABCDEFGHIJKLMNOP a@b.co"}]),
    ]
    path = _write(tmp_path, lines)
    stats = st.stats(path)
    assert stats.raw_bytes == path.stat().st_size
    assert stats.text_bytes == len("mail a@b.co and c@d.org") + len("AKIAABCDEFGHIJKLMNOP a@b.co")
    assert stats.secret_matches == 1
    assert stats.distinct_emails == 2


# ----------------------------------------------------------------------------------------------------------------------
def test_main_writes_one_markdown_per_session(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = _write(tmp_path, [_record("user", "hello"), _record("assistant", [{"type": "text", "text": "hi"}])])
    out = tmp_path / "out"
    assert st.main([str(path), "--out", str(out)]) == 0
    written = list(out.glob("*.md"))
    assert len(written) == 1 and written[0].stem == path.stem
    assert "hello" in written[0].read_text(encoding="utf-8")


# ----------------------------------------------------------------------------------------------------------------------
def test_role_filter_keeps_one_side(tmp_path: Path) -> None:
    path = _write(tmp_path, [_record("user", "hello"), _record("assistant", [{"type": "text", "text": "hi"}])])
    assert [t.role for t in st.iter_turns(path, "owner")] == ["owner"]
    assert [t.role for t in st.iter_turns(path, "assistant")] == ["assistant"]
    assert [t.role for t in st.iter_turns(path)] == ["owner", "assistant"]


# ----------------------------------------------------------------------------------------------------------------------
def test_secret_assignments_with_affixes_are_redacted() -> None:
    out = st.redact(
        "AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG and my_api_key: abcdef123456 and token_value=xyz789012"
    )
    assert "wJalrXUtnFEMI" not in out and "abcdef123456" not in out and "xyz789012" not in out
    assert out.count(st.REDACTED) == 3
    assert (
        st.redact("the token bucket refills, secret sauce, password reset")
        == "the token bucket refills, secret sauce, password reset"
    )


# ----------------------------------------------------------------------------------------------------------------------
def test_quoted_secret_values_with_spaces_redact_whole() -> None:
    out = st.redact("password=\"my secret phrase\" then api_key: 'another long one' end")
    assert "secret phrase" not in out and "another long" not in out
    assert out == f"{st.REDACTED} then {st.REDACTED} end"


# ----------------------------------------------------------------------------------------------------------------------
def test_stats_skip_the_records_the_render_skips_and_total_unions_emails(tmp_path: Path, capsys) -> None:
    a = _write(tmp_path, [_record("user", "x@y.io"), _record("user", "hidden z@w.io", isSidechain=True)])
    b = tmp_path / "second.jsonl"
    b.write_text(_record("assistant", [{"type": "text", "text": "again x@y.io"}]) + "\n", encoding="utf-8")
    assert st.stats(a).distinct_emails == 1 and st.stats(a).text_bytes == len("x@y.io")
    assert st.main([str(a), str(b), "--stats"]) == 0
    last = capsys.readouterr().out.strip().splitlines()[-1]
    assert last.startswith("TOTAL") and last.endswith("emails 1 distinct")
