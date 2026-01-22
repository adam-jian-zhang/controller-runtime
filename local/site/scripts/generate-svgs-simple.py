#!/usr/bin/env python3
"""
Generate SVG files from Mermaid diagrams using Mermaid.ink API
This is a simple, reliable solution that doesn't require mmdc
"""

import re
import hashlib
import urllib.parse
import urllib.request
import time
from pathlib import Path

DOCS_DIR = Path(__file__).parent.parent.parent / "docs"
STATIC_DIR = Path(__file__).parent.parent / "static" / "images" / "diagrams"

STATIC_DIR.mkdir(parents=True, exist_ok=True)

def extract_mermaid_diagrams():
    """Extract all Mermaid diagrams from markdown files"""
    diagrams = []
    
    for md_file in DOCS_DIR.glob("*.md"):
        if md_file.name in ['SUMMARY.md', 'INDEX.md']:
            continue
            
        content = md_file.read_text()
        pattern = r'```mermaid\n(.*?)\n```'
        
        for match in re.finditer(pattern, content, re.DOTALL):
            mermaid_code = match.group(1)
            hash_obj = hashlib.md5(mermaid_code.encode())
            diagram_hash = hash_obj.hexdigest()[:12]
            
            diagrams.append({
                'code': mermaid_code,
                'hash': diagram_hash,
                'file': md_file.name
            })
    
    return diagrams

def convert_diagram_via_api(diagram, index, total):
    """Convert Mermaid diagram to SVG using mermaid.ink API"""
    svg_path = STATIC_DIR / f"diagram-{diagram['hash']}.svg"
    
    # Skip if already exists
    if svg_path.exists() and svg_path.stat().st_size > 0:
        print(f"  ✓ [{index}/{total}] Cached: diagram-{diagram['hash']}.svg")
        return True
    
    try:
        print(f"  → [{index}/{total}] Converting diagram-{diagram['hash']}.svg...")
        
        # Encode Mermaid code for URL
        encoded = urllib.parse.quote(diagram['code'])
        url = f"https://mermaid.ink/svg/{encoded}"
        
        # Download SVG
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            svg_content = response.read()
        
        # Save SVG
        svg_path.write_bytes(svg_content)
        
        print(f"  ✓ [{index}/{total}] Created: diagram-{diagram['hash']}.svg ({len(svg_content)} bytes)")
        time.sleep(0.5)  # Be nice to the API
        return True
        
    except Exception as e:
        print(f"  ✗ [{index}/{total}] Failed: {str(e)[:50]}")
        return False

def main():
    print("Extracting Mermaid diagrams...")
    diagrams = extract_mermaid_diagrams()
    print(f"Found {len(diagrams)} diagrams\n")
    
    if not diagrams:
        print("No diagrams found!")
        return
    
    converted = 0
    cached = 0
    failed = 0
    
    for index, diagram in enumerate(diagrams, 1):
        svg_path = STATIC_DIR / f"diagram-{diagram['hash']}.svg"
        was_cached = svg_path.exists() and svg_path.stat().st_size > 0
        
        result = convert_diagram_via_api(diagram, index, len(diagrams))
        
        if result:
            if was_cached:
                cached += 1
            else:
                converted += 1
        else:
            failed += 1
    
    print(f"\nSummary:")
    print(f"  Converted: {converted}")
    print(f"  Cached: {cached}")
    print(f"  Failed: {failed}")
    print(f"  Total: {len(diagrams)}")
    
    if failed > 0:
        print(f"\nNote: {failed} diagrams will use client-side rendering")
    
    print(f"\nSVG files saved to: {STATIC_DIR}")

if __name__ == '__main__':
    main()
