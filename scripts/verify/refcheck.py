"""List asset references in a built site that do not resolve to a file.

Usage: python scripts/verify/refcheck.py <built-site-dir> [site-url]

Scans every .html file for src/href-style attributes and every .css file for
url(...), resolves each local reference against the build directory, and prints
the ones that point at nothing as "<file>\t<reference>". The count goes to stderr.

Compare the output for a build of main against your branch: a reference that is
missing only on the branch is a regression. Some hits are false positives (a
link inside an HTML comment, or markdown pasted into an href), so only the
difference between two builds is meaningful.
"""
import pathlib
import re
import sys
import urllib.parse

root = pathlib.Path(sys.argv[1])
SITE = (sys.argv[2] if len(sys.argv) > 2 else "https://www.co3dex.com").rstrip("/")
ATTR = re.compile(r'(?:src|href|data-src|data-responsive|poster)\s*=\s*"([^"]+)"', re.I)
CSSURL = re.compile(r"url\(([^)]+)\)", re.I)
SKIP = ("data:", "#", "mailto:", "javascript:", "tel:", "//")


def resolve(base, ref):
    ref = ref.strip().strip("\"'")
    if not ref or ref.startswith(SKIP):
        return None
    if ref.startswith("http"):
        if not ref.startswith(SITE):
            return None
        ref = ref[len(SITE):] or "/"
    ref = urllib.parse.unquote(ref.split("#")[0].split("?")[0])
    if not ref:
        return None
    return root / ref.lstrip("/") if ref.startswith("/") else base.parent / ref


def exists(p):
    return p.is_file() or (p.is_dir() and (p / "index.html").is_file()) or p.with_suffix(".html").is_file()


missing, checked = set(), 0
for f in root.rglob("*"):
    if not f.is_file():
        continue
    suffix = f.suffix.lower()
    if suffix not in (".html", ".htm", ".css"):
        continue
    text = f.read_text(encoding="utf-8", errors="ignore")
    refs = CSSURL.findall(text) if suffix == ".css" else ATTR.findall(text)
    for ref in refs:
        target = resolve(f, ref)
        if target is None:
            continue
        checked += 1
        if not exists(target):
            missing.add((f.relative_to(root).as_posix(), ref.strip().strip("\"'")))

print(f"checked={checked} missing={len(missing)}", file=sys.stderr)
for item in sorted(missing):
    print("\t".join(item))
