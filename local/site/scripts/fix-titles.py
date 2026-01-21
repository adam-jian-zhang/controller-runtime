#!/usr/bin/env python3

import re
from pathlib import Path

CONTENT_DIR = Path("/Users/adamz/work/community/k8s/controller-runtime/local/site/content/docs")

# Mapping of file names to simplified titles
title_mapping = {
    '00-overview': ('Architecture Overview', 'Architecture', -1),  # -1 to put at top
    '01-manager': ('Manager Package', 'Manager', 1),
    '02-controller': ('Controller Package', 'Controller', 2),
    '03-reconcile': ('Reconcile Package', 'Reconcile', 3),
    '04-builder': ('Builder Package', 'Builder', 4),
    '05-client': ('Client Package', 'Client', 5),
    '06-cache': ('Cache Package', 'Cache', 6),
    '07-source': ('Source Package', 'Source', 7),
    '08-handler': ('Handler Package', 'Handler', 8),
    '09-predicate': ('Predicate Package', 'Predicate', 9),
    '10-webhook': ('Webhook Package', 'Webhook', 10),
    '11-additional-packages': ('Additional Packages', 'Additional Packages', 11),
}

for doc_dir in CONTENT_DIR.iterdir():
    if not doc_dir.is_dir():
        continue
    
    doc_name = doc_dir.name
    index_file = doc_dir / "_index.md"
    
    if not index_file.exists():
        continue
    
    if doc_name not in title_mapping:
        continue
    
    old_title, new_title, weight = title_mapping[doc_name]
    
    # Read the file
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update title and weight
    content = re.sub(
        r'^title: ".*?"$',
        f'title: "{new_title}"',
        content,
        flags=re.MULTILINE
    )
    
    content = re.sub(
        r'^weight: \d+$',
        f'weight: {weight}',
        content,
        flags=re.MULTILINE
    )
    
    # Write back
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated {doc_name}: '{old_title}' -> '{new_title}' (weight: {weight})")

print("\nDone!")
