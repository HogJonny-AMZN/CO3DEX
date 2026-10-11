"""Render pages from two built copies of the site in headless Chrome and compare pixels.

Usage:
    python scripts/verify/render_compare.py <before-dir> <after-dir> [--pages /,/about/,...]

Both builds must be made with the site URL pointed at the local servers this
script starts (before = http://localhost:4101, after = http://localhost:4102).
Otherwise the pages pull their CSS and JS from the live site and the comparison
is meaningless. For example:

    printf 'url: "http://localhost:4101"\n' > ov-before.yml
    printf 'url: "http://localhost:4102"\n' > ov-after.yml
    # in a clean worktree of main:   bundle exec jekyll build --config _config.yml,<abs path>/ov-before.yml --destination <abs path>/site_before
    # in the branch:                 bundle exec jekyll build --config _config.yml,<abs path>/ov-after.yml  --destination <abs path>/site_after

On Windows, pass the override file to --config as a C:/... path, not /c/....

Each side is rendered twice. The two "before" renders show how much a page
changes between renders of identical code (animations, third-party widgets,
font timing). A page counts as changed only if even the closest before/after
pair differs by more than that noise. A change smaller than the noise on an
animated page can slip through, so read the reported bounding boxes too.

Needs Chrome or Chromium (set CHROME to override discovery). Standard library only.
"""
import argparse
import functools
import http.server
import os
import pathlib
import shutil
import socketserver
import struct
import subprocess
import tempfile
import threading
import urllib.error
import urllib.request
import zlib

DEFAULT_PAGES = ["/", "/about/", "/blog/", "/contact/", "/gallery/"]
# Third-party widgets that load after the page and flicker between renders. They are not
# part of what the repo serves, so they are blocked to keep renders deterministic. Real
# dependencies such as jQuery from a CDN are left alone so the page's scripts still run.
NOISY_HOSTS = ["makerwidget.com", "*.makerwidget.com", "buymeacoffee.com", "*.buymeacoffee.com"]


def find_chrome():
    candidates = [os.environ.get("CHROME", "")]
    candidates += [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                   r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                   r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                   "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"]
    candidates += [shutil.which(n) or "" for n in ("google-chrome", "chromium", "chromium-browser", "chrome")]
    for c in candidates:
        if c and pathlib.Path(c).exists():
            return c
    raise SystemExit("No Chrome/Chromium found. Set the CHROME environment variable.")


def load_png(path):
    data = pathlib.Path(path).read_bytes()
    assert data[:8] == b"\x89PNG\r\n\x1a\n", "not a PNG"
    pos, idat, ihdr = 8, b"", None
    while pos < len(data):
        n, t = struct.unpack(">I4s", data[pos:pos + 8])
        body = data[pos + 8:pos + 8 + n]
        pos += 12 + n
        if t == b"IHDR":
            ihdr = struct.unpack(">IIBBBBB", body)
        elif t == b"IDAT":
            idat += body
    w, h, depth, ctype, _, _, interlace = ihdr
    assert depth == 8 and interlace == 0 and ctype in (2, 6), f"unsupported PNG {ihdr}"
    bpp = 3 if ctype == 2 else 4
    stride = w * bpp
    raw, rows, prev, i = zlib.decompress(idat), [], bytearray(stride), 0
    for _ in range(h):
        ftype, line = raw[i], bytearray(raw[i + 1:i + 1 + stride])
        i += 1 + stride
        for x in range(stride):
            a = line[x - bpp] if x >= bpp else 0
            b = prev[x]
            c = prev[x - bpp] if x >= bpp else 0
            if ftype == 1:
                line[x] = (line[x] + a) & 255
            elif ftype == 2:
                line[x] = (line[x] + b) & 255
            elif ftype == 3:
                line[x] = (line[x] + ((a + b) >> 1)) & 255
            elif ftype == 4:
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                line[x] = (line[x] + (a if pa <= pb and pa <= pc else b if pb <= pc else c)) & 255
        rows.append(bytes(line))
        prev = line
    return w, h, bpp, rows


def diff(path_a, path_b):
    """Return (count, bbox, max_channel_delta); count 0 means pixel-identical."""
    wa, ha, bpp, ra = load_png(path_a)
    wb, hb, _, rb = load_png(path_b)
    if (wa, ha) != (wb, hb):
        return -1, None, 255
    n, maxd, box = 0, 0, [10**9, 10**9, -1, -1]
    for y in range(ha):
        if ra[y] == rb[y]:
            continue
        for x in range(wa):
            pa, pb = ra[y][x * bpp:(x + 1) * bpp], rb[y][x * bpp:(x + 1) * bpp]
            if pa != pb:
                n += 1
                maxd = max(maxd, max(abs(i - j) for i, j in zip(pa, pb)))
                box = [min(box[0], x), min(box[1], y), max(box[2], x), max(box[3], y)]
    return n, (tuple(box) if n else None), maxd


