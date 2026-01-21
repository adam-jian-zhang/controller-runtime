#!/usr/bin/env python3
import re
from pathlib import Path

DOCS_DIR = Path("/Users/adamz/work/community/k8s/controller-runtime/local/docs")
CONTENT_DIR = Path("/Users/adamz/work/community/k8s/controller-runtime/local/site/content/docs")

CONTENT_DIR.mkdir(parents=True, exist_ok=True)

for doc_file in sorted(DOCS_DIR.glob("*.md")):
    if doc_file.name in ['SUMMARY.md', 'INDEX.md']:
        continue
    
    print(f"Processing {doc_file.name}...")
    
    with open(doc_file, 'r') as f:
        content = f.read()
    
    title_match = re.match(r'^# (.+)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else doc_file.stem
    content = re.sub(r'^# .+$\n', '', content, count=1, flags=re.MULTILINE)
    
    weight_match = re.match(r'^(\d+)', doc_file.name)
    weight = int(weight_match.group(1)) if weight_match else 100
    
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
