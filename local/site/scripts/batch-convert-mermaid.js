#!/usr/bin/env node
/**
 * Batch convert Mermaid diagrams to SVG
 * This script processes all diagrams in parallel with proper error handling
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const crypto = require('crypto');

const DOCS_DIR = path.join(__dirname, '../../docs');
const STATIC_DIR = path.join(__dirname, '../static/images/diagrams');
const TIMEOUT = 5000; // 5 seconds per diagram

// Ensure output directory exists
if (!fs.existsSync(STATIC_DIR)) {
    fs.mkdirSync(STATIC_DIR, { recursive: true });
}

// Extract all Mermaid diagrams from markdown files
function extractMermaidDiagrams() {
    const diagrams = [];
    const files = fs.readdirSync(DOCS_DIR).filter(f => f.endsWith('.md'));
    
    for (const file of files) {
        const content = fs.readFileSync(path.join(DOCS_DIR, file), 'utf8');
        const regex = /```mermaid\n(.*?)\n```/gs;
        let match;
        
        while ((match = regex.exec(content)) !== null) {
            const mermaidCode = match[1];
            const hash = crypto.createHash('md5').update(mermaidCode).digest('hex').substring(0, 12);
            diagrams.push({
                code: mermaidCode,
                hash: hash,
                file: file
            });
        }
    }
    
    return diagrams;
}

// Convert a single diagram
function convertDiagram(diagram, index, total) {
    const svgPath = path.join(STATIC_DIR, `diagram-${diagram.hash}.svg`);
    
    // Skip if already exists
    if (fs.existsSync(svgPath) && fs.statSync(svgPath).size > 0) {
        console.log(`  ✓ [${index}/${total}] Cached: diagram-${diagram.hash}.svg`);
        return true;
    }
    
    // Create temp file
    const tmpFile = path.join('/tmp', `mermaid-${diagram.hash}.mmd`);
    fs.writeFileSync(tmpFile, diagram.code);
    
    try {
        console.log(`  → [${index}/${total}] Converting diagram-${diagram.hash}.svg...`);
        
        // Use mmdc with timeout
        execSync(
            `timeout ${TIMEOUT/1000} mmdc -i "${tmpFile}" -o "${svgPath}" -b transparent -q`,
            { stdio: 'pipe', timeout: TIMEOUT }
        );
        
        if (fs.existsSync(svgPath) && fs.statSync(svgPath).size > 0) {
            console.log(`  ✓ [${index}/${total}] Created: diagram-${diagram.hash}.svg`);
            fs.unlinkSync(tmpFile);
            return true;
        } else {
            console.log(`  ✗ [${index}/${total}] Failed: no output file`);
            fs.unlinkSync(tmpFile);
            return false;
        }
    } catch (error) {
        console.log(`  ✗ [${index}/${total}] Error: ${error.message}`);
        if (fs.existsSync(tmpFile)) fs.unlinkSync(tmpFile);
        return false;
    }
}

// Main
console.log('Extracting Mermaid diagrams...');
const diagrams = extractMermaidDiagrams();
console.log(`Found ${diagrams.length} diagrams\n`);

let converted = 0;
let cached = 0;
let failed = 0;

diagrams.forEach((diagram, index) => {
    const result = convertDiagram(diagram, index + 1, diagrams.length);
    if (result) {
        if (fs.existsSync(path.join(STATIC_DIR, `diagram-${diagram.hash}.svg`))) {
            const stats = fs.statSync(path.join(STATIC_DIR, `diagram-${diagram.hash}.svg`));
            if (stats.mtimeMs > Date.now() - 10000) {
                converted++;
            } else {
                cached++;
            }
        }
    } else {
        failed++;
    }
});

console.log(`\nSummary:`);
console.log(`  Converted: ${converted}`);
console.log(`  Cached: ${cached}`);
console.log(`  Failed: ${failed}`);
console.log(`  Total: ${diagrams.length}`);

if (failed > 0) {
    console.log(`\nNote: ${failed} diagrams will use client-side rendering`);
}

process.exit(0);
