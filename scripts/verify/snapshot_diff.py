"""Compare two snapshots made by snapshot_live.py (for example before and after a hosting or build change).

Usage:
    python scripts/verify/snapshot_diff.py <before-dir> <after-dir>

Reports, in order:
  * how each host/scheme variant redirects (apex, www, http, https)
  * status-code and header changes, and URLs that appeared or disappeared
  * which bodies changed, with changed lines sorted into timestamps, generator tag, code-highlight markup
    and everything else, plus the visible text of every HTML page (tags stripped) compared exactly

Exit code 1 if any status code, redirect, URL set or visible text changed; byte-level changes that leave the
visible text alone (markup, timestamps, compiled CSS) are reported but do not fail the run.

Before trusting a clean result, run it on two snapshots of the same unchanged site (it must report no
problems) and on a copy you altered on purpose (it must report them). Standard library only.
"""
import difflib
import html
import json
import pathlib
import re
import sys

TS = re.compile(r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:[+-]\d{2}:\d{2}| [+-]\d{4})"
                r"|\w{3}, \d{2} \w{3} \d{4} \d{2}:\d{2}:\d{2} [+-]\d{4}")
HL = re.compile(r'class=(?:"|&quot;)(?:bp|nn|n|nb|nc|nf|o|p|k|kn|nd|s|s1|s2|sh|c1|mi|w|err)(?:"|&quot;)')


def load(directory):
    return json.loads((directory / "index.json").read_text(encoding="utf-8"))


def visible_words(raw):
    text = raw.decode("utf-8", "replace")
    text = re.sub(r"(?is)<(script|style)\b.*?</\1>", " ", text)
    text = re.sub(r"(?s)<!--.*?-->", " ", text)
    text = re.sub(r"</?span\b[^>]*>", "", text)      # inline spans (code tokens) add no whitespace
    text = re.sub(r"<[^>]+>", " ", text)
    return html.unescape(text).split()


def lines(raw):
    return raw.decode("utf-8", "replace").replace("\r", "").replace("> <", ">\n<").split("\n")


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    before_dir, after_dir = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    a_idx, b_idx = load(before_dir), load(after_dir)
    A, B = a_idx["pages"], b_idx["pages"]
    site = a_idx.get("site") or next(iter(A)).split("/", 3)[0:3]
    site = site if isinstance(site, str) else "/".join(site)
    short = lambda u: u[len(site):] or "/"
    problems = 0

    print("== redirects / host variants ==")
    for key in sorted(set(a_idx["redirects"]) | set(b_idx["redirects"])):
        a, b = a_idx["redirects"].get(key), b_idx["redirects"].get(key)
        if a == b:
            print(f"  {key:18} same     {a}")
        else:
            problems += 1
            print(f"  {key:18} CHANGED  before={a}  after={b}")

    print("== status codes, headers, URL set ==")
    only_a, only_b = sorted(set(A) - set(B)), sorted(set(B) - set(A))
    if only_a or only_b:
        problems += 1
        print("  URL set changed. only before:", [short(u) for u in only_a], " only after:", [short(u) for u in only_b])
    for u in sorted(set(A) & set(B)):
        if A[u]["status"] != B[u]["status"]:
            problems += 1
            print(f"  STATUS {short(u)}: {A[u]['status']} -> {B[u]['status']}")
        for h in sorted(set(A[u]["headers"]) | set(B[u]["headers"])):
            if A[u]["headers"].get(h) != B[u]["headers"].get(h):
                print(f"  header {h} on {short(u)}: {A[u]['headers'].get(h)!r} -> {B[u]['headers'].get(h)!r}")

    print("== bodies ==")
    identical = changed = pages_checked = 0
    for u in sorted(set(A) & set(B)):
        ra = (before_dir / (A[u]["file"] + ".body")).read_bytes()
        rb = (after_dir / (B[u]["file"] + ".body")).read_bytes()
        is_html = b"<html" in ra[:3000].lower()
        if is_html:
            pages_checked += 1
            if visible_words(ra) != visible_words(rb):
                problems += 1
                print(f"  VISIBLE TEXT CHANGED: {short(u)}")
        if A[u]["sha256"] == B[u]["sha256"]:
            identical += 1
            continue
        changed += 1
        kinds = {"timestamp": 0, "generator": 0, "highlight markup": 0, "other": 0}
        samples = []
        for line in difflib.unified_diff(lines(ra), lines(rb), lineterm="", n=0):
            if line[:1] not in "+-" or line.startswith(("---", "+++")):
                continue
            body = line[1:]
            if "Jekyll v" in body:
                kinds["generator"] += 1
            elif HL.search(body):
                kinds["highlight markup"] += 1
            elif TS.search(body):
                kinds["timestamp"] += 1
            elif body.strip():
                kinds["other"] += 1
                if len(samples) < 2:
                    samples.append(line[:150])
        print(f"  changed {short(u)}: " + (", ".join(f"{k}={v}" for k, v in kinds.items() if v) or "whitespace only"))
        for s in samples:
            print("      ", s)
    print(f"  {identical} bodies byte-identical, {changed} changed; visible text compared on {pages_checked} HTML pages")
    print(f"\nPROBLEMS (status, redirect, URL set, visible text): {problems}")
    raise SystemExit(1 if problems else 0)


if __name__ == "__main__":
    main()
