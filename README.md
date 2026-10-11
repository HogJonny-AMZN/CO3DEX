# CO3DEX

Source for [www.co3dex.com](https://www.co3dex.com), a technical art blog by Jonny Galloway
(HogJonny): real-time rendering, game engines, Python tools and procedural worlds.

It is a static [Jekyll](https://jekyllrb.com/) site. No backend, no database. Posts are Markdown
files in `_posts/`.

## Run it locally

```bash
bundle install
bundle exec jekyll serve --livereload     # http://localhost:4000
bundle exec jekyll build                  # output goes to ./build
```

On Windows without `make`, the PowerShell equivalents are in `scripts/`.

## Publishing

Push to `main`. GitHub Pages builds the site and serves it at the custom domain in `CNAME`. Posts
dated in the future are silently skipped by Jekyll, so keep `date:` at today or earlier.

## Where things are

- [CLAUDE.md](CLAUDE.md) covers repo structure, post front matter, categories and the draft workflow.
- [EDITORIAL_PIPELINE.md](EDITORIAL_PIPELINE.md) covers the layered review process for turning a
  draft into a post.
- [docs/origins.md](docs/origins.md) covers where the site came from and what was removed.

## Origins

Forked from [devlopr-jekyll](https://github.com/sujaykundu777/devlopr-jekyll) by Sujay Kundu and
heavily modified since. See [docs/origins.md](docs/origins.md).

## License

MIT. See [LICENSE](LICENSE). The upstream theme's copyright notice is preserved there.
