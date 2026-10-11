"""Snapshot a live site: bodies, status codes and selected headers for every sitemap URL, plus how the host and
scheme variants redirect. Take one before a hosting or build change and one after, then compare them with
snapshot_diff.py.

Usage:
    python scripts/verify/snapshot_live.py <output-dir> [--site https://www.co3dex.com]

The apex-domain and plain-HTTP variants are derived from --site. Standard library only.
"""
import argparse
import hashlib
import http.client
import json
import pathlib
import re
import urllib.error
import urllib.parse
import urllib.request

KEEP = ("content-type", "cache-control", "server", "content-encoding", "access-control-allow-origin", "location")
EXTRA = ["/sitemap.xml", "/feed.xml", "/robots.txt", "/404.html", "/humans.txt", "/CNAME", "/assets/css/main.css",
         "/this-page-does-not-exist/"]


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "co3dex-snapshot", "Accept-Encoding": "identity"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, dict(r.headers), r.read()
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read()


def redirect(host, path="/", https=True):
    """One request, no redirect following: what does this host/scheme answer?"""
    conn_cls = http.client.HTTPSConnection if https else http.client.HTTPConnection
    try:
        conn = conn_cls(host, timeout=30)
        conn.request("GET", path, headers={"User-Agent": "co3dex-snapshot"})
        resp = conn.getresponse()
        location = resp.getheader("Location")
        resp.read()
        conn.close()
        return {"status": resp.status, "location": location}
    except Exception as e:  # a connection failure is itself a result worth recording
        return {"error": f"{type(e).__name__}: {str(e)[:80]}"}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("outdir")
    ap.add_argument("--site", default="https://www.co3dex.com")
    args = ap.parse_args()
    site = args.site.rstrip("/")
    out = pathlib.Path(args.outdir)
    out.mkdir(parents=True, exist_ok=True)

    status, _, body = get(site + "/sitemap.xml")
    if status != 200:
        raise SystemExit(f"{site}/sitemap.xml returned {status}; cannot enumerate pages")
    urls = sorted(set(re.findall(r"<loc>([^<]+)</loc>", body.decode("utf-8", "replace")) + [site + e for e in EXTRA]))
    pages = {}
    for url in urls:
        st, hd, bd = get(url)
        name = hashlib.sha1(url.encode()).hexdigest()[:12]
        (out / f"{name}.body").write_bytes(bd)
        pages[url] = {"status": st, "sha256": hashlib.sha256(bd).hexdigest(), "len": len(bd), "file": name,
                      "headers": {k: v for k, v in ((k.lower(), v) for k, v in hd.items()) if k in KEEP}}

    host = urllib.parse.urlparse(site).hostname
    apex = host[4:] if host.startswith("www.") else host
    variants = {"https://www": redirect(host), "http://www": redirect(host, https=False),
                "https://apex": redirect(apex), "http://apex": redirect(apex, https=False),
                "https://www/blog": redirect(host, "/blog")}
    (out / "index.json").write_text(json.dumps({"site": site, "pages": pages, "redirects": variants}, indent=1),
                                    encoding="utf-8")
    print(f"snapshot: {len(pages)} urls -> {out}")


if __name__ == "__main__":
    main()
