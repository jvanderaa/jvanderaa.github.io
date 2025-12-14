import os
import re
import sys

def parse_args():
    if len(sys.argv) > 1:
        return sys.argv[1]
    return "docs/posts"

def get_markdown_files(root_dir):
    markdown_files = []
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".md"):
                markdown_files.append(os.path.join(root, file))
    return markdown_files

def check_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Extract content after frontmatter
    match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if match:
        body = match.group(2)
        frontmatter_found = True
    else:
        body = content
        frontmatter_found = False

    # 2. Check for <!-- more -->
    if "<!-- more -->" in body:
        return True, 0

    # 3. Count paragraphs
    blocks = re.split(r'\n\s*\n', body.strip())
    paragraphs = [b for b in blocks if b.strip()]
    count = len(paragraphs)
    
    if count > 2:
        return False, count
    
    return True, count

def main():
    search_dir = parse_args()
    print(f"Scanning directory: {search_dir}")
    
    files = get_markdown_files(search_dir)
    print(f"Found {len(files)} markdown files.")
    
    failures = []
    
    for file in files:
        passed, count = check_file(file)
        if not passed:
            failures.append((file, count))
            
    if failures:
        print("\nERROR: The following files have more than 2 paragraphs but are missing the '<!-- more -->' tag:\n")
        for f, c in failures:
            print(f"  - {f} (Paragraphs: {c})")
        print("\nPlease add '<!-- more -->' to these posts to define the summary break.")
        sys.exit(1)
    else:
        print("\nAll files passed the check!")
        sys.exit(0)

if __name__ == "__main__":
    main()
