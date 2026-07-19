# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Josh VanDeraa's personal blog (https://josh-v.com), built with Hugo and the Congo v2 theme, deployed to GitHub Pages via GitHub Actions on push to `main`. CI builds PRs with `.github/workflows/test-build.yml` (Hugo extended 0.152.2 + Dart Sass, `hugo --gc --minify`).

## Commands

```bash
hugo server                                        # local dev server at http://localhost:1313
hugo --gc --minify                                 # production build (what CI runs)
hugo new content content/posts/YYYY/YourTitle/index.md   # scaffold a new post
go run ./cmd/check-more-tag content/posts          # verify posts have a <!-- more --> summary break
```

The theme is loaded two ways: Hugo modules (`config/_default/module.toml` + `go.mod`, the active mechanism — `theme` is commented out in config.toml) and git submodules in `themes/` (`git submodule update --init --recursive` after a fresh clone). Go is required for Hugo modules to resolve.

## Content structure

- Posts are page bundles: `content/posts/<YYYY>/<PostTitle>/index.md` with a `feature.jpg`/`feature.png` cover image alongside.
- Permalinks strip the date: posts publish at `/:slug` (set `slug:` in front matter or the bundle directory name is used).
- Front matter is YAML: `date`, `title`, `summary`, `categories`, `tags`, `author: jvanderaa`, `coverAlt`, `coverCaption` (HTML attribution for Unsplash images), `params.showComments`.
- Posts longer than two paragraphs need a `<!-- more -->` tag to mark the summary break — enforced by `cmd/check-more-tag`.
- Drafts live in `content/draft/`.

## Customizations over the theme

- `layouts/shortcodes/` — `subscribe`, `tabs`/`tab`, `timeline`.
- `layouts/_default/_markup/` — render hooks for code blocks and images.
- `layouts/partials/comments.html` — giscus comments (GitHub Discussions).
- Newsletter subscribe forms POST to a Cloudflare Workers endpoint configured in `[newsletter]` in `config/_default/params.toml`.
- Admonitions come from the `hugo-admonitions` module.

## Legacy directories — do not edit

`_archive/` (old MkDocs site), `archive/` (earlier Hugo migration attempt), and `temp/` are leftovers from the MkDocs→Hugo migration, as are the MkDocs dependencies in `pyproject.toml` and the scripts in `scripts/`. The live site is built only from `content/`, `layouts/`, `assets/`, `static/`, and `config/`.
