#!/usr/bin/env python3

import os
import re
import hashlib
import subprocess
import tempfile
from pathlib import Path
import sys

DOCS_DIR = Path(__file__).parent.parent.parent / "docs"
CONTENT_DIR = Path(__file__).parent.parent / "content" / "docs"
STATIC_DIR = Path(__file__).parent.parent / "static" / "images" / "diagrams"

# Create directories
CONTENT_DIR.mkdir(parents=True, exist_ok=True)
STATIC_DIR.mkdir(parents=True, exist_ok=True)

def generate_hash(content):
    """Generate MD5 hash from content"""
    return hashlib.md5(content.encode()).hexdigest()[:12]

def extract_mermaid_blocks(content):
    """Extract mermaid blocks and return modified content with SVG references"""
    pattern = r'```mermaid\n(.*?)```'
    
    def replace_mermaid(match):
        mermaid_content = match.group(1)
        content_hash = generate_hash(mermaid_content)
        svg_filename = f"diagram-{content_hash}.svg"
        svg_path = STATIC_DIR / svg_filename
        
        # Create mermaid file and convert to SVG (with timeout)
        if not svg_path.exists():
            with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False) as f:
                f.write(mermaid_content)
                mmd_path = f.name
            
            try:
                print(f"  Converting diagram {svg_filename}...", end='', flush=True)
                result = subprocess.run([
                    'mmdc', '-i', mmd_path, '-o', str(svg_path),
                    '-b', 'transparent'
                ], check=True, capture_output=True, timeout=5)
                print(" done")
            except subprocess.TimeoutExpired:
                print(" timeout, skipping")
            except subprocess.CalledProcessError as e:
                print(f" failed: {e}")
            except FileNotFoundError:
                print(" mmdc not found, skipping")
            finally:
                try:
                    os.unlink(mmd_path)
                except:
                    pass
        
        # Return HTML with SVG (or placeholder if conversion failed)
        if svg_path.exists():
            return f'<div class="mermaid-diagram">\n<img src="/images/diagrams/{svg_filename}" alt="Diagram" />\n</div>\n'
        else:
            # Return mermaid code block as fallback
            return f'```mermaid\n{mermaid_content}```'
    
    return re.sub(pattern, replace_mermaid, content, flags=re.DOTALL)

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
    
    # Process mermaid diagrams
    content = extract_mermaid_blocks(content)
    
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
    print(f"Content directory: {CONTENT_DIR}")
    print(f"Diagrams directory: {STATIC_DIR}")

if __name__ == "__main__":
    main()
