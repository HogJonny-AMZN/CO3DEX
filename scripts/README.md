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

- `refcheck.py <built-site-dir> [site-url]` lists asset references (HTML attributes and CSS `url(...)`)
  that point at nothing. Run it on a build of `main` and on your branch; a reference missing only on the
  branch is a regression. Some hits exist on both sides (a link inside an HTML comment, markdown pasted
  into an `href`), so only the difference matters.
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
