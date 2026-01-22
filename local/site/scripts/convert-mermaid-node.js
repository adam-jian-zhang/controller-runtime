#!/usr/bin/env node
/**
 * Convert Mermaid diagrams to SVG using mmdc CLI
 * Processes diagrams sequentially with timeout handling
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { spawn } = require('child_process');

const DOCS_DIR = path.resolve(__dirname, '../../docs');
const STATIC_DIR = path.resolve(__dirname, '../static/images/diagrams');
const TIMEOUT = 10000; // 10 seconds per diagram

// Ensure directories exist
if (!fs.existsSync(STATIC_DIR)) {
    fs.mkdirSync(STATIC_DIR, { recursive: true });
}

// Extract all Mermaid diagrams
function extractMermaidDiagrams() {
    const diagrams = [];
    const files = fs.readdirSync(DOCS_DIR).filter(f => f.endsWith('.md'));
    
    for (const file of files) {
        if (file === 'SUMMARY.md' || file === 'INDEX.md') continue;
        
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

// Convert a single diagram using mmdc
function convertDiagram(diagram, index, total) {
    return new Promise((resolve) => {
        const svgPath = path.join(STATIC_DIR, `diagram-${diagram.hash}.svg`);
        
        // Skip if already exists
        if (fs.existsSync(svgPath) && fs.statSync(svgPath).size > 0) {
            console.log(`  ✓ [${index}/${total}] Cached: diagram-${diagram.hash}.svg`);
            resolve({ success: true, cached: true });
            return;
        }
        
        // Create temp file
        const tmpFile = path.join('/tmp', `mermaid-${diagram.hash}-${Date.now()}.mmd`);
        fs.writeFileSync(tmpFile, diagram.code);
        
        console.log(`  → [${index}/${total}] Converting diagram-${diagram.hash}.svg...`);
        
        // Spawn mmdc process
        const mmdc = spawn('mmdc', [
            '-i', tmpFile,
            '-o', svgPath,
            '-b', 'transparent'
        ]);
        
        let timedOut = false;
        const timer = setTimeout(() => {
            timedOut = true;
            mmdc.kill('SIGKILL');
            console.log(`  ✗ [${index}/${total}] Timeout - skipped`);
            try {
                if (fs.existsSync(tmpFile)) {
                    fs.unlinkSync(tmpFile);
                }
            } catch (e) {
                // Ignore cleanup errors
            }
            resolve({ success: false, reason: 'timeout' });
        }, TIMEOUT);
        
        mmdc.on('close', (code) => {
            clearTimeout(timer);
            
            if (timedOut) return;
            
            // Clean up temp file
            try {
                if (fs.existsSync(tmpFile)) {
                    fs.unlinkSync(tmpFile);
                }
            } catch (e) {
                // Ignore cleanup errors
            }
            
            if (code === 0 && fs.existsSync(svgPath) && fs.statSync(svgPath).size > 0) {
                console.log(`  ✓ [${index}/${total}] Created: diagram-${diagram.hash}.svg`);
                resolve({ success: true, cached: false });
            } else {
                console.log(`  ✗ [${index}/${total}] Failed (exit code: ${code})`);
                resolve({ success: false, reason: 'failed' });
            }
        });
        
        mmdc.on('error', (err) => {
            clearTimeout(timer);
            try {
                if (fs.existsSync(tmpFile)) {
                    fs.unlinkSync(tmpFile);
                }
            } catch (e) {
                // Ignore cleanup errors
            }
            console.log(`  ✗ [${index}/${total}] Error: ${err.message}`);
            resolve({ success: false, reason: 'error' });
        });
    });
}

// Main processing
async function main() {
    console.log('Extracting Mermaid diagrams...');
    const diagrams = extractMermaidDiagrams();
    console.log(`Found ${diagrams.length} diagrams\n`);
    
    if (diagrams.length === 0) {
        console.log('No diagrams to process.');
        return;
    }
    
    let converted = 0;
    let cached = 0;
    let failed = 0;
    
    // Process diagrams sequentially to avoid overwhelming mmdc
    for (let i = 0; i < diagrams.length; i++) {
        const result = await convertDiagram(diagrams[i], i + 1, diagrams.length);
        
        if (result.success) {
            if (result.cached) {
                cached++;
            } else {
                converted++;
            }
        } else {
            failed++;
        }
        
        // Small delay between conversions
        if (i < diagrams.length - 1) {
            await new Promise(resolve => setTimeout(resolve, 100));
        }
    }
    
    console.log(`\nSummary:`);
    console.log(`  Converted: ${converted}`);
    console.log(`  Cached: ${cached}`);
    console.log(`  Failed: ${failed}`);
    console.log(`  Total: ${diagrams.length}`);
    
    if (failed > 0) {
        console.log(`\n⚠️  WARNING: ${failed} diagrams failed to convert!`);
        console.log(`These will show as errors in the documentation.`);
        process.exit(1);
    } else {
        console.log(`\n✓ All diagrams converted successfully!`);
        process.exit(0);
    }
}

main().catch(err => {
    console.error('Fatal error:', err);
    process.exit(1);
});
