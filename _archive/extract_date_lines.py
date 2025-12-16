import os
import re

def extract_date_line(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("date:"):
                print(f"File: {file_path}, Date Line: {line.strip()}")
                break

def process_directory(directory_path):
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".md"):  # Assuming blog files are markdown files
                file_path = os.path.join(root, file)
                extract_date_line(file_path)

# Path to the directory containing your blog files
blog_directory = 'docs/posts'
process_directory(blog_directory)
