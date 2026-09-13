#!/usr/bin/env python3
"""Scan files the devblog generated before they are committed to a public repository. Any hit fails.

Usage::

    python scan_public.py <file>...        # exit 1 and print file:line: kind: the match, on any hit

Hits: secret-shaped strings and email addresses (the same patterns ``session_text.py`` redacts, run over the
whole text so a private-key block spanning lines is seen whole), absolute paths (a drive letter with either
slash, doubled backslashes included; a UNC share; a POSIX path under a root folder such as ``/home``,
``/Users``, ``/tmp``, ``/var``, ``/workspace``), and URLs into the private repositories named in PRIVATE_REPOS.
A URL scheme's ``://`` and a clock time's ``17:08/`` are not paths.

The gate is for generated files: the memo and the two continuity files. The skill's own sources and tests
carry fixtures that trip it on purpose and are not scanned by the coordinator.
Citations must be stable identifiers, a journal file and heading, a commit hash, a benchmark file, so a
private URL or an absolute path in a memo is a disclosure, not a citation.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

from session_text import EMAIL_PATTERN, SECRET_PATTERNS

__version__ = "1.3.0"

PRIVATE_REPOS: tuple[str, ...] = (
    "HogJonny-AMZN/SpriteJammer",
    "HogJonny-AMZN/LargeWorlds",
    "HogJonny-AMZN/Job_Orchestrator",
    "HogJonny-AMZN/devlog-sessions",
)
POSIX_ROOTS = ("home", "Users", "tmp", "var", "workspace", "workspaces", "mnt", "opt", "srv", "root", "etc", "usr")
ABSOLUTE_PATH = re.compile(
    r"(?<![A-Za-z0-9])[A-Za-z]:(?:\\+|/(?!/))"  # D:\, D:\\ (escaped), D:/  but not the :// of a URL scheme
    r"|(?<![\w/.])\\\\+[A-Za-z0-9_.-]+\\"  # \\server\share
    r"|(?<![\w/.])/(?:" + "|".join(POSIX_ROOTS) + r")/"  # /home/..., /tmp/...
)
PRIVATE_URL = re.compile(r"github\.com/(?:" + "|".join(re.escape(r) for r in PRIVATE_REPOS) + r")", re.IGNORECASE)
SECRET_MARKER = "[secret shape, not shown]"
MARKERS = {
    "secret": SECRET_MARKER,
    "email address": "[email address, not shown]",
    "absolute path": "[absolute path, not shown]",
    "private repository URL": "[private repository URL, not shown]",
}


# ----------------------------------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class Hit:
    line: int
    kind: str
    match: str


# ----------------------------------------------------------------------------------------------------------------------
def scan_text(text: str) -> list[Hit]:
    """Every disclosure in ``text``, in line order; a multi-line match is reported at the line it starts on."""
    hits: list[Hit] = []
    for pattern, kind in [(p, "secret") for p in SECRET_PATTERNS] + [
        (EMAIL_PATTERN, "email address"),
        (ABSOLUTE_PATH, "absolute path"),
        (PRIVATE_URL, "private repository URL"),
    ]:
        for m in pattern.finditer(text):
            # a secret is never echoed, not even in part: the gate's own output may land in a CI log
            shown = MARKERS[kind]  # nothing disallowed is echoed: this output may land in a public CI log
            hits.append(Hit(text.count("\n", 0, m.start()) + 1, kind, shown))
    return sorted(hits, key=lambda h: (h.line, h.kind, h.match))


# ----------------------------------------------------------------------------------------------------------------------
def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("files", nargs="+", type=Path)
    args = parser.parse_args(argv)
    total = 0
    for path in args.files:
        if not path.exists():
            print(f"{path}: missing: a file the run should have written is not there")
            total += 1
            continue
        for hit in scan_text(path.read_text(encoding="utf-8", errors="replace")):
            print(f"{path}:{hit.line}: {hit.kind}: {hit.match}")
            total += 1
    print(f"{'HALT' if total else 'clean'}: {total} hit(s) in {len(args.files)} file(s)")
    return 1 if total else 0


if __name__ == "__main__":
    raise SystemExit(main())
