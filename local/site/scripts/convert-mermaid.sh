#!/bin/bash
# Wrapper script for mmdc with timeout
# Usage: convert-mermaid.sh input.mmd output.svg

INPUT="$1"
OUTPUT="$2"
TIMEOUT=3

# Run mmdc with timeout
timeout $TIMEOUT mmdc -i "$INPUT" -o "$OUTPUT" -b transparent -q 2>/dev/null

# Check if successful
if [ -f "$OUTPUT" ] && [ -s "$OUTPUT" ]; then
    exit 0
else
    exit 1
fi
