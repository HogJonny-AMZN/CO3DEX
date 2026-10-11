# SEO Best Practices for CO3DEX

This guide outlines the SEO optimizations implemented and best practices for maintaining optimal search engine visibility.

## Implemented Optimizations

### 1. Meta Tags & Head Section
- ✅ Proper title tags with site hierarchy
- ✅ Meta descriptions (auto-generated from summaries, max 160 chars)
- ✅ Keywords meta tag (from front matter + categories + tags)
- ✅ Author meta tags
- ✅ Language and locale settings
- ✅ Viewport and character encoding
- ✅ Canonical URLs for all pages

### 2. Open Graph Tags
- ✅ og:title
- ✅ og:description (truncated to 200 chars)
- ✅ og:image with alt text
- ✅ og:url
- ✅ og:type (article vs website)
- ✅ og:locale
- ✅ article:published_time
- ✅ article:modified_time
- ✅ article:author
- ✅ article:section (from categories)
- ✅ article:tag (from tags)

### 3. Twitter Cards
- ✅ twitter:card (summary_large_image when thumbnail present)
- ✅ twitter:site and twitter:creator
- ✅ twitter:title
- ✅ twitter:description (truncated to 200 chars)
- ✅ twitter:image with alt text
- ✅ twitter:url

### 4. Structured Data (JSON-LD)
- ✅ BlogPosting schema for posts
- ✅ WebPage schema for pages
- ✅ BreadcrumbList schema for navigation
- ✅ Organization schema (publisher)
- ✅ Person schema (author)
- ✅ ImageObject schema

### 5. Technical SEO
- ✅ robots.txt file
- ✅ Sitemap (auto-generated via jekyll-sitemap plugin)
- ✅ humans.txt file
- ✅ RSS feed
- ✅ Canonical URLs
- ✅ Proper permalink structure
- ✅ Mobile-friendly viewport

## Content Creation Best Practices

### Post Front Matter Template
Every blog post should include the following front matter:

```yaml
---
layout: post
title: "Your SEO-Optimized Title (50-60 characters)"
summary: "Compelling meta description that includes primary keyword (150-160 characters)"
author: hogjonny
date: "YYYY-MM-DD HH:MM:SS -0600"
category: techart  # or python, rendering, tools, etc.
thumbnail: /assets/img/posts/your-post-slug/featured-image.png
keywords: primary-keyword,secondary-keyword,tertiary-keyword,related-term
permalink: /blog/your-post-slug/
usemathjax: false  # set to true if using math equations
modified_date: "YYYY-MM-DD HH:MM:SS -0600"  # optional, add when significantly updating
---
```

### Title Optimization
- **Length**: 50-60 characters (to avoid truncation in search results)
- **Include primary keyword** near the beginning
- **Be specific and descriptive**
- **Consider using**: How to, Guide, Tutorial, Introduction, Best Practices
- **Examples**:
  - ✅ "Python Logging Best Practices for Game Development Tools"
  - ✅ "Image-Based Lighting Setup Guide for O3DE"
  - ❌ "Logging" (too vague)
  - ❌ "Everything You Ever Wanted to Know About..." (too long & clickbait)

### Summary/Description Optimization
- **Length**: 150-160 characters (Google typically displays 155-160)
- **Include primary keyword naturally**
- **Write compelling copy** that encourages clicks
- **Include a call-to-action or value proposition**
- **Examples**:
  - ✅ "Learn how to implement defensive logging strategies in Python tools for game development. Transform fragile prototypes into production-ready applications."
  - ✅ "Master Image-Based Lighting in Open 3D Engine. Complete guide to HDR environments, skyboxes, and global illumination setup for realistic rendering."
  - ❌ "This post is about logging" (not compelling)

### Keyword Strategy
- **Primary keyword**: Main topic (1-2 words)
- **Secondary keywords**: Related concepts (2-4 terms)
- **Long-tail keywords**: Specific phrases users might search (3-5 terms)
- **Separate with commas**, no spaces after commas
- **Include 5-10 keywords** total
- **Examples**:
  - `python,logging,tools,game-development,debugging,pyside,qt`
  - `ibl,image-based-lighting,o3de,rendering,hdri,global-illumination`

### Image Optimization
1. **Thumbnails**:
   - Recommended size: 1200x630px (optimal for social sharing)
   - Format: PNG or JPG
   - File size: < 200KB for performance
   - Path: `/assets/img/posts/YYYY-MM-DD-post-slug/thumbnail.png`

2. **Content Images**:
   - Use descriptive filenames: `o3de-lighting-setup.png` not `img001.png`
   - Add alt text for accessibility and SEO
   - Compress images before uploading
   - Use appropriate format: PNG for screenshots/diagrams, JPG for photos

