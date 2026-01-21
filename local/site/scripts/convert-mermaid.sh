#!/bin/bash

CONTENT_DIR="../content"
STATIC_DIR="../static/images/diagrams"

mkdir -p "$STATIC_DIR"

echo "Extracting and converting Mermaid diagrams..."

# Find all mermaid code blocks and convert them
find "$CONTENT_DIR" -name "*.md" -type f | while read -r file; do
    echo "Processing $file..."
    
    # Extract mermaid blocks and convert to SVG
    awk '
    BEGIN { in_mermaid=0; mermaid_content=""; file_count=0 }
    /^```mermaid/ { in_mermaid=1; mermaid_content=""; next }
    in_mermaid && /^```$/ {
        in_mermaid=0
        file_count++
        # Generate hash and create temp file
        cmd = "echo \"" mermaid_content "\" | md5sum | cut -d\" \" -f1"
        cmd | getline hash
        close(cmd)
        
        svg_file = "'$STATIC_DIR'/diagram-" substr(hash, 1, 12) ".svg"
        mmd_file = "/tmp/diagram-" file_count ".mmd"
        
        # Write mermaid content to temp file
        print mermaid_content > mmd_file
        close(mmd_file)
        
        # Convert to SVG if not exists
        if (system("test -f " svg_file) != 0) {
            system("mmdc -i " mmd_file " -o " svg_file " -b transparent 2>/dev/null")
            print "  Created " svg_file
        }
        
        system("rm -f " mmd_file)
        next
    }
    in_mermaid { mermaid_content = mermaid_content $0 "\n" }
    ' "$file"
done

echo "Mermaid diagram conversion complete!"
