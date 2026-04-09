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

This is a **Jekyll 4.x static blog** based on the devlopr-jekyll theme, hosted at <https://www.co3dex.com>. It is a pure static site — no backend, no database.

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
| `life` | `categories/life.md` |
| `python` | `categories/python.md` |
| `techart` | `categories/techart.md` |

Update this table when adding a new category.

### How layouts and includes connect

- `_layouts/post.html` — wraps all blog posts; includes `blog_post_article.html`, `blog_sidebar.html`, `blog_post_comments.html`
- `_includes/blog_post_article.html` — renders post content, category links, share buttons
- `_includes/blog_sidebar.html` — sidebar with recent posts, categories, author info
- `_includes/head.html` — SEO tags via `jekyll-seo-tag`; reads `thumbnail`, `keywords`, and `description` from post front matter
- `_layouts/home.html` — paginated blog index (uses `jekyll-paginate`, 4 posts/page)

### Authors

Author pages live in `_authors/<slug>.md` and are rendered via `_layouts/author.html`. Posts reference authors by the `author:` field matching the author's filename slug.

### Deployment

The `DEPLOY_STRATEGY` file controls CI/CD target (`none`, `gh-pages`, or `firebase`). The site currently builds to `./build/`. Docker Compose files exist for containerized dev/prod if needed.
