# Origins

CO3DEX started as a fork of [devlopr-jekyll](https://github.com/sujaykundu777/devlopr-jekyll) by
Sujay Kundu (MIT licensed; his copyright notice stays in [LICENSE](../LICENSE)). It has since been
modified heavily and does not track upstream.

Pass 1 of the cleanup removed everything from the theme that this site doesn't use. Nothing is
lost: the full pre-cleanup state is the git tag **`pre-cleanup`**.

```bash
git show pre-cleanup:<path>                 # read an old file
git checkout pre-cleanup -- <path>          # bring it back into the working tree
git diff pre-cleanup HEAD --stat            # everything the cleanup changed
```

## What was removed, and how to revive it

| Feature | What it was | Where it lived | Reviving it |
| ------- | ----------- | -------------- | ----------- |
| Disqus comments | Hosted comment service | `_includes/blog_post_comments.html`, `disqus_shortname` in `_config.yml` | Its mount point was already commented out, so it never showed a comment box. Planned replacement is giscus (GitHub Discussions). |
| Hyvor comments | Paid comment service | `_includes/hyvor_comments.html`, `hyvor_talk_website_id` | Needs a Hyvor account. |
| Olvy | "What's new" changelog popup for SaaS products | `_layouts/full-width.html`, `_includes/hero.html`, `olvy_*` config | Needs your own Olvy org. Low value on a blog. |
| Snipcart | E-commerce cart | `_layouts/default.html`, `_layouts/full-width.html` | Needs your own Snipcart API key. The upstream key was removed. |
| Netlify Identity / Netlify CMS | Browser-based post editor and login | `admin/`, `_includes/head.html` | `admin/config.yml` pointed at upstream's repo and needs rewriting for yours. |
| Mailchimp newsletter form | Email signup box | `_includes/blog_newsletter.html` (commented block), `mailchimp_form_url` | Needs your own Mailchimp form URL. |
| WakaTime charts | Coding-time activity charts | `_includes/coding_activity.html`, `_layouts/about-me.html` | Needs your own WakaTime share links. |
| Shop | Product pages | `_products/`, `_layouts/product.html`, `_includes/product*.html`, `shop.md` | Pairs with Snipcart. |
| About-me layout | Alternate about page with skills and coding activity | `_layouts/about-me.html`, `_includes/author_skills.html` | Superseded by `about-single-column`. |
| Theme docs | Styleguide, install guide, demo posts | `styleguide.md`, `install.md`, `_posts_archive/` | Reference only. |
| Other deploy targets | Heroku, Netlify, Firebase, nginx, Forestry, gnome-builder | `Procfile`, `netlify.toml`, `firebase.json`, `nginx/`, `.forestry/`, ... | The live site uses GitHub Pages only. |
| Upstream project files | Contributor guide, code of conduct, funding links, greeting bot | `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `.github/FUNDING.yml`, ... | `FUNDING.yml` pointed at upstream's donation links. |

Still in the tree on purpose: the Formspree contact form, the lightGallery-based gallery, the
Bootstrap-era layouts and the bower components. Those are planned for the modernization pass.