def serve(directory, port):
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass
    handler = functools.partial(Quiet, directory=str(directory))
    server = socketserver.ThreadingTCPServer(("127.0.0.1", port), handler)
    server.daemon_threads = True
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("before"); ap.add_argument("after")
    ap.add_argument("--pages", default=",".join(DEFAULT_PAGES))
    ap.add_argument("--block", default="", help="extra comma-separated hosts to block during renders")
    ap.add_argument("--width", type=int, default=1280); ap.add_argument("--height", type=int, default=1800)
    args = ap.parse_args()
    pages = [p.strip() for p in args.pages.split(",") if p.strip()]
    bad = [p for p in pages if not p.startswith("/") or ":" in p]
    if bad:
        raise SystemExit(f"Not a site path: {bad}. In Git Bash, a lone '/' argument is rewritten to a Windows path; "
                         "run with MSYS_NO_PATHCONV=1, or omit --pages to use the defaults.")
    for label, d in (("before", args.before), ("after", args.after)):
        if not (pathlib.Path(d) / "index.html").is_file():
            raise SystemExit(f"--{label} directory has no index.html: {d!r}. "
                             "On Windows pass C:/... style paths if Git Bash path conversion is disabled.")
    chrome = find_chrome()
    blocked = NOISY_HOSTS + [h.strip() for h in args.block.split(",") if h.strip()]
    resolver = "--host-resolver-rules=" + ", ".join(f"MAP {h} ~NOTFOUND" for h in blocked)
    servers = [serve(args.before, 4101), serve(args.after, 4102)]
    # Refuse to compare error pages: every page must answer 200 on both sides.
    for port in (4101, 4102):
        for path in pages:
            try:
                status = urllib.request.urlopen(f"http://localhost:{port}{path}", timeout=30).status
            except urllib.error.HTTPError as e:
                status = e.code
            if status != 200:
                for s_ in servers:
                    s_.shutdown()
                raise SystemExit(f"http://localhost:{port}{path} returned {status}. Check the page exists in that build.")
    out = pathlib.Path(tempfile.mkdtemp(prefix="render_compare_"))

    def shoot(tag, port):
        for i, path in enumerate(pages):
            target = out / f"{tag}_{i}.png"
            # A fresh profile per launch: otherwise Chrome reuses cached CSS/JS from an earlier
            # run at the same URL and a broken "after" build can look identical to "before".
            profile = tempfile.mkdtemp(prefix="render_compare_profile_")
            try:
                subprocess.run([chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                                f"--user-data-dir={profile}", "--disk-cache-size=1", "--incognito",
                                resolver,
                                f"--window-size={args.width},{args.height}", "--virtual-time-budget=12000",
                                f"--screenshot={target}", f"http://localhost:{port}{path}"],
                               capture_output=True, timeout=180)
            finally:
                shutil.rmtree(profile, ignore_errors=True)

    shoot("before", 4101); shoot("before2", 4101); shoot("after", 4102); shoot("after2", 4102)
    changed = 0
    print(f"{'page':26} {'before vs before (noise)':32} {'closest before/after':32} verdict")
    fmt = lambda d: "identical" if d[0] == 0 else "size changed" if d[0] < 0 else f"{d[0]} px {d[1]} d<={d[2]}"
    for i, path in enumerate(pages):
        try:
            noise = diff(out / f"before_{i}.png", out / f"before2_{i}.png")
            pairs = [diff(out / f"{b}_{i}.png", out / f"{a}_{i}.png") for b in ("before", "before2") for a in ("after", "after2")]
        except (FileNotFoundError, AssertionError) as e:
            print(f"{path:26} could not render: {e}"); changed += 1; continue
        closest = min(pairs, key=lambda d: (d[0] < 0, d[0] if d[0] >= 0 else 0))
        real = closest[0] != 0 and (closest[0] < 0 or noise[0] < 0 or closest[0] > noise[0])
        changed += real
        print(f"{path:26} {fmt(noise):32} {fmt(closest):32} {'CHANGED' if real else 'same'}")
    for s in servers:
        s.shutdown()
    print(f"\n{changed} page(s) changed beyond control noise. Screenshots kept in {out}")
    raise SystemExit(1 if changed else 0)


if __name__ == "__main__":
    main()
