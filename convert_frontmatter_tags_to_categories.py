import os
import re

def replace_tags_with_category(base_dir):
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                print(f"Checking file: {file_path}")

                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                in_front_matter = False
                new_lines = []
                for line in lines:
                    if line.strip() == '---' and not in_front_matter:
                        in_front_matter = True
                        new_lines.append(line)
                    elif line.strip() == '---' and in_front_matter:
                        in_front_matter = False
                        new_lines.append(line)
                    elif in_front_matter:
                        new_line = re.sub(r'^tags:', r'categories:', line)
                        new_lines.append(new_line)
                    else:
                        new_lines.append(line)

                with open(file_path, 'w', encoding='utf-8') as f:
                    f.writelines(new_lines)

    print("Conversion complete.")

# Specify your base directory
base_directory = 'docs/posts'

replace_tags_with_category(base_directory)
