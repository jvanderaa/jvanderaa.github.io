# Josh VanDeraa Blog Site

Personal blog site migrated to Hugo with the Congo theme.

## Development

### Prerequisites

- [Hugo Extended](https://gohugo.io/installation/) (v0.120.0+ recommended)
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

### Creating a New Post

```bash
hugo new content content/posts/YYYY/YourTitle/index.md
```
