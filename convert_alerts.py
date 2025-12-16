import os
import re

def convert_alerts(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    new_lines = []
    in_alert = False
    alert_type = ""
    alert_indent = ""

    # Regex to match start of alert: > [!TYPE] Title or > [!TYPE]- Title
    # Capture groups: 1=indent, 2=Type, 3=Foldable(-), 4=Title
    alert_start_re = re.compile(r'^(\s*)>\s*\[!(NOTE|TIP|WARNING|IMPORTANT|INFO|CAUTION)\](-?)\s*(.*)$', re.IGNORECASE)
    
    # Regex to match content of alert: > Content
    alert_content_re = re.compile(r'^(\s*)>\s?(.*)$')
    
    # Mapping
    type_map = {
        "NOTE": "circle-info",
        "INFO": "circle-info",
        "TIP": "lightbulb",
        "WARNING": "triangle-exclamation",
        "IMPORTANT": "circle-exclamation",
        "CAUTION": "triangle-exclamation"
    }

    i = 0
    while i < len(lines):
        line = lines[i]
        match = alert_start_re.match(line)
        
        if match:
            # Found alert start
            indent = match.group(1)
            raw_type = match.group(2).upper()
            is_foldable = match.group(3) == "-"
            title = match.group(4).strip()
            
            shortcode_type = type_map.get(raw_type, "circle-info")
            
            # Start shortcode
            # default title handling: bold the title if present
            new_lines.append(f'{indent}{{{{< alert "{shortcode_type}" >}}}}\n')
            if title:
                new_lines.append(f'{indent}**{title}**\n')
            
            in_alert = True
            alert_indent = indent
            i += 1
            continue
        
        if in_alert:
            # Check if line continues the blockquote
            content_match = alert_content_re.match(line)
            if content_match:
                # It is content
                # Check indentation match? Usually lenient is better
                content = content_match.group(2)
                new_lines.append(f'{alert_indent}{content}\n')
                i += 1
                continue
            else:
                # Alert ended by non-blockquote line
                new_lines.append(f'{alert_indent}{{{{< /alert >}}}}\n')
                in_alert = False
                # Process this line normally
                new_lines.append(line)
                i += 1
        else:
            new_lines.append(line)
            i += 1
            
    # If ended in alert
    if in_alert:
         new_lines.append(f'{alert_indent}{{{{< /alert >}}}}\n')

    with open(file_path, 'w') as f:
        f.writelines(new_lines)

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                convert_alerts(os.path.join(root, file))

if __name__ == "__main__":
    process_directory("content/posts")
