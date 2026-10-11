"""List asset references in a built site that do not resolve to a file.

Usage:
    python scripts/verify/refcheck.py <built-site-dir> [--site-url URL]
    python scripts/verify/refcheck.py <built-site-dir> --baseline <dir-of-main-build> [--baseline-site-url URL]

Scans every .html file for src/href/srcset-style attributes and every .css file
for url(...), resolves each local reference against the build directory, and
prints the ones that point at nothing as "<file>\\t<reference>". A summary goes
to stderr.

Some hits are false positives that exist in every build (a link inside an HTML
comment, markdown pasted into an href), so a bare list is informational and the
exit code is 0. To gate a change, pass --baseline with a build of main: only
references missing in <built-site-dir> and NOT in the baseline are reported, and
the exit code is 1 if there are any.

Exit codes: 0 ok, 1 regressions found (--baseline), 2 bad input. Bad input
includes a directory with no index.html and a scan that finds no references at
all, because "nothing missing" from a scan that looked at nothing is not a pass.

What it cannot see: URLs assembled by JavaScript, and anything outside
src/href/data-src/data-responsive/poster/srcset attributes and CSS url(...).
Standard library only.
"""
import argparse
import pathlib
import re
import sys
import urllib.parse

ATTR = re.compile(r'(?:src|href|data-src|data-responsive|poster)\s*=\s*"([^"]+)"', re.I)
SRCSET = re.compile(r'srcset\s*=\s*"([^"]+)"', re.I)
CSSURL = re.compile(r"url\(([^)]+)\)", re.I)
SKIP = ("data:", "#", "mailto:", "javascript:", "tel:", "//")


def resolve(root, site, base, ref):
    ref = ref.strip().strip("\"'")
    if not ref or ref.startswith(SKIP):
        return None
    if ref.startswith("http"):
        if not ref.startswith(site):
            return None
        ref = ref[len(site):] or "/"
    ref = urllib.parse.unquote(ref.split("#")[0].split("?")[0])
    if not ref:
        return None
    return root / ref.lstrip("/") if ref.startswith("/") else base.parent / ref


def exists(p):
    return p.is_file() or (p.is_dir() and (p / "index.html").is_file()) or p.with_suffix(".html").is_file()


def scan(root, site):
    """Return (references_checked, set of (file, reference) that resolve to nothing)."""
    missing, checked = set(), 0
    for f in root.rglob("*"):
        if not f.is_file():
            continue
        suffix = f.suffix.lower()
        if suffix not in (".html", ".htm", ".css"):
            continue
        text = f.read_text(encoding="utf-8", errors="ignore")
        if suffix == ".css":
            refs = CSSURL.findall(text)
        else:
            refs = ATTR.findall(text)
            for group in SRCSET.findall(text):
                refs += [part.strip().split()[0] for part in group.split(",") if part.strip()]
        for ref in refs:
            target = resolve(root, site, f, ref)
            if target is None:
                continue
            checked += 1
            if not exists(target):
                shown = ref.strip().strip("\"'")
                if shown.startswith(site):          # builds made with different url: values must compare equal
                    shown = shown[len(site):] or "/"
                missing.add((f.relative_to(root).as_posix(), shown))
    return checked, missing


def fail(message):
    print(message, file=sys.stderr)
    sys.exit(2)


def checked_scan(label, directory, site):
    root = pathlib.Path(directory)
    if not (root / "index.html").is_file():
        fail(f"{label}: {directory!r} has no index.html. Is this a built site directory? "
             "(In Git Bash on Windows, pass a C:/... path if path conversion is disabled.)")
    checked, missing = scan(root, site)
    if checked == 0:
        fail(f"{label}: no asset references found under {directory!r}. Refusing to report "
             "'nothing missing' from a scan that looked at nothing. Check --site-url.")
    return checked, missing


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("directory")
    ap.add_argument("--site-url", default="https://www.co3dex.com",
                    help="the url: the directory was built with; absolute refs under it are checked")
    ap.add_argument("--baseline", help="a build of main; report only references missing here and not there")
    ap.add_argument("--baseline-site-url", help="the url: the baseline was built with (default: --site-url)")
    args = ap.parse_args()
    site = args.site_url.rstrip("/")

    checked, missing = checked_scan("build", args.directory, site)
    if not args.baseline:
        print(f"checked={checked} missing={len(missing)}", file=sys.stderr)
        for item in sorted(missing):
            print("\t".join(item))
        return 0

    base_site = (args.baseline_site_url or args.site_url).rstrip("/")
    base_checked, base_missing = checked_scan("baseline", args.baseline, base_site)
    regressions = missing - base_missing
    print(f"checked={checked} (baseline {base_checked})  missing={len(missing)} (baseline {len(base_missing)})  "
          f"regressions={len(regressions)}  fixed={len(base_missing - missing)}", file=sys.stderr)
    for item in sorted(regressions):
        print("\t".join(item))
    return 1 if regressions else 0


if __name__ == "__main__":
    raise SystemExit(main())
