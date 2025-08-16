#!/usr/bin/env node
/**
 * Build Script Einstein-Level
 * Ottimizzazioni performance e SEO
 */

const fs = require('fs').promises;
const path = require('path');
const { execSync } = require('child_process');

class QuantumBuilder {
    async build() {
        console.log('🔨 Avvio build QuantumChoices...');
        
        // 1. Crea directory dist
        await this.createDistDirectory();
        
        // 2. Copy files
        await this.copyStaticFiles();
        
        // 3. Optimize CSS
        await this.optimizeCSS();
        
        // 4. Optimize JS
        await this.optimizeJS();
        
        // 5. Generate sitemap
        await this.generateSitemap();
        
        // 6. Generate robots.txt
        await this.generateRobots();
        
        // 7. Optimize images
        await this.optimizeImages();
        
        console.log('✅ Build completato!');
    }
    
    async createDistDirectory() {
        try {
            await fs.mkdir('dist', { recursive: true });
            await fs.mkdir('dist/assets', { recursive: true });
            await fs.mkdir('dist/src', { recursive: true });
        } catch (error) {
            console.error('Error creating dist:', error);
        }
    }
    
    async copyStaticFiles() {
        const files = [
            'index.html',
            'package.json',
            'README.md'
        ];
        
        for (const file of files) {
            try {
                await fs.copyFile(file, `dist/${file}`);
            } catch (error) {
                console.log(`File ${file} not found, skipping...`);
            }
        }
        
        // Copy directories
        await this.copyDirectory('assets', 'dist/assets');
        await this.copyDirectory('src', 'dist/src');
    }
    
    async copyDirectory(src, dest) {
        try {
            await fs.mkdir(dest, { recursive: true });
            const files = await fs.readdir(src, { withFileTypes: true });
            
            for (const file of files) {
                const srcPath = path.join(src, file.name);
                const destPath = path.join(dest, file.name);
                
                if (file.isDirectory()) {
                    await this.copyDirectory(srcPath, destPath);
                } else {
                    await fs.copyFile(srcPath, destPath);
                }
            }
        } catch (error) {
            console.log(`Directory ${src} not found, skipping...`);
        }
    }
    
    async optimizeCSS() {
        try {
            const cssContent = await fs.readFile('src/css/quantum.css', 'utf8');
            
            // Minify CSS (basic)
            const minified = cssContent
                .replace(/\/\*[\s\S]*?\*\//g, '') // Remove comments
                .replace(/\s+/g, ' ') // Collapse whitespace
                .replace(/;\s*}/g, '}') // Remove last semicolon
                .trim();
            
            await fs.writeFile('dist/src/css/quantum.min.css', minified);
            console.log('📦 CSS ottimizzato');
        } catch (error) {
            console.error('CSS optimization error:', error);
        }
    }
    
    async optimizeJS() {
        try {
            // Copy and minify JS files
            const jsFiles = [
                'src/js/quantum-core.js',
                'src/js/amazon-integration.js',
                'src/js/ai-insights.js'
            ];
            
            for (const file of jsFiles) {
                try {
                    const content = await fs.readFile(file, 'utf8');
                    // Basic minification
                    const minified = content
                        .replace(/\/\*[\s\S]*?\*\//g, '')
                        .replace(/\/\/.*$/gm, '')
                        .replace(/\s+/g, ' ')
                        .trim();
                    
                    const outputFile = file.replace('.js', '.min.js').replace('src/', 'dist/src/');
                    await fs.writeFile(outputFile, minified);
                } catch (err) {
                    console.log(`File ${file} not found, skipping...`);
                }
            }
            
            console.log('📦 JavaScript ottimizzato');
        } catch (error) {
            console.error('JS optimization error:', error);
        }
    }
    
    async generateSitemap() {
        const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://quantumchoices.github.io/</loc>
        <lastmod>${new Date().toISOString()}</lastmod>
        <changefreq>daily</changefreq>
        <priority>1.0</priority>
    </url>
    <url>
        <loc>https://quantumchoices.github.io/#categories</loc>
        <lastmod>${new Date().toISOString()}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>https://quantumchoices.github.io/#methodology</loc>
        <lastmod>${new Date().toISOString()}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.6</priority>
    </url>
</urlset>`;
        
        await fs.writeFile('dist/sitemap.xml', sitemap);
        console.log('🗺️ Sitemap generata');
    }
    
    async generateRobots() {
        const robots = `User-agent: *
Allow: /

Sitemap: https://quantumchoices.github.io/sitemap.xml

# Optimize for search engines
Crawl-delay: 1

# Block unnecessary pages
Disallow: /src/
Disallow: /scripts/
Disallow: /.github/
`;
        
        await fs.writeFile('dist/robots.txt', robots);
        console.log('🤖 Robots.txt generato');
    }
    
    async optimizeImages() {
        try {
            // Placeholder per ottimizzazione immagini
            console.log('🖼️ Ottimizzazione immagini (placeholder)');
            // In produzione: usare imagemin o sharp
        } catch (error) {
            console.error('Image optimization error:', error);
        }
    }
}

async function main() {
    const builder = new QuantumBuilder();
    await builder.build();
}

if (require.main === module) {
    main();
}

module.exports = QuantumBuilder;
