#!/bin/bash
# Generate SVG files from Mermaid diagrams
# This script can be run separately if mmdc works in your environment
# Otherwise, the site will use client-side rendering

set -e

DOCS_DIR="../docs"
STATIC_DIR="static/images/diagrams"

mkdir -p "$STATIC_DIR"

echo "Extracting Mermaid diagrams..."

# Extract all mermaid blocks and convert them
find "$DOCS_DIR" -name "*.md" -type f | while read -r file; do
    echo "Processing: $(basename "$file")"
    
    # Extract mermaid blocks and convert each one
    awk '/```mermaid/,/```/ {
        if (/```mermaid/) { in_block=1; next }
        if (/```/ && in_block) { in_block=0; print "---DIAGRAM_END---"; next }
        if (in_block) print
    }' "$file" | {
        diagram_num=0
        diagram_content=""
        
        while IFS= read -r line; do
            if [ "$line" = "---DIAGRAM_END---" ]; then
                if [ -n "$diagram_content" ]; then
                    diagram_num=$((diagram_num + 1))
                    
                    # Generate hash for filename
                    hash=$(echo "$diagram_content" | md5 | cut -c1-12)
                    svg_file="$STATIC_DIR/diagram-$hash.svg"
                    
                    if [ -f "$svg_file" ]; then
                        echo "  ✓ Cached: diagram-$hash.svg"
                    else
                        echo "  → Converting diagram $diagram_num..."
                        
                        # Create temp file
                        tmp_file=$(mktemp).mmd
                        echo "$diagram_content" > "$tmp_file"
                        
                        # Try to convert with timeout
                        if timeout 5 mmdc -i "$tmp_file" -o "$svg_file" -b transparent -q 2>/dev/null; then
                            echo "  ✓ Created: diagram-$hash.svg"
                        else
                            echo "  ✗ Failed: diagram $diagram_num (will use client-side rendering)"
                        fi
                        
                        rm -f "$tmp_file"
                    fi
                    
                    diagram_content=""
                fi
            else
                diagram_content="$diagram_content$line"$'\n'
            fi
        done
    }
done

echo ""
echo "Done! Generated SVGs are in $STATIC_DIR/"
echo "Note: Failed diagrams will use client-side rendering automatically."