3. **Alt Text Best Practices**:
   ```markdown
   ![Descriptive alt text](path/to/image.png)
   ```
   - Be specific and descriptive
   - Include keywords naturally
   - ✅ "O3DE editor showing global illumination settings with HDR skybox"
   - ❌ "screenshot" or "image1"

### URL/Permalink Structure
- Use **descriptive slugs** that include primary keyword
- Keep **short and readable** (3-5 words ideal)
- Use **hyphens** to separate words, not underscores
- **Avoid**: dates in URL (already in filename), special characters, stop words
- **Examples**:
  - ✅ `/blog/python-logging-best-practices/`
  - ✅ `/blog/image-based-lighting-setup/`
  - ❌ `/blog/2026/02/25/post/`
  - ❌ `/blog/a-guide-to-the-best-practices/`

### Content Structure for SEO

#### Headings Hierarchy
- Use **one H1** per page (automatically from title)
- Use **H2 for main sections**
- Use **H3 for subsections**
- Never skip heading levels (H1 → H3)
- Include keywords in H2 headings when natural

#### Internal Linking
- Link to related posts naturally in content
- Use descriptive anchor text (not "click here")
- Aim for 2-3 internal links per 1000 words
- Update older posts to link to new content

#### Content Length
- **Tutorial/Guide**: 1500-3000 words (comprehensive)
- **How-To**: 800-1500 words (focused)
- **News/Updates**: 300-800 words (concise)
- Quality over quantity - don't add fluff

#### First Paragraph
- Include primary keyword in first 100 words
- Hook readers with value proposition
- Preview what they'll learn

## Technical Considerations

### Performance
- Images should be optimized (compressed)
- Use lazy loading for images below the fold
- Minimize CSS/JS where possible
- Enable caching (handled by hosting platform)

### Mobile Optimization
- All pages are mobile-responsive
- Test on actual devices
- Ensure images scale properly
- Verify readability of text size

### Analytics Setup
Consider adding:
- Google Analytics 4
- Google Search Console
- Monitor: traffic, popular content, search queries, click-through rates

### Schema Validation
- Test structured data: https://search.google.com/test/rich-results
- Validate Open Graph: https://developers.facebook.com/tools/debug/
- Check Twitter Cards: https://cards-dev.twitter.com/validator

## Monitoring & Maintenance

### Regular Checks
- **Weekly**: Monitor new post indexing in Search Console
- **Monthly**: Review top performing content and keywords
- **Quarterly**: Audit and update old content
- **Yearly**: Comprehensive SEO audit

### Content Updates
When significantly updating a post:
1. Add `modified_date` to front matter
2. Update meta description if scope changed
3. Add/update keywords if relevant
4. Consider refreshing images/screenshots
5. Update internal links

### Common Issues to Avoid
- ❌ Duplicate content
- ❌ Missing or duplicate meta descriptions
- ❌ Broken internal/external links
- ❌ Images without alt text
- ❌ Non-descriptive page titles
- ❌ Thin content (< 300 words without reason)
- ❌ Keyword stuffing
- ❌ Slow page load times

## Resources & Tools

### Validation Tools
- [Google Rich Results Test](https://search.google.com/test/rich-results)
- [Schema.org Validator](https://validator.schema.org/)
- [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/)
- [Twitter Card Validator](https://cards-dev.twitter.com/validator)
- [W3C Markup Validation](https://validator.w3.org/)

### SEO Tools
- Google Search Console (required)
- Google Analytics 4 (recommended)
- Bing Webmaster Tools (optional)
- Ahrefs / SEMrush (for advanced analysis)

### Learning Resources
- [Google Search Central](https://developers.google.com/search)
- [Moz Beginner's Guide to SEO](https://moz.com/beginners-guide-to-seo)
- [Schema.org Documentation](https://schema.org/)

## Quick Checklist for New Posts

Before publishing, verify:

- [ ] Title is 50-60 characters with primary keyword
- [ ] Summary is 150-160 characters and compelling
- [ ] Keywords include 5-10 relevant terms
- [ ] Thumbnail image is 1200x630px and < 200KB
- [ ] Permalink is descriptive and keyword-rich
- [ ] First paragraph includes primary keyword
- [ ] Images have descriptive alt text
- [ ] Content has proper heading hierarchy (H2, H3)
- [ ] 2-3 internal links to related content
- [ ] Content is 800+ words (for substantial posts)
- [ ] Proofread for spelling/grammar
- [ ] Mobile-friendly (test on phone)
- [ ] All links work (no 404s)

## Contact
For questions about SEO implementation, contact the site author or check the latest at [schema.org](https://schema.org/) and [Google Search Central](https://developers.google.com/search).
