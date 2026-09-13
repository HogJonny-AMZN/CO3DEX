#!/usr/bin/env python3
"""Scan files the devblog generated before they are committed to a public repository. Any hit fails.

Usage::

    python scan_public.py <file>...        # exit 1 and print file:line: kind — the match, on any hit

Hits: secret-shaped strings and email addresses (the same patterns ``session_text.py`` redacts), absolute paths
(Windows drives, ``/home/``, ``/Users/``), and URLs into the private repositories named in PRIVATE_REPOS.
Citations must be stable identifiers — a journal file and heading, a commit hash, a benchmark file — so a
private URL or an absolute path in a memo is a disclosure, not a citation.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

from session_text import EMAIL_PATTERN, SECRET_PATTERNS

__version__ = "1.0.0"

PRIVATE_REPOS: tuple[str, ...] = (
    "HogJonny-AMZN/SpriteJammer",
    "HogJonny-AMZN/LargeWorlds",
    "HogJonny-AMZN/Job_Orchestrator",
    "HogJonny-AMZN/devlog-sessions",
)
ABSOLUTE_PATH = re.compile(r"(?<![A-Za-z0-9])[A-Za-z]:[\\/](?![\\/])|(?<![\w/])/(?:home|Users)/")
PRIVATE_URL = re.compile(r"github\.com/(?:" + "|".join(re.escape(r) for r in PRIVATE_REPOS) + r")", re.IGNORECASE)


# ----------------------------------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class Hit:
    line: int
    kind: str
    match: str


# ----------------------------------------------------------------------------------------------------------------------
def scan_text(text: str) -> list[Hit]:
    """Every disclosure in ``text``, in line order."""
    hits: list[Hit] = []
    for number, line in enumerate(text.splitlines(), start=1):
        for pattern in SECRET_PATTERNS:
            hits += [Hit(number, "secret", m.group(0)[:24]) for m in pattern.finditer(line)]
        hits += [Hit(number, "email address", m.group(0)) for m in EMAIL_PATTERN.finditer(line)]
        hits += [Hit(number, "absolute path", m.group(0)) for m in ABSOLUTE_PATH.finditer(line)]
        hits += [Hit(number, "private repository URL", m.group(0)) for m in PRIVATE_URL.finditer(line)]
    return hits


# ----------------------------------------------------------------------------------------------------------------------
def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("files", nargs="+", type=Path)
    args = parser.parse_args(argv)
    total = 0
    for path in args.files:
        for hit in scan_text(path.read_text(encoding="utf-8", errors="replace")):
            print(f"{path}:{hit.line}: {hit.kind}: {hit.match}")
            total += 1
    print(f"{'HALT' if total else 'clean'}: {total} hit(s) in {len(args.files)} file(s)")
    return 1 if total else 0


if __name__ == "__main__":
    raise SystemExit(main())
