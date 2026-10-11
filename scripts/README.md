# CO3DEX Development Scripts

Quick commands to manage the Jekyll site.

## Usage

### PowerShell (Recommended for Windows)

```powershell
# Install dependencies
.\scripts\install.ps1

# Start development server with LiveReload
.\scripts\serve.ps1

# Build for production
.\scripts\build.ps1

# Clean build artifacts
.\scripts\clean.ps1
```

### Batch Files (Windows CMD)

```cmd
REM Start development server
scripts\serve.cmd
```

### Makefile (Linux/macOS/Windows with Make)

```bash
# Show available commands
make help

# Install dependencies
make install

# Start development server
make serve

# Build for production
make build

# Clean build artifacts
make clean
```

## Prerequisites

- Ruby 3.3+ with DevKit
- Bundler gem

Install with:
```powershell
winget install RubyInstallerTeam.RubyWithDevKit.3.3
gem install bundler
```

## Development Workflow

1. **First time setup:**
   ```powershell
   .\scripts\install.ps1
   ```

2. **Start local server:**
   ```powershell
   .\scripts\serve.ps1
   ```
   Visit http://localhost:4000

3. **Build for deployment:**
   ```powershell
   .\scripts\build.ps1
   ```
   Output in `_site/` folder

## Notes

- Config changes (`_config.yml`) require server restart
- LiveReload auto-refreshes browser on file changes
- Server runs on http://localhost:4000 by default

## Verification tools (`scripts/verify/`)

Use these when a change should leave the site looking and behaving the same: removing a feature,
slimming assets, upgrading a library. Standard library Python only. See "Removing or replacing a site
feature" in [CLAUDE.md](../CLAUDE.md) for when and how to run them.

- `refcheck.py <built-site-dir> --baseline <main-build-dir>` reports asset references (HTML attributes,
  `srcset`, and CSS `url(...)`) that point at nothing in your build but resolve in the `main` build, and
  exits 1 if there are any. Without `--baseline` it just lists every unresolved reference (about 40
  harmless ones exist today: a link inside an HTML comment, markdown pasted into an `href`) and exits 0.
  If the two builds were made with different `url:` values (as `render_compare.py` needs), pass
  `--site-url` and `--baseline-site-url`. Exit code 2 means bad input: a directory with no `index.html`,
  or a scan that found no references at all, since "nothing missing" from a scan that looked at nothing
  is not a pass. It cannot see URLs assembled by JavaScript.
- `render_compare.py <before-dir> <after-dir> [--pages /,/about/]` renders pages from two builds in
  headless Chrome and compares pixels. Build both with the site `url:` set to `http://localhost:4101`
  (before) and `http://localhost:4102` (after), or the pages load their assets from the live site. Each
  side is rendered twice to measure noise. It exits nonzero if any page changed beyond that noise. It
  blocks the Maker Widget and Buy Me a Coffee hosts (they flicker), starts every Chrome launch with a
  fresh profile (so cached CSS cannot hide a break), and refuses to compare unless every page returns
  200.
  - It checks the page as first rendered. Click-driven UI (the lightbox, the search overlay, the theme
    toggle) is not exercised.
  - Before trusting a "same", prove the tool can fail: copy the after build, delete a stylesheet the page
    needs, and confirm it reports CHANGED.
  - In Git Bash on Windows, path arguments are rewritten. Set `MSYS_NO_PATHCONV=1` and pass `C:/...`
    paths for the directories and `/about/`-style paths for `--pages`.
- `snapshot_live.py <output-dir> [--site URL]` records a live site: the body, status code and key headers of
  every sitemap URL, plus how the apex, `www`, HTTP and HTTPS variants redirect. Take one before a hosting or
  build change and one after, then run `snapshot_diff.py <before> <after>`. It exits 1 if any status code,
  redirect, URL set or visible page text changed; changes that leave the visible text alone (markup,
  timestamps, compiled CSS) are listed but do not fail it. Check the tool the way you check the others: two
  snapshots of an unchanged site must give no problems, and an altered copy must give some. Used for the
  2026-10-11 Pages cutover.

