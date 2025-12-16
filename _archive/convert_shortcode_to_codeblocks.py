import os
import re

def convert_syntax_highlighting(base_dir):
    # Define the pattern to match the specific Hugo shortcode for bash with line numbers
    highlight_pattern = re.compile(r'{{<\s*highlight\s*bash\s*"linenos=table"\s*>}}(.*?){{<\s*/highlight\s*>\s*}}', re.DOTALL)
    # Define the replacement template for MkDocs Material theme code blocks with line numbers
    code_block_template = '```bash linenums="1"\n{}\n```'

    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)

                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Perform the replacement for the matched patterns
                converted_content = re.sub(highlight_pattern, lambda match: code_block_template.format(match.group(1).strip()), content)

                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(converted_content)

    print("Conversion complete.")

# Specify your base directory
base_directory = 'docs/posts'

convert_syntax_highlighting(base_directory)
