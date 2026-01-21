#!/usr/bin/env python3

import re
from pathlib import Path

DOCS_DIR = Path(__file__).parent.parent.parent / "docs"
CONTENT_DIR = Path(__file__).parent.parent / "content" / "docs"

# Create directories
CONTENT_DIR.mkdir(parents=True, exist_ok=True)

def get_weight(filename):
    """Extract weight from filename"""
    match = re.match(r'^(\d+)', filename)
    return int(match.group(1)) if match else 100

def process_markdown_file(input_path, output_path):
    """Process a single markdown file"""
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract title from first heading
    title_match = re.match(r'^# (.+)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else input_path.stem
    
    # Remove first heading
    content = re.sub(r'^# .+$\n', '', content, count=1, flags=re.MULTILINE)
    
    # Create front matter
    weight = get_weight(input_path.name)
    front_matter = f"""---
title: "{title}"
weight: {weight}
---

"""
    
    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(front_matter + content)

def main():
    print("Processing documentation files...")
    
    # Process each markdown file
    for doc_file in sorted(DOCS_DIR.glob("*.md")):
        filename = doc_file.name
        
        # Skip certain files
        if filename in ['SUMMARY.md', 'INDEX.md']:
            continue
        
        print(f"Processing {filename}...")
        
        # Determine output location
        if filename == 'README.md':
            output_file = CONTENT_DIR.parent / "_index.md"
        else:
            # Create directory for the doc
            doc_name = doc_file.stem
            doc_dir = CONTENT_DIR / doc_name
            doc_dir.mkdir(parents=True, exist_ok=True)
            output_file = doc_dir / "_index.md"
        
        # Process the file
        try:
            process_markdown_file(doc_file, output_file)
        except Exception as e:
            print(f"  Error processing {filename}: {e}")
            continue
    
    print("\nDocumentation processing complete!")

if __name__ == "__main__":
    main()
