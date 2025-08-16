#!/usr/bin/env node
/**
 * QuantumChoices - AI Content Generator
 * Genera automaticamente articoli, recensioni e contenuti SEO
 */

const OpenAI = require('openai');
const fs = require('fs').promises;
const path = require('path');

class QuantumContentGenerator {
    constructor() {
        this.openai = new OpenAI({
            apiKey: process.env.OPENAI_API_KEY
        });
        
        this.templates = {
            review: this.getReviewTemplate(),
            comparison: this.getComparisonTemplate(),
            guide: this.getGuideTemplate()
        };
    }

    async generateProductReview(product) {
        console.log(`📝 Generando recensione per: ${product.title}`);
        
        const prompt = `
        Scrivi una recensione scientifica e oggettiva per questo prodotto Amazon:
        
        Prodotto: ${product.title}
        Prezzo: €${product.price}
        Rating: ${product.rating}/5 (${product.review_count} recensioni)
        Quantum Score: ${product.quantum_score}/10
        Categoria: ${product.category}
        
        La recensione deve:
        - Essere lunga 800-1200 parole
        - Includere analisi tecnica approfondita
        - Menzionare pro e contro oggettivi
        - Includere sezione "Per chi è consigliato"
        - Utilizzare approccio scientifico (dati, test, misurazioni)
        - Essere SEO-ottimizzata
        - Includere link affiliate Amazon naturalmente
        
        Struttura:
        # [Titolo Accattivante]
        ## Introduzione
        ## Analisi Tecnica Dettagliata
        ## Test Pratici e Performance
        ## Pro e Contro
        ## Confronto con Alternative
        ## Conclusioni e Raccomandazioni
        
        Usa un tono professionale ma accessibile.
        `;
        
        try {
            const response = await this.openai.chat.completions.create({
                model: "gpt-4",
                messages: [{ role: "user", content: prompt }],
                max_tokens: 2000,
                temperature: 0.7
            });
            
            const content = response.choices[0].message.content;
            
            // Aggiungi metadata e affiliate links
            const enrichedContent = this.enrichContentWithSEO(content, product);
            
            // Salva file
            const filename = `review_${product.asin}_${Date.now()}.md`;
            await this.saveContent(filename, enrichedContent);
            
            return { filename, content: enrichedContent };
            
        } catch (error) {
            console.error('Errore generazione recensione:', error);
            throw error;
        }
    }

    async generateCategoryComparison(products, category) {
        console.log(`🔬 Generando confronto categoria: ${category}`);
        
        const topProducts = products.slice(0, 5);
        
        const prompt = `
        Crea un articolo di confronto scientifico per i migliori 5 prodotti ${category}:
        
        ${topProducts.map((p, i) => `
        ${i+1}. ${p.title}
           - Prezzo: €${p.price}
           - Rating: ${p.rating}/5
           - Quantum Score: ${p.quantum_score}/10
        `).join('\n')}
        
        L'articolo deve:
        - 1500-2000 parole
        - Tabella comparativa dettagliata
        - Metodologia di test spiegata
        - Vincitore per ogni categoria d'uso
        - Sezione FAQ
        - Ottimizzazione SEO per "migliori [categoria] 2025"
        
        Includi analisi di:
        - Rapporto qualità-prezzo
        - Prestazioni tecniche
        - Facilità d'uso
        - Durabilità
        - Assistenza post-vendita
        `;
        
        const response = await this.openai.chat.completions.create({
            model: "gpt-4",
            messages: [{ role: "user", content: prompt }],
            max_tokens: 3000,
            temperature: 0.6
        });
        
        const content = this.enrichContentWithSEO(response.choices[0].message.content, null, category);
        const filename = `comparison_${category}_${Date.now()}.md`;
        await this.saveContent(filename, content);
        
        return { filename, content };
    }

    async generateBuyingGuide(category) {
        console.log(`📋 Generando guida acquisto: ${category}`);
        
        const prompt = `
        Scrivi una guida completa all'acquisto per la categoria ${category}.
        
        La guida deve includere:
        - Cosa considerare prima dell'acquisto
        - Caratteristiche tecniche importanti
        - Fasce di prezzo e budget consigliati
        - Errori comuni da evitare
        - Quando conviene comprare (stagionalità)
        - Domande frequenti
        - Glossario tecnico
        
        Lunghezza: 2000-2500 parole
        Tono: Esperto ma accessibile
        SEO: Ottimizzata per "come scegliere [categoria]"
        `;
        
        const response = await this.openai.chat.completions.create({
            model: "gpt-4",
            messages: [{ role: "user", content: prompt }],
            max_tokens: 3500,
            temperature: 0.7
        });
        
        const content = this.enrichContentWithSEO(response.choices[0].message.content, null, category);
        const filename = `guide_${category}_${Date.now()}.md`;
        await this.saveContent(filename, content);
        
        return { filename, content };
    }

    enrichContentWithSEO(content, product = null, category = null) {
        const timestamp = new Date().toISOString();
        
        let frontMatter = `---
layout: post
title: "${this.extractTitle(content)}"
date: ${timestamp}
category: ${category || (product ? product.category : 'general')}
quantum_generated: true
seo_optimized: true
`;

        if (product) {
            frontMatter += `
product_asin: ${product.asin}
quantum_score: ${product.quantum_score}
affiliate_link: https://amazon.it/dp/${product.asin}?tag=quantumchoic-21
`;
        }

        frontMatter += `---

`;

        // Aggiungi disclaimer affiliate
        const disclaimer = `
> **Disclaimer**: Questo articolo contiene link affiliati Amazon. QuantumChoices può ricevere una commissione per acquisti qualificati, senza costi aggiuntivi per te. Le nostre recensioni rimangono imparziali e basate su analisi scientifica.

`;

        // Aggiungi structured data
        let structuredData = '';
        if (product) {
            structuredData = `
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Review",
  "itemReviewed": {
    "@type": "Product",
    "name": "${product.title}",
    "offers": {
      "@type": "Offer",
      "price": "${product.price}",
      "priceCurrency": "EUR"
    }
  },
  "reviewRating": {
    "@type": "Rating",
    "ratingValue": "${product.quantum_score}",
    "bestRating": "10"
  },
  "author": {
    "@type": "Organization",
    "name": "QuantumChoices"
  }
}
</script>
`;
        }

        return frontMatter + disclaimer + content + structuredData;
    }

