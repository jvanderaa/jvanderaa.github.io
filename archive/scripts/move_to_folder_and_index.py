#!/usr/bin/env python
"""Move files with dates to folder bundles.

Status: WIP - does not do anything yet.
"""
from glob import glob
import os

import frontmatter
import inflect

def snake_to_camel(snake_case):
    words = snake_case.split('_')
    p = inflect.engine()
    camel_case = ''.join(p.capitalize(word) for word in words)
    return camel_case

def main():
    markdown_files = glob(f"content/posts/**/*.markdown", recursive=True)
    md_files = glob(f"content/posts/**/*.md", recursive=True)
    print(len(markdown_files))
    print(len(md_files))
    all_files = markdown_files + md_files
    all_files.remove("content/posts/NautobotVaultSecret/index.md")
    print(len(all_files))

    for markdown_file in all_files:
        slug = markdown_file.split("-")[-1].split(".")[0]
        print(slug)
        print(snake_to_camel(slug))
        # bundle_dir = os.path.dirname(slug)


if __name__ == "__main__":
    main()
