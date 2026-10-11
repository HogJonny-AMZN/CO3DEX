# Decisions

A short log of decisions that shape the site, so the reasons live in the repo. Newest first. Each entry
says what was decided, why, and what it means for the next change.

## 2026-10-10

### Locked content has two tiers

- **Non-sensitive locked portfolio items** (the owner confirmed nothing in the current set is sensitive):
  password-protected pages on the public site, encrypted in the browser at build time (a StatiCrypt-style
  approach). Simple, free, stays on `co3dex.com`.
- **Genuinely sensitive material** (anything that could cause real harm if it leaked): never in this repo.
  It lives in a **separate private repo with its own site**, behind real server-side authentication, for
  example a private Cloudflare Pages site behind Cloudflare Access on a subdomain such as
  `private.co3dex.com`. Not built yet. Build it when the first piece of sensitive content needs a home.

**Why two tiers:** this repo is public and Pages is a static host. Encrypted files are public too, so anyone
can copy them and guess passwords offline. That is fine when a leak costs nothing and wrong when it costs
something. A server-side gate keeps the content off the public repo entirely.

**Next:** design the portfolio so either gate can sit in front of an entry, and keep sensitive source files
out of this repo from the start (`.docs/private/` is gitignored and stays local).

### Comments: giscus, as a trial

giscus stores comments as GitHub Discussions on this repo. Free, no ads, no third-party account for the
owner. It needs Discussions enabled on the repo and the giscus app installed. Easy to remove if the
experiment is not worth the time. Disqus and Hyvor are gone (see [origins.md](origins.md)).

### The gallery folds into the portfolio

The standalone gallery (one Starhawk set) becomes the image viewer inside portfolio entries. The nav item
goes away. **lightGallery 1.6.12 is licensed GPLv3** in its own header, so the viewer is replaced with a
permissively licensed one when the portfolio is built (candidates to evaluate: GLightbox, PhotoSwipe;
confirm each license when choosing).

### The legacy portfolio comes from jonathankimballgalloway.me

That site is the source for portfolio entries to import. New work is added alongside it. Entries live in a
Jekyll collection so each is a Markdown file.

### The deploy moves to a GitHub Actions build

Pages is built today by GitHub's pinned Jekyll 3.10, which differs from the Jekyll 4.4 used locally and
blocks plugins. The Actions build removes the mismatch. Cutover is gated on a repo variable and a Pages
setting, so it can be reversed. Differences found between the two builds are listed in the PR that adds
the workflow.

### Housekeeping decided in the owner's favor

- **LICENSE** keeps the upstream copyright line (MIT requires it) and adds the owner's own line for the
  work since the fork (first commit 2022-06-03).
- **Personal images** that nothing referenced stopped being published from `assets/img/`. Four of them
  (`ProfilePicture.jpg`, `CoverPicture.jpg`, `CoverPictture.jpg`, `High Resolution File.jpg`) were already archived
  in `_archive/CO3DEX/` as Git LFS objects, byte-identical (verified by SHA-256 and by fetching them from
  GitHub's LFS server), so the copies in `assets/img/` were removed, not duplicated. `Vectorfile.eps` was not
  archived anywhere and is not covered by the LFS rules, so it moved to `_archive/CO3DEX/Vectorfile.eps`.
  `.gitattributes` sends every JPEG outside `assets/` through LFS, so a raw JPEG must never be committed
  outside `assets/`.
- **The three `SEO_*.md` notes** moved unchanged to `docs/seo/` with an index. They are dated snapshots from
  February and March 2026; verify before relying on them.
- **CI runner** pinned to `ubuntu-24.04`. GitHub moves `ubuntu-latest` to Ubuntu 26 on 2026-10-19, and a
  build tool should not change under the build unannounced.
