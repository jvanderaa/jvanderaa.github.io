import os
import re

def update_date_format(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Regular expression to match the date field with time and timezone
    date_pattern = re.compile(r'(date:\s*)(\d{4}-\d{2}-\d{2})\s+\d{2}:\d{2}:\d{2}\+\d{2}:\d{2}')
    updated_content = date_pattern.sub(r'\1\2', content)
    
    # Regular expression to match the date field with time (no timezone)
    date_pattern_no_timezone = re.compile(r'(date:\s*)(\d{4}-\d{2}-\d{2})\s+\d{2}:\d{2}:\d{2}')
    updated_content = date_pattern_no_timezone.sub(r'\1\2', updated_content)

    with open(file_path, 'w') as file:
        file.write(updated_content)

def process_directory(directory_path):
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".md"):  # Assuming blog files are markdown files
                file_path = os.path.join(root, file)
                update_date_format(file_path)
                print(f"Updated {file_path}")

# Path to the directory containing your blog files
blog_directory = 'docs/posts'
process_directory(blog_directory)
