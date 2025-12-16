import os
import re

def convert_admonitions(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    new_lines = []
    in_admonition = False
    admonition_indent = 0
    admonition_type = ""
    
    # Regex for MkDocs admonitions
    # ??? type "Title" or ???+ type "Title" or !!! type "Title"
    # Matches: ??? or ???+ or !!!, space, type, space, "Title" (optional)
    start_pattern = re.compile(r'^(\s*)([\?\!]{3}\+?)\s+(\w+)(?:\s+"(.*)")?')
    
    i = 0
    while i < len(lines):
        line = lines[i]
        match = start_pattern.match(line)
        
        if match:
            indent_str = match.group(1)
            marker = match.group(2)
            atype = match.group(3).upper() # Hugo admonitions seem to prefer UPPERCASE types in syntax? Or case-insensitive. Standard is UPPER.
            title = match.group(4) or ""
            
            # Map types if necessary
            type_mapping = {
                "NOTE": "NOTE",
                "TIP": "TIP",
                "WARNING": "WARNING",
                "INFO": "INFO",
                "DANGER": "DANGER",
                "FAILURE": "ERROR",
                "BUG": "BUG", # Check if supported, otherwise INFO
                "QUESTION": "QUESTION",
                "SUCCESS": "SUCCESS",
                "EXAMPLE": "EXAMPLE",
                "QUOTE": "QUOTE",
                "ABSTRACT": "ABSTRACT",
                "SEEALSO": "TIP",
                "TLDR": "ABSTRACT",
            }
            
            final_type = type_mapping.get(atype, "NOTE") # Fallback to NOTE
            
            # Determine collapsible state
            # ??? -> collapsed (-)
            # ???+ -> expanded (default)
            # !!! -> expanded (default)
            
            suffix = ""
            if marker == "???":
                suffix = "-"
            
            # Construct the Hugo Admonition Blockquote Header
            # > [!TYPE]- Title
            # Use current indentation? 
            # Blockquotes are usually > at start of line, but can be indented.
            # If the original block was indented, we should preserve that indentation?
            # Or assume top level? 
            # Hugo/Markdown supports indented blockquotes.
            
            header = f"{indent_str}> [!{final_type}]{suffix} {title}\n"
            new_lines.append(header)
            
            # Set state
            in_admonition = True
            admonition_indent = len(indent_str)
            
            # The next lines should be indented more than admonition_indent.
            # We need to detect the indentation of the content.
            # MkDocs usually requires 4 spaces indent.
            
            i += 1
            continue

        if in_admonition:
            # Check indentation
            stripped = line.lstrip()
            current_indent = len(line) - len(stripped)
            
            # Empty lines are part of the block if consistent
            if not line.strip():
                new_lines.append(f"{' ' * admonition_indent}>\n") # Add > to empty lines to maintain blockquote
                i += 1
                continue
                
            # If indentation drops to or below definition, block ends.
            # BUT MkDocs indent is strict.
            # We expect content to be indented by 4 spaces relative to parent.
            # If current_indent <= admonition_indent, it's widely likely the end.
            
            if current_indent <= admonition_indent:
                in_admonition = False
                new_lines.append(line)
            else:
                # It is content. We need to strip the extra indentation and prefix with '> '
                # How much to strip? Typically 4 spaces.
                # Or just strip `admonition_indent + 4`?
                # Let's simple check: if it has enough indent, prefix the content with >.
                
                # Careful: The indentation inside blockquote should be maintained relative to >.
                # MkDocs:
                # ??? note
                #     Content
                #
                # Hugo:
                # > [!NOTE]
                # > Content
                
                # Use slice?
                # If we assume standard 4 space indent for the block content:
                # We remove 4 spaces from the start (after the base indent).
                
                # Indentation of content line relative to file start: current_indent
                # Indentation of marker: admonition_indent
                # Content indentation relative to marker: current_indent - admonition_indent
                
                # If relative indent >= 4, it's part of the block?
                # What if user used tabs? assuming spaces for now.
                
                # We want to replace the FIRST level of indentation (4 spaces) with '> '.
                # Example: "    Content" -> "> Content"
                # Example: "      Nested" -> ">   Nested"
                
                # Reconstruct line:
                # Prefix indent (same as marker) + "> " + content (minus 4 spaces of indent)
                
                content_indent_prefix = line[:admonition_indent]
                content_rest = line[admonition_indent:]
                
                if content_rest.startswith("    "):
                     new_line = f"{content_indent_prefix}> {content_rest[4:]}"
                elif content_rest.startswith("\t"):
                     new_line = f"{content_indent_prefix}> {content_rest[1:]}"
                else:
                    # Fallback if weird indentation: just prefix > to the stripped line?
                    # No, that loses nested indentation.
                    # Just add > and keep the line as is? 
                    # ">     Content" is valid blockquote.
                    new_line = f"{content_indent_prefix}> {content_rest}"
                
                new_lines.append(new_line)

        else:
            new_lines.append(line)
        
        i += 1

    with open(file_path, 'w') as f:
        f.writelines(new_lines)

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.md', '.markdown')):
                convert_admonitions(os.path.join(root, file))

if __name__ == "__main__":
    process_directory("content")
