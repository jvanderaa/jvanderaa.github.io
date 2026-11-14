# Josh VanDeraa Blog Site

Personal blog site migrated to Hugo with the Congo theme.

## Development

### Prerequisites

- [Hugo Extended](https://gohugo.io/installation/) (v0.168.0, pinned in `.tool-versions`)
- Go (for modules)

### Setup

Clone the repository with submodules to ensure the theme is installed:

```bash
git clone --recurse-submodules https://github.com/jvanderaa/jvanderaa.github.io.git
cd jvanderaa.github.io
```

If you already cloned it without submodules:

```bash
git submodule update --init --recursive
```

### Running Locally

Start the local development server:

```bash
hugo server
```

The site will be available at http://localhost:1313.

### Article sidebar

The table of contents appears as a sticky progress card on desktop and a
collapsible card above the article on smaller screens. Earlier sections receive
checkmarks as the reader scrolls, and the current section is highlighted. Jump
links work without JavaScript. The customization lives in
`layouts/_partials/toc.html`, `assets/js/reading-agenda.js`, and
`assets/css/custom.css`.

Run the sidebar behavior checks with Node.js:

```bash
node --test tests/reading-agenda.test.cjs
```

### Creating a New Post

```bash
hugo new content content/posts/YYYY/YourTitle/index.md
```

Social video exports, their build scripts, and suggested post copy live under
[`social/`](social/). See the [ChatGPT Dots teaser](social/2026/chatgpt-dots/README.md)
for an example. Hugo does not publish this directory.

## Runnable examples

The [`examples/`](examples/) directory contains editable source for examples featured
in posts. Hugo does not publish this directory. Reader downloads live alongside
their posts under `content/posts/`.

For the [OSNM Design Builder lab](examples/osnm-design-builder/README.md), regenerate
the ZIP and standalone template after editing the source:

```bash
python3 examples/osnm-design-builder/scripts/package_lab.py
```
