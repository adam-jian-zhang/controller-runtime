#!/bin/bash

set -e

DOCS_DIR="../docs"
CONTENT_DIR="../site/content/docs"
STATIC_DIR="../site/static/images/diagrams"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Create directories
mkdir -p "$CONTENT_DIR"
mkdir -p "$STATIC_DIR"

echo "Processing documentation files..."

# Function to generate hash from content
generate_hash() {
    echo -n "$1" | md5sum | cut -d' ' -f1
}

# Function to extract and convert mermaid diagrams
process_mermaid() {
    local input_file="$1"
    local output_file="$2"
    local temp_file=$(mktemp)
    
    # Read the file
    local in_mermaid=0
    local mermaid_content=""
    local line_num=0
    
    while IFS= read -r line; do
        line_num=$((line_num + 1))
        
        # Check if we're starting a mermaid block
        if [[ "$line" =~ ^\`\`\`mermaid ]]; then
            in_mermaid=1
            mermaid_content=""
            continue
        fi
        
        # Check if we're ending a mermaid block
        if [[ $in_mermaid -eq 1 ]] && [[ "$line" =~ ^\`\`\`$ ]]; then
            # Generate hash from mermaid content
            local hash=$(generate_hash "$mermaid_content")
            local svg_file="diagram-${hash}.svg"
            local svg_path="$STATIC_DIR/$svg_file"
            
            # Create mermaid file
            local mmd_file=$(mktemp --suffix=.mmd)
            echo "$mermaid_content" > "$mmd_file"
            
            # Convert to SVG if not already exists
            if [ ! -f "$svg_path" ]; then
                echo "  Converting diagram $svg_file..."
                mmdc -i "$mmd_file" -o "$svg_path" -b transparent 2>/dev/null || echo "  Warning: Failed to convert diagram"
            fi
            
            # Replace mermaid block with SVG image
            echo "<div class=\"mermaid-diagram\">" >> "$temp_file"
            echo "<img src=\"/images/diagrams/$svg_file\" alt=\"Diagram\" />" >> "$temp_file"
            echo "</div>" >> "$temp_file"
            echo "" >> "$temp_file"
            
            rm -f "$mmd_file"
            in_mermaid=0
            mermaid_content=""
            continue
        fi
        
        # Accumulate mermaid content
        if [[ $in_mermaid -eq 1 ]]; then
            mermaid_content="${mermaid_content}${line}"$'\n'
        else
            echo "$line" >> "$temp_file"
        fi
    done < "$input_file"
    
    mv "$temp_file" "$output_file"
}

# Process each markdown file
for doc_file in "$DOCS_DIR"/*.md; do
    if [ -f "$doc_file" ]; then
        filename=$(basename "$doc_file")
        
        # Skip SUMMARY.md and INDEX.md
        if [[ "$filename" == "SUMMARY.md" ]] || [[ "$filename" == "INDEX.md" ]]; then
            continue
        fi
        
        echo "Processing $filename..."
        
        # Determine output location
        if [[ "$filename" == "README.md" ]]; then
            output_file="$CONTENT_DIR/../_index.md"
        else
            # Create directory for the doc
            doc_name="${filename%.md}"
            doc_dir="$CONTENT_DIR/$doc_name"
            mkdir -p "$doc_dir"
            output_file="$doc_dir/_index.md"
        fi
        
        # Add front matter
        {
            echo "---"
            echo "title: \"$(head -1 "$doc_file" | sed 's/^# //')\""
            echo "weight: $(echo "$filename" | grep -o '^[0-9]*' || echo '100')"
            echo "---"
            echo ""
        } > "$output_file.tmp"
        
        # Remove the first heading (title) from content
        tail -n +2 "$doc_file" >> "$output_file.tmp"
        
        # Process mermaid diagrams
        process_mermaid "$output_file.tmp" "$output_file"
        rm -f "$output_file.tmp"
    fi
done

echo "Documentation processing complete!"
