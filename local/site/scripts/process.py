#!/usr/bin/env python3
import re
import hashlib
import subprocess
import tempfile
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

DOCS_DIR = Path(
    "/Users/adamz/work/community/k8s/controller-runtime/local/docs")
CONTENT_DIR = Path(
    "/Users/adamz/work/community/k8s/controller-runtime/local/site/content/docs")
STATIC_DIR = Path(
    "/Users/adamz/work/community/k8s/controller-runtime/local/site/static/images/diagrams")

CONTENT_DIR.mkdir(parents=True, exist_ok=True)
STATIC_DIR.mkdir(parents=True, exist_ok=True)

# Title mapping: original title -> (simplified title, weight)
title_mapping = {
    'Controller-Runtime Architecture Overview': ('Architecture', -1),
    'Architecture Overview': ('Architecture', -1),
    'Manager Package': ('Manager', 1),
    'Controller Package': ('Controller', 2),
    'Reconcile Package': ('Reconcile', 3),
    'Builder Package': ('Builder', 4),
    'Client Package': ('Client', 5),
    'Cache Package': ('Cache', 6),
    'Source Package': ('Source', 7),
    'Handler Package': ('Handler', 8),
    'Predicate Package': ('Predicate', 9),
    'Webhook Package': ('Webhook', 10),
    'Additional Packages': ('Additional Packages', 11),
}


def fix_links(content):
    """Fix markdown links to work with Hugo"""
    # Pattern 1: [text](./XX-name.md) -> [text](/docs/XX-name/)
    content = re.sub(r'\[([^\]]+)\]\(\./(\d+-[^)]+)\.md\)',
                     r'[\1](/docs/\2/)', content)
    # Pattern 2: [text](XX-name.md) -> [text](/docs/XX-name/)
    content = re.sub(r'\[([^\]]+)\]\((\d+-[^)]+)\.md\)',
                     r'[\1](/docs/\2/)', content)
    # Pattern 3: [text](./README.md) -> [text](/)
    content = re.sub(r'\[([^\]]+)\]\(\./README\.md\)', r'[\1](/)', content)
    # Pattern 4: [text](README.md) -> [text](/)
    content = re.sub(r'\[([^\]]+)\]\(README\.md\)', r'[\1](/)', content)
    return content


def convert_mermaid_to_svg(mermaid_code, diagram_index):
    """Convert Mermaid to embedded SVG (requires pre-generated SVGs)"""
    # Generate hash for filename
    hash_obj = hashlib.md5(mermaid_code.encode())
    diagram_hash = hash_obj.hexdigest()[:12]
    svg_filename = f"diagram-{diagram_hash}.svg"
    svg_path = STATIC_DIR / svg_filename
    
    # Check if SVG exists
    if svg_path.exists() and svg_path.stat().st_size > 0:
        print(f"  ✓ Embedding SVG for diagram {diagram_index}")
        with open(svg_path, 'r') as f:
            svg_content = f.read()
        # Remove XML declaration and make it embeddable
        svg_content = re.sub(r'<\?xml[^>]*\?>\s*', '', svg_content)
        svg_content = re.sub(r'<!DOCTYPE[^>]*>\s*', '', svg_content)
        return svg_content
    
    # No SVG found - ERROR
    print(f"  ✗ ERROR: No SVG found for diagram {diagram_index} (hash: {diagram_hash})")
    print(f"    Run 'node scripts/convert-mermaid-node.js' first to generate SVGs")
    return None


def process_mermaid_diagrams(content):
    """Extract and convert all Mermaid diagrams to embedded SVG"""
    # Find all mermaid code blocks
    pattern = r'```mermaid\n(.*?)\n```'
    matches = list(re.finditer(pattern, content, flags=re.DOTALL))
    
    if not matches:
        return content
    
    print(f"  Found {len(matches)} Mermaid diagram(s)")
    
    # Convert diagrams sequentially
    diagram_results = []
    has_errors = False
    for i, match in enumerate(matches):
        svg_content = convert_mermaid_to_svg(match.group(1), i+1)
        if svg_content is None:
            has_errors = True
            # Use error placeholder
            hash_obj = hashlib.md5(match.group(1).encode())
            diagram_hash = hash_obj.hexdigest()[:12]
            diagram_results.append(f'<div class="error-diagram">ERROR: SVG not found for diagram {i+1} (hash: {diagram_hash})</div>')
        else:
            diagram_results.append(svg_content)
    
    if has_errors:
        print(f"\n  ⚠️  WARNING: Some diagrams are missing SVG files!")
        print(f"  Run: node scripts/convert-mermaid-node.js")
        print(f"  Or: make generate-svgs\n")
    
    # Replace diagrams in order
    def replace_mermaid(match):
        nonlocal replace_index
        svg_content = diagram_results[replace_index]
        replace_index += 1
        # Wrap in a styled div
        return f'<div class="mermaid-diagram">\n{svg_content}\n</div>'
    
    replace_index = 0
    content = re.sub(pattern, replace_mermaid, content, flags=re.DOTALL)
    return content


for doc_file in sorted(DOCS_DIR.glob("*.md")):
    if doc_file.name in ['SUMMARY.md', 'INDEX.md']:
        continue

    print(f"Processing {doc_file.name}...")

    with open(doc_file, 'r') as f:
        content = f.read()

    title_match = re.match(r'^# (.+)$', content, re.MULTILINE)
    original_title = title_match.group(1) if title_match else doc_file.stem

    # Apply title mapping
    if original_title in title_mapping:
        title, weight = title_mapping[original_title]
    else:
        # Fallback: use original title and extract weight from filename
        title = original_title
        weight_match = re.match(r'^(\d+)', doc_file.name)
        weight = int(weight_match.group(1)) if weight_match else 100

    content = re.sub(r'^# .+$\n', '', content, count=1, flags=re.MULTILINE)

    # Fix internal links
    content = fix_links(content)
    
    # Process Mermaid diagrams (convert to HTML divs)
    content = process_mermaid_diagrams(content)

    front_matter = f'---\ntitle: "{title}"\nweight: {weight}\n---\n\n'

    if doc_file.name == 'README.md':
        output_file = CONTENT_DIR.parent / "_index.md"
    else:
        doc_dir = CONTENT_DIR / doc_file.stem
        doc_dir.mkdir(parents=True, exist_ok=True)
        output_file = doc_dir / "_index.md"

    with open(output_file, 'w') as f:
        f.write(front_matter + content)

print("Done!")
