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

# Local CMS admin UI at http://localhost:4000/admin
# (available automatically when serving locally via jekyll-admin gem)
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

GitHub Pages builds and deploys from `main` using GitHub's built-in Jekyll builder (the `pages-build-deployment` run in the Actions tab), with CNAME `www.co3dex.com`. A push to `main` goes live in about a minute. No workflow in `.github/workflows/` does the deploy. Locally the site builds to `./build/`.

The builder is GitHub's pinned Jekyll with a plugin whitelist, which can differ from the Jekyll 4.x used locally. Moving to an Actions-based build is planned.

Internal repo files (`CLAUDE.md`, `AGENTS.md`, `README.md`, the SEO notes, `scripts/`, and so on) are kept out of the published site by the `exclude:` list in `_config.yml`. Add any new root-level non-site file there.

## Universal AI Agent Instructions

For universal guidelines across coding assistants (GitHub Copilot, Cursor, Windsurf, OpenAI, Claude, etc.), refer to:

- [AGENTS.md](AGENTS.md) — Master repository-wide guide for all autonomous agents
- [.github/copilot-instructions.md](.github/copilot-instructions.md) — GitHub Copilot repository instructions
