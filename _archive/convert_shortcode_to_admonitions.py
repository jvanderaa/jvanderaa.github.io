import os
import re

def convert_alerts_to_admonitions(base_dir):
    patterns = [
        (re.compile(r'{{<\s*alert\s*"circle-info"\s*>}}(.*?){{<\s*/alert\s*>}}', re.DOTALL), '!!! info\n    {}\n'),
        (re.compile(r'{{<\s*alert\s*"triangle-exclamation"\s*>}}(.*?){{<\s*/alert\s*>}}', re.DOTALL), '!!! warning\n    {}\n'),
        (re.compile(r'{{<\s*alert\s*"comment"\s*>}}(.*?){{<\s*/alert\s*>}}', re.DOTALL), '!!! abstract\n    {}\n'),
        (re.compile(r'{{<\s*alert\s*>}}(.*?){{<\s*/alert\s*>}}', re.DOTALL), '!!! note\n    {}\n')
    ]

    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)

                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                for pattern, template in patterns:
                    content = re.sub(pattern, lambda match: template.format(match.group(1).strip()), content)

                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)

    print("Conversion complete.")

# Specify your base directory
base_directory = 'docs/posts'

convert_alerts_to_admonitions(base_directory)
