#!/usr/bin/env python3
"""Render a Claude Code session ``.jsonl`` as redacted Markdown: prompts and replies, nothing else.

Usage::

    python session_text.py <session.jsonl>... [--out DIR]     # one Markdown file per session (stdout without --out)
    python session_text.py <session.jsonl>... --role owner     # the owner's prompts only — the human story, small
    python session_text.py <session.jsonl>... --stats          # raw bytes, text bytes, secret matches, emails

What is kept: each ``user`` text prompt and each ``assistant`` text reply, in order, with a timestamp.
What is dropped: tool calls, tool results, thinking, subagent side-chains, meta records, harness tags such
as ``<system-reminder>`` and ``<ide_opened_file>``, and every record that is not a message.
What is redacted: token-shaped strings (GitHub, Slack, AWS, Anthropic/OpenAI-style keys, bearer tokens),
private-key blocks, ``password=``-style assignments, and every email address — each becomes ``[redacted]``.

Standard library only. No network. This is the one renderer both the local run and the session exporter use,
so no pass in the devblog pipeline ever reads a raw log.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from pathlib import Path

__version__ = "1.0.0"

REDACTED = "[redacted]"

SECRET_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----", re.DOTALL),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),  # GitHub tokens
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}\b"),  # Slack
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),  # AWS access key id
    re.compile(r"\bsk-(?:ant-)?[A-Za-z0-9_-]{20,}\b"),  # Anthropic / OpenAI style
    re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]{20,}"),
    # password=..., secret: ..., AWS_SECRET_ACCESS_KEY=..., api_key="..." : the key word may carry affixes
    re.compile(
        r"(?i)\b[A-Za-z0-9_-]*(?:password|passwd|secret|token|api[_-]?key)[A-Za-z0-9_-]*\s*[=:]\s*['\"]?[^\s'\"]{6,}"
    ),
)
EMAIL_PATTERN = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
HARNESS_TAGS = re.compile(r"<(system-reminder|ide_opened_file|ide_selection)>.*?</\1>\s*", re.DOTALL)


# ----------------------------------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class Turn:
    """One prompt or reply."""

    timestamp: str
    role: str
    text: str


# ----------------------------------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class Stats:
    """The figures the design measured, re-derived: see design/devblog.md, *Session logs*."""

    raw_bytes: int
    text_bytes: int
    secret_matches: int
    distinct_emails: int


# ----------------------------------------------------------------------------------------------------------------------
def redact(text: str) -> str:
    """Replace every secret-shaped string and every email address with ``[redacted]``."""
    for pattern in SECRET_PATTERNS:
        text = pattern.sub(REDACTED, text)
    return EMAIL_PATTERN.sub(REDACTED, text)


# ----------------------------------------------------------------------------------------------------------------------
def clean(text: str) -> str:
    """Strip harness tags injected around a human prompt."""
    return HARNESS_TAGS.sub("", text).strip()


# ----------------------------------------------------------------------------------------------------------------------
def _text_of(content: object) -> str:
    """The text blocks of a message's content; tool calls, tool results and thinking are not text."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = [b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text"]
        return "\n\n".join(p for p in parts if p)
    return ""


# ----------------------------------------------------------------------------------------------------------------------
def _records(path: Path) -> Iterator[dict]:
    with path.open(encoding="utf-8", errors="replace") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(record, dict):
                yield record


# ----------------------------------------------------------------------------------------------------------------------
def iter_turns(path: Path, role: str | None = None) -> Iterator[Turn]:
    """Yield the conversation of one session, redacted, in file order; ``role`` keeps only ``owner`` or ``assistant``."""
    for record in _records(path):
        kind = record.get("type")
        if kind not in ("user", "assistant") or record.get("isSidechain") or record.get("isMeta"):
            continue
        if role and role != ("owner" if kind == "user" else "assistant"):
            continue
        text = clean(_text_of(record.get("message", {}).get("content")))
        if not text:
            continue
        yield Turn(str(record.get("timestamp", "")), "owner" if kind == "user" else "assistant", redact(text))


# ----------------------------------------------------------------------------------------------------------------------
def _stamp(timestamp: str) -> str:
    """``2026-09-06T17:08:41.133Z`` → ``2026-09-06 17:08``; anything else is returned as given."""
    return timestamp[:16].replace("T", " ") if len(timestamp) >= 16 and timestamp[10:11] == "T" else timestamp


# ----------------------------------------------------------------------------------------------------------------------
def render(turns: Iterable[Turn], session_id: str) -> str:
    """One Markdown document: a title, then one ``##`` heading per turn."""
    out = [
        f"# Session {session_id}",
        "",
        "*Prompts and replies only; tool output omitted; secrets and emails redacted.*",
        "",
    ]
    for turn in turns:
        out += [f"## {_stamp(turn.timestamp)} · {turn.role}", "", turn.text, ""]
    return "\n".join(out)


# ----------------------------------------------------------------------------------------------------------------------
def stats(path: Path) -> Stats:
    """Re-derive the design's figures for one raw log, before redaction."""
    text_bytes = 0
    secrets = 0
    emails: set[str] = set()
    for record in _records(path):
        if record.get("type") not in ("user", "assistant"):
            continue
        text = _text_of(record.get("message", {}).get("content"))
        text_bytes += len(text.encode("utf-8"))
        secrets += sum(len(p.findall(text)) for p in SECRET_PATTERNS)
        emails.update(EMAIL_PATTERN.findall(text))
    return Stats(path.stat().st_size, text_bytes, secrets, len(emails))


# ----------------------------------------------------------------------------------------------------------------------
def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("sessions", nargs="+", type=Path, help="session .jsonl files")
    parser.add_argument("--out", type=Path, help="write <session-id>.md files here instead of stdout")
    parser.add_argument("--stats", action="store_true", help="print the design's figures instead of rendering")
    parser.add_argument("--role", choices=("owner", "assistant"), help="keep only one side of the conversation")
    args = parser.parse_args(argv)

    if args.stats:
        total = Stats(0, 0, 0, 0)
        for path in args.sessions:
            s = stats(path)
            print(
                f"{path.name}\traw {s.raw_bytes}\ttext {s.text_bytes}\tsecrets {s.secret_matches}\temails {s.distinct_emails}"
            )
            total = Stats(
                total.raw_bytes + s.raw_bytes,
                total.text_bytes + s.text_bytes,
                total.secret_matches + s.secret_matches,
                total.distinct_emails + s.distinct_emails,
            )
        print(
            f"TOTAL\traw {total.raw_bytes}\ttext {total.text_bytes}\tsecrets {total.secret_matches}\temails {total.distinct_emails}"
        )
        return 0

    for path in args.sessions:
        session_id = path.stem
        document = render(iter_turns(path, args.role), session_id)
        if args.out:
            args.out.mkdir(parents=True, exist_ok=True)
            target = args.out / (f"{session_id}.{args.role}.md" if args.role else f"{session_id}.md")
            target.write_text(document, encoding="utf-8")
            print(f"{target}	{len(document.encode('utf-8'))} bytes")
        else:
            sys.stdout.write(document)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