    extractTitle(content) {
        const titleMatch = content.match(/^#\s+(.+)/m);
        return titleMatch ? titleMatch[1] : 'Articolo QuantumChoices';
    }

    async saveContent(filename, content) {
        const contentDir = path.join(__dirname, '..', 'content');
        
        try {
            await fs.mkdir(contentDir, { recursive: true });
            await fs.writeFile(path.join(contentDir, filename), content, 'utf8');
            console.log(`✅ Contenuto salvato: ${filename}`);
        } catch (error) {
            console.error('Errore salvataggio:', error);
            throw error;
        }
    }

    async generateSocialMediaPosts(products) {
        console.log('📱 Generando post social media...');
        
        const posts = [];
        
        for (const product of products.slice(0, 3)) {
            const prompt = `
            Crea 3 post social per questo prodotto:
            
            Prodotto: ${product.title}
            Quantum Score: ${product.quantum_score}/10
            
            1. Post Instagram (con emoji e hashtag)
            2. Post LinkedIn (professionale)
            3. Tweet (280 caratteri max)
            
            Ogni post deve generare engagement e includere call-to-action.
            `;
            
            const response = await this.openai.chat.completions.create({
                model: "gpt-3.5-turbo",
                messages: [{ role: "user", content: prompt }],
                max_tokens: 500,
                temperature: 0.8
            });
            
            posts.push({
                product: product.title,
                content: response.choices[0].message.content
            });
        }
        
        await this.saveContent('social_posts.json', JSON.stringify(posts, null, 2));
        return posts;
    }

    async generateEmailNewsletter(products) {
        console.log('📧 Generando newsletter...');
        
        const topProducts = products.slice(0, 5);
        
        const prompt = `
        Crea una newsletter settimanale "QuantumChoices Weekly" con:
        
        Top 5 prodotti della settimana:
        ${topProducts.map((p, i) => `${i+1}. ${p.title} (Score: ${p.quantum_score})`).join('\n')}
        
        Include:
        - Introduzione accattivante
        - Sezione "Prodotto della Settimana"
        - "Deal da non perdere"
        - "Tendenze Tech"
        - Call-to-action per il sito
        
        Formato HTML email-friendly.
        `;
        
        const response = await this.openai.chat.completions.create({
            model: "gpt-4",
            messages: [{ role: "user", content: prompt }],
            max_tokens: 2000,
            temperature: 0.7
        });
        
        const newsletter = response.choices[0].message.content;
        await this.saveContent('newsletter.html', newsletter);
        
        return newsletter;
    }

    getReviewTemplate() {
        return `
# [PRODUCT_NAME]: Recensione Scientifica Completa

## 🔬 Metodologia di Test

La nostra analisi si basa su:
- Test pratici in laboratorio
- Analisi delle specifiche tecniche
- Confronto con benchmark di categoria
- Valutazione del rapporto qualità-prezzo

## 📊 Quantum Score: [SCORE]/10

[DETAILED_ANALYSIS]

## ✅ Verdetto Finale

[CONCLUSIONS]

---
*Testato dal team QuantumChoices con metodologia scientifica*
        `;
    }

    getComparisonTemplate() {
        return `
# I Migliori [CATEGORY] 2025: Confronto Scientifico

## �� Metodologia di Test

## 📊 Tabella Comparativa

| Prodotto | Quantum Score | Prezzo | Pro | Contro |
|----------|---------------|--------|-----|--------|
[COMPARISON_TABLE]

## 🏆 Il Nostro Verdetto

[WINNER_ANALYSIS]
        `;
    }

    getGuideTemplate() {
        return `
# Come Scegliere [CATEGORY]: Guida Completa 2025

## 🎯 Cosa Considerare

## 💰 Fasce di Prezzo

## ⚠️ Errori da Evitare

## ❓ Domande Frequenti

## 📚 Glossario Tecnico
        `;
    }
}

async function main() {
    try {
        // Carica dati prodotti
        const quantumData = JSON.parse(
            await fs.readFile('assets/data/quantum_data.json', 'utf8')
        );
        
        const generator = new QuantumContentGenerator();
        
        console.log('🚀 Avvio generazione contenuti...');
        
        // Genera contenuti per ogni categoria
        for (const [category, data] of Object.entries(quantumData.categories)) {
            const products = data.top_products;
            
            // Recensione prodotto top
            await generator.generateProductReview(products[0]);
            
            // Confronto categoria
            await generator.generateCategoryComparison(products, category);
            
            // Guida acquisto
            await generator.generateBuyingGuide(category);
        }
        
        // Content per social e newsletter
        const allProducts = Object.values(quantumData.categories)
            .flatMap(cat => cat.top_products);
        
        await generator.generateSocialMediaPosts(allProducts);
        await generator.generateEmailNewsletter(allProducts);
        
        console.log('✅ Generazione contenuti completata!');
        
    } catch (error) {
        console.error('❌ Errore:', error);
        process.exit(1);
    }
}

if (require.main === module) {
    main();
}

module.exports = QuantumContentGenerator;
