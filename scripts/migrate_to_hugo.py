import os
import re
import yaml
import sys
from datetime import datetime

# Configuration
CONTENT_DIR = "content"
POSTS_DIR = os.path.join(CONTENT_DIR, "posts")

# Regex patterns
ADMONITION_REGEX = re.compile(r'!!!\s+(\w+)(?:\s+"(.*?)")?')
TAB_REGEX = re.compile(r'===\s+"(.*?)"')
SOCIAL_SHARE_REGEX = re.compile(r'\[Share on .*?\]\(.*?\)\{ \.custom-share-button \}')
MORE_TAG_REGEX = re.compile(r'<!-- more -->')

# Icon mapping (Example - extend as needed)
ICON_MAP = {
    ":material-wifi:": "📶",
    ":simple-ansible:": "Ansible",
    ":simple-jenkins:": "Jenkins",
    ":material-security:": "🔒",
    ":fontawesome-brands-linkedin-in:": "LinkedIn",
    ":simple-x:": "X",
    ":simple-facebook:": "Facebook",
    ":fontawesome-brands-mastodon:": "Mastodon",
    ":fontawesome-brands-bluesky:": "Bluesky"
}

def convert_admonitions(content):
    """
    Converts MkDocs Admonitions (!!! type "Title") to Hugo/Congo shortcodes.
    """
    lines = content.split('\n')
    new_lines = []
    
    # Admonition Stack: Stores (indent_level, type)
    stack = []
    
    for line in lines:
        stripped_line = line.strip()
        current_indent = len(line) - len(line.lstrip())
        
        match = ADMONITION_REGEX.match(stripped_line)
        
        if match:
            # New admonition detected.
            # Check if we need to close existing ones based on indentation.
            while stack and current_indent <= stack[-1]:
                new_lines.append(f'{{{{< /alert >}}}}')
                stack.pop()
            
            type_ = match.group(1)
            title = match.group(2)
            
            # Map types
            if type_ == "note": type_ = "neutral" 
            elif type_ == "info": type_ = "info"
            elif type_ == "tip": type_ = "success"
            elif type_ == "warning": type_ = "warning"
            elif type_ == "danger": type_ = "danger"
            elif type_ == "bug": type_ = "danger"
            elif type_ == "quote": type_ = "neutral" 
            else: type_ = "neutral"
            
            opening = f'{{{{< alert "{type_}" >}}}}'
            if title:
                opening += f"\n**{title}**\n"
            
            new_lines.append(opening)
            stack.append(current_indent)
            continue
        
        # Not a new admonition. Check if we need to close existing ones.
        if stack:
            # If line is not empty and indent is <= last stack item, close it.
            if stripped_line != "" and current_indent <= stack[-1]:
                while stack and current_indent <= stack[-1]:
                    new_lines.append(f'{{{{< /alert >}}}}')
                    stack.pop()
                new_lines.append(line)
            else:
                # Inside admonition.
                # Remove indentation corresponding to the stack level?
                # Usually standard indent is 4 spaces.
                # If we have nested, logic is tricky.
                # Simple approach: Deduct 4 chars if possible, or just print as is if it looks okay.
                # To be safe and preserve nested code blocks:
                dedented_line = line[4:] if line.startswith("    ") else line.lstrip()
                # Actually, standard mkdocs indent is 4 chars per level.
                # We should probably strip `current_indent` - `stack[-1]`? No, that's not right.
                # Let's just strip 4 spaces if it starts with them.
                new_lines.append(dedented_line)
        else:
            new_lines.append(line)
            
    # Close any remaining at end of file
    while stack:
        new_lines.append(f'{{{{< /alert >}}}}')
        stack.pop()
        
    return '\n'.join(new_lines)

def convert_shortcodes(content):
    # Convert Tabs
    # MkDocs: === "Tab Title"
    # Hugo: {{< tab "Tab Title" >}} ... {{< /tab >}} (Needs a parent {{< tabs >}})
    # This is complex because tabs need a parent wrapper.
    # For now, let's just make them bold headers or try to wrap them.
    # A simpler fallback for tabs: Just make them Headers.
    content = TAB_REGEX.sub(r'### \1', content)
    
    # Convert More Tag
    content = MORE_TAG_REGEX.sub(r'<!--more-->', content)
    
    # Convert Icons
    for code, clean in ICON_MAP.items():
        content = content.replace(code, clean)
        
    # Remove social share injections (handled by theme)
    # The regex might need to be multiline or robust
    # content = SOCIAL_SHARE_REGEX.sub('', content) 
    
    return content

def process_frontmatter(fm):
    """
    Update frontmatter for Hugo/Congo.
    """
    new_fm = fm.copy()
    
    # Author
    if 'authors' in fm:
        authors = fm['authors']
        if isinstance(authors, list) and len(authors) > 0:
            new_fm['author'] = authors[0] # Take first
            # Or use taxonomy: new_fm['authors'] = authors
        del new_fm['authors']
        
    # Comments
    if 'comments' in fm:
        if fm['comments'] is True:
            # Congo uses params.showComments = true
            if 'params' not in new_fm:
                new_fm['params'] = {}
            new_fm['params']['showComments'] = True
        del new_fm['comments']
        
    # Created/Date
    # If date is missing, infer? Most possess it.
    
    return new_fm

def migrate_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split Frontmatter
    parts = re.split(r'^---\s*$', content, maxsplit=2, flags=re.MULTILINE)
    
    if len(parts) >= 3:
        # Has frontmatter
        raw_fm = parts[1]
        body = parts[2]
        
        try:
            fm = yaml.safe_load(raw_fm)
            if fm:
                new_fm = process_frontmatter(fm)
                
                # Convert Body
                new_body = convert_admonitions(body)
                new_body = convert_shortcodes(new_body)
                
                # Reassemble
                new_content = "---\n" + yaml.dump(new_fm, sort_keys=False, allow_unicode=True) + "---\n" + new_body
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Migrated: {filepath}")
                
        except yaml.YAMLError as e:
            print(f"Error parsing YAML in {filepath}: {e}")
    else:
        print(f"No frontmatter found in {filepath}")

def main():
    print("Starting migration...")
    for root, dirs, files in os.walk(CONTENT_DIR):
        for file in files:
            if file.endswith(".md"):
                migrate_file(os.path.join(root, file))
    print("Migration complete.")

if __name__ == "__main__":
    main()
