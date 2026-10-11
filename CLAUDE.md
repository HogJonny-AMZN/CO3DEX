# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
bundle install

# Local dev server with live reload at http://localhost:4000
bundle exec jekyll serve --livereload

# Production build (outputs to ./build)
bundle exec jekyll build

# Clean build artifacts
bundle exec jekyll clean
```

## Architecture

This is a **Jekyll 4.x static blog** originally forked from the devlopr-jekyll theme (see `docs/origins.md`), hosted at <https://www.co3dex.com>. It is a pure static site — no backend, no database.

### Key directories

- `_posts/` — blog posts as Markdown, named `YYYY-MM-DD-slug.md`
- `_layouts/` — page templates (`post.html`, `home.html`, `page.html`, etc.)
- `_includes/` — reusable HTML partials injected into layouts
- `_authors/` — author profile pages (one file per author, e.g. `hogjonny.md`)
- `categories/` — one Markdown file per category (see below)
- `_data/` — YAML data files consumed by layouts/includes
- `assets/` — images, CSS, JS, bower components
- `_sass/` — Sass stylesheets
- `build/` — Jekyll output directory (gitignored)

### Post front matter

```yaml
---
layout: post
title: "Post Title"
summary: "Short summary"
author: hogjonny
date: "YYYY-MM-DD 00:00:00 -0600"
modified_date: "YYYY-MM-DD 00:00:00 -0600"
category: <category-slug>
thumbnail: /assets/img/posts/YYYY-MM-DD-slug.png
keywords: comma,separated,keywords
permalink: /blog/slug/
usemathjax: false
---
```

### Post date (REQUIRED — must not be in the future)

Jekyll **silently skips** posts whose `date:` is in the future — no error, the post simply won't appear after build. Always set `date:` to today or earlier before publishing.

### Category pages (REQUIRED for every new category)

Jekyll does **not** auto-generate category pages — `_config.yml` has `jekyll-archives` disabled. Every unique `category:` value in any post **must** have a matching file in `categories/` or clicking the category link returns a 404.

**Check for missing categories before publishing:**

```bash
grep -h "^category:" _posts/*.md | sort -u
ls categories/
```

Create `categories/<slug>.md` for any missing category:

```markdown
---
layout: page
title: <Display Name>
permalink: /blog/categories/<slug>/
---

<h5> Posts by Category : {{ page.title }} </h5>

<div class="card">
{% for post in site.categories.<slug> %}
 <li class="category-posts"><span>{{ post.date | date_to_string }}</span> &nbsp; <a href="{{ post.url }}">{{ post.title }}</a></li>
{% endfor %}
</div>
```

The `site.categories.<slug>` tag must exactly match the `category:` slug used in posts. The permalink must match the pattern in `_includes/blog_post_article.html`: `/blog/categories/{{category|slugize}}`.

### Currently defined categories

| Slug | File |
| ---- | ---- |
| `info` | `categories/info.md` |
| `jekyll` | `categories/jekyll.md` |
| `life` | `categories/life.md` |
| `guides` | `categories/guides.md` |
| `python` | `categories/python.md` |
| `techart` | `categories/techart.md` |
| `gamedev` | `categories/gamedev.md` |

`categories/all.md` and `categories/sample_category.md` exist as structural/demo files — not real post categories.

Update this table when adding a new category.

### How layouts and includes connect

- `_layouts/post.html` — wraps all blog posts; includes `blog_post_article.html`, `blog_sidebar.html`
- `_includes/blog_post_article.html` — renders post content, category links, share buttons
- `_includes/blog_sidebar.html` — sidebar with recent posts, categories, author info
- `_includes/head.html` — SEO tags via `jekyll-seo-tag`; reads `thumbnail`, `keywords`, and `description` from post front matter
- `_layouts/home.html` — paginated blog index (uses `jekyll-paginate`, 8 posts/page)

### Authors

Author pages live in `_authors/<slug>.md` and are rendered via `_layouts/author.html`. Posts reference authors by the `author:` field matching the author's filename slug.

### Draft workflow

There are **four** distinct draft holding areas — they are not interchangeable.

#### `.docs/wip/` — live free-form drafts

Early writing that isn't post-shaped yet. Tracked in git, ignored by Jekyll entirely (outside its source tree).

> **This repository is PUBLIC.** Anything committed to `.docs/wip/` is immediately readable by anyone on GitHub. Only put drafts here that you are comfortable publishing in their current state. Work material, employer or partner strategy, and anything under NDA goes in `.docs/private/` instead.

#### `.docs/private/` — work material, never published

Gitignored by the `.docs/*` rule in `.gitignore`, which has explicit exceptions only for `wip/` and `archive/`. Files here live on disk and never enter git. Use for anything work-related, commercially sensitive, or not yet cleared to be public.

**Do not add a negation rule for this directory.** Its whole purpose is staying untracked.

#### `.docs/archive/` — retired drafts

Working drafts whose posts are already published, plus editorial process artifacts. Tracked, never built. See `.docs/archive/README.md` for the draft-to-post mapping. Move a draft here after publishing so `wip/` only ever shows live work.

#### `_drafts/` — Jekyll native drafts

Fully post-shaped files (complete front matter, `permalink`, etc.) that are **not built or previewed** by `jekyll serve`/`build`, because neither the Makefile nor `scripts/serve.ps1` passes `--drafts`. To preview them, run `bundle exec jekyll serve --livereload --drafts`. Use for finished posts staged ahead of their publish date.

#### Publishing

Move the file to `_posts/YYYY-MM-DD-slug.md` and set `date:` to today or earlier (see the future-date rule above). Then move the source draft to `.docs/archive/` and add a row to its README.

`_archive/` is a separate legacy location holding brand image assets (the old `_posts_archive/` of theme demo posts was removed; see `docs/origins.md`) — do not publish from these without review.

### Editing a draft toward publication

**Read [EDITORIAL_PIPELINE.md](EDITORIAL_PIPELINE.md) before running any editing pass.** It defines the layered review order (structure → facts → voice → rhythm → reach), the measured voice baselines to calibrate against, which skill in `.claude/skills/` each layer uses, and the publish checklist.

The order is load-bearing: voice work is never first, because restructuring rewrites sentences. Do not polish prose before the structure settles.

### Windows scripts

`scripts/` contains PowerShell equivalents of the Makefile targets (`serve.ps1`, `build.ps1`, `clean.ps1`, `install.ps1`). Use these on Windows if `make` is unavailable.

### Deployment

**GitHub Actions builds and deploys the site** (live since 2026-10-11). `.github/workflows/pages.yml` builds with Jekyll 4.4 and `Gemfile.lock` in production mode on every PR and every push to `main`, and uploads the result as an artifact (download it with `gh run download <run-id> -n github-pages`). On a push to `main` (or a manual run) its deploy job publishes that build to GitHub Pages, with CNAME `www.co3dex.com`. A merge goes live in about a minute. On a PR the deploy job is skipped, so the run is the build check. Locally the site builds to `./build/`.

**The deploy is controlled by two settings, not by code:** the repo variable `PAGES_DEPLOY_VIA_ACTIONS` (must be `true`) and the Pages source (must be "GitHub Actions"). To roll back to GitHub's built-in Jekyll 3.10 builder: set the Pages source back to "Deploy from a branch" (`main`, `/`) and delete the variable. The rollback has not been exercised.

Before the cutover the Jekyll 4 build was compared with the live Jekyll 3 build, and after it the live site was snapshotted before and after (see `scripts/verify/`): the visible text of all 31 HTML pages was identical, no status code, header or redirect changed, and the TLS certificate was unchanged. What did change: the generator tag, build timestamps, code-block highlight class names (same colors) and the compiled stylesheet (expanded, with comments, 57 KB instead of 51 KB; `sass: style: compressed` would shrink it).

Two things the old builder did that this one does not: it silently enabled plugins such as `jekyll-titles-from-headings` (a page with no `title:` got one from its first heading, so give every page a `title:`), and it pinned an older Rouge.

**Local Windows builds show wrong date offsets.** Windows ignores the `America/Chicago` time zone Jekyll sets, so a local build renders every date with today's UTC offset (`-0500` in summer) and shifts times by an hour. Linux (CI and Pages) is correct. Use the CI artifact when exact date output matters.

Internal repo files (`CLAUDE.md`, `AGENTS.md`, `README.md`, the SEO notes, `scripts/`, and so on) are kept out of the published site by the `exclude:` list in `_config.yml`. Add any new root-level non-site file there.

### Handling PR reviews (REQUIRED)

When Copilot or anyone else leaves a review on a PR, and you assess it, **reply on every open review comment and thread**, not only the ones you fixed. The point is that the PR itself shows at a glance what has been handled.

1. Verify each finding against the repo before answering it. Reviews are sometimes wrong, and sometimes right about things a diff can't show.
2. Post an inline reply on each comment:

   ```bash
   gh api -X POST repos/:owner/:repo/pulls/<n>/comments/<comment_id>/replies -f body="..."
   ```

   List the comments with `gh api repos/:owner/:repo/pulls/<n>/comments`. Also answer any findings that live only in the review body or in issue-level comments.
3. Each reply says what happened: addressed (cite the commit and what you verified), declined (say why), or deferred (say to what and why). Never leave a thread silent.
4. Do not resolve threads unless asked. The reviewer or the owner resolves them.

### Repository workflow (REQUIRED)

- **Never commit to `main`.** Branch from an up-to-date `main` (`chore/...`, `docs/...`, `fix/...`, `feat/...`), open a PR, squash-merge it, delete the branch. A push to `main` deploys the site.
- **One PR per change set.** Review fixes and small related rule or doc changes go on the same PR, not in extra ones.
- **Sign off every commit** with `git commit -s`. A DCO check on the repo fails any PR with an unsigned commit. It is not a required check, but keep it green. Never rewrite or force-push existing commits just to add sign-offs without asking the owner: a sign-off is a certification in the owner's name.
- **Titles** use `type: summary` (`chore`, `docs`, `fix`, `feat`, `ci`). A PR description says what changes on the live site, how it was verified, and what is deliberately not included.
- **CI is the Pages workflow** (`.github/workflows/pages.yml`): it runs `bundle exec jekyll build` on PRs and on `main`, using the Ruby in `.ruby-version`, which must stay the Ruby actually used locally. It deploys only from `main`.

### Removing or replacing a site feature (REQUIRED procedure)

1. **Keep it restorable.** Tag `pre-cleanup` holds the state before the first cleanup. Record every removal in `docs/origins.md`: what it was, where it lived, how to revive it.
2. **Build a trustworthy baseline.** Build `main` in a clean worktree (`git worktree add <dir> main`) and the branch into a separate directory. Never reuse a leftover scratch build as the baseline: one silently held 62 files instead of 8,199.
3. **Compare file sets** (`LC_ALL=C sort`, then `comm`). Only the intended files may disappear, and nothing may appear.
4. **Run the tools in [scripts/verify/](scripts/verify/)** (see [scripts/README.md](scripts/README.md)). `refcheck.py <branch-build> --baseline <main-build>` must exit 0 (no reference that resolves on `main` may break on the branch; exit 2 means you pointed it at the wrong directory). `render_compare.py` must exit 0 on the pages the change could touch. Prove the render tool can fail before trusting a "same" (delete a needed stylesheet in a copy; it must say CHANGED). It checks the initial render only, so click-driven UI is not covered.
5. **Search the built output for the names of what you removed.** A before/after diff proves you removed what you meant to; it cannot show something you forgot to remove (a dead cart icon survived one pass this way).
6. **Count references only from live code.** A grep also matches HTML comments, so a commented-out `<script>` looks like a dependency.
7. **Update `docs/origins.md`** and any CLAUDE.md or AGENTS.md text that describes the removed thing.

### Chat conventions (REQUIRED)

When you mention a pull request or issue in chat, **always make it a clickable hyperlink**, for example `[PR #103](https://github.com/HogJonny-AMZN/CO3DEX/pull/103)`. Never write a bare `#103` or "PR 103". Issues use `/issues/<n>`. Get the URL from the `gh pr create` output or `gh pr view <n> --json url`.

**Explain jargon plainly.** When you use a technical term, gloss it right away in plain language with a concrete, slightly playful image, ideally pulled from the author's own text. The author is a polymath who learns by that pause; a bare term reads as gatekeeping.

## Universal AI Agent Instructions

For universal guidelines across coding assistants (GitHub Copilot, Cursor, Windsurf, OpenAI, Claude, etc.), refer to:

- [AGENTS.md](AGENTS.md) — Master repository-wide guide for all autonomous agents
- [.github/copilot-instructions.md](.github/copilot-instructions.md) — GitHub Copilot repository instructions
