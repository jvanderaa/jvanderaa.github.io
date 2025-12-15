import os
import re

def extract_date(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Regular expression to match the date field
    date_pattern = re.compile(r'date:\s*(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\+\d{2}:\d{2}|\d{4}-\d{2}-\d{2})')
    match = date_pattern.search(content)
    
    if match:
        date = match.group(1)
        print(f"File: {file_path}, Date: {date}")
    else:
        print(f"File: {file_path}, Date: Not found")

def process_directory(directory_path):
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".md"):  # Assuming blog files are markdown files
                file_path = os.path.join(root, file)
                extract_date(file_path)

# Path to the directory containing your blog files
blog_directory = 'docs/posts'
process_directory(blog_directory)
