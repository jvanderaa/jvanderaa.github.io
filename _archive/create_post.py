import datetime
import os
import re
import sys

def slugify(text):
    text = text.lower()
    return re.sub(r'[^a-z0-9]+', '-', text).strip('-')

def to_pascal_case(text):
    # Remove non-alphanumeric characters but keep spaces to split
    clean_text = re.sub(r'[^a-zA-Z0-9 ]', '', text)
    return "".join(x.capitalize() for x in clean_text.split())

def main():
    # 1. Prompt for Title
    title = input("Enter the blog post Title: ").strip()
    if not title:
        print("Title is required.")
        sys.exit(1)

    # 2. Prompt for Tags
    tags_input = input("Enter Tags (comma separated): ").strip()
    tags = [t.strip() for t in tags_input.split(',') if t.strip()]

    # 3. Determine Date and Defaults
    today = datetime.date.today()
    date_str = today.strftime("%Y-%m-%d")
    year_str = str(today.year)
    
    default_authors = ["jvanderaa"]
    default_comments = "true"
    default_toc = "true"
    default_categories = ["automation"]

    # 4. Generate Slug and Folder Name
    slug = slugify(title)
    folder_name = to_pascal_case(title)
    
    # Allow overriding folder name if needed (optional, keeping it simple as requested)
    # But let's print them for verification
    print(f"\nConfiguration:")
    print(f"Title: {title}")
    print(f"Date: {date_str}")
    print(f"Slug: {slug}")
    print(f"Folder Name: {folder_name}")
    print(f"Tags: {tags}")
    
    confirm = input("\nProceed with creation? (y/n): ").lower()
    if confirm != 'y':
        print("Cancelled.")
        sys.exit(0)

    # 5. Create Directory Structure
    # Assuming script is run from project root, or we find the root relative to this script
    # The user said "docs/posts/..." so we assume the CWD is the project root.
    base_dir = os.path.join(os.getcwd(), "docs", "posts", year_str, folder_name)
    
    if os.path.exists(base_dir):
        print(f"Error: Directory {base_dir} already exists.")
        sys.exit(1)
        
    os.makedirs(base_dir)
    print(f"Created directory: {base_dir}")

    # 6. Create Content
    frontmatter = [
        "---",
        f"authors: {default_authors}".replace("'", ""), # minimalistic formatting
        f"comments: {default_comments}",
        f"date: {date_str}",
        f"slug: {slug}",
        "categories:"
    ]
    for cat in default_categories:
        frontmatter.append(f"- {cat}")
    
    frontmatter.append(f'title: "{title}"')
    frontmatter.append(f"toc: {default_toc}")
    
    if tags:
        frontmatter.append("tags:")
        for tag in tags:
            frontmatter.append(f"- {tag}")
    
    frontmatter.append("---")
    frontmatter.append("")
    frontmatter.append("Content goes here...")
    frontmatter.append("")
    frontmatter.append("<!-- more -->")
    frontmatter.append("")
    
    file_content = "\n".join(frontmatter)
    file_path = os.path.join(base_dir, "index.md")
    
    with open(file_path, "w") as f:
        f.write(file_content)
        
    print(f"Created file: {file_path}")

if __name__ == "__main__":
    main()
