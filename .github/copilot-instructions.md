# GitHub Copilot Instructions: CO3DEX

This repository is **CO3DEX** (<https://www.co3dex.com>), a Jekyll 4.x static blog built on the `devlopr-jekyll` theme.

## Core Rules for Copilot

1. **Date Validation (Zero Future Dates)**:
   - Jekyll silently omits posts with `date:` set in the future during build.
   - Always verify and ensure `date:` and `modified_date:` are set to today or earlier when creating or editing posts.

2. **Category Page Enforcement**:
   - `jekyll-archives` is disabled. Any `category:` used in a post MUST have a matching file at `categories/<slug>.md`.
   - Never add a post with an unmapped category without creating its corresponding category file.

3. **Front Matter Schema**:
   Ensure all posts in `_posts/` and `_drafts/` have valid YAML front matter:
   ```yaml
   ---
   layout: post
   title: "Post Title"
   summary: "Summary text"
   author: hogjonny
   date: "YYYY-MM-DD 00:00:00 -0600"
   modified_date: "YYYY-MM-DD 00:00:00 -0600"
   category: <category-slug>
   thumbnail: /assets/img/posts/YYYY-MM-DD-slug.png
   keywords: tag1,tag2
   permalink: /blog/slug/
   usemathjax: false
   ---
   ```

4. **Directory Organization**:
   - `_posts/YYYY-MM-DD-slug.md` for live published posts.
   - `_drafts/` for complete, staged posts previewed with `--drafts`.
   - `.docs/wip/` for unstructured concept drafts and thesis notes (ignored by Jekyll).
   - `_layouts/` and `_includes/` contain the Liquid template partials.

5. **Commands**:
   - Serve dev: `bundle exec jekyll serve --livereload` (or `.\scripts\serve.ps1`)
   - Build: `bundle exec jekyll build` (or `.\scripts\build.ps1`)
   - Clean: `bundle exec jekyll clean` (or `.\scripts\clean.ps1`)

For full cross-agent guidelines, see [AGENTS.md](../AGENTS.md) and [CLAUDE.md](../CLAUDE.md).
