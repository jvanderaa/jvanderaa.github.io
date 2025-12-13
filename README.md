# Josh VanDeraa Blog Site

Definition of the blog site.

## Development

### Creating a New Post

To create a new blog post, run the `create_post.py` script from the root of the repository:

```bash
python3 create_post.py
```

This interactive script will:
1. Prompt you for the **Title**.
2. Prompt for **Tags** (comma-separated).
3. Generate the directory structure and file path based on the current year and a pascal-cased version of the title.
4. Create the `index.md` file with the appropriate frontmatter (Authors, Date, Categories, etc.).

Once run, you can find your new post in `docs/posts/<YYYY>/<Title>/index.md`.
