#!/usr/bin/env python3
"""
QuantumChoices - AI Product Analyzer
Approccio Einstein: Analisi scientifica basata su dati oggettivi
"""

import asyncio
import aiohttp
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import openai
import os
import requests
from bs4 import BeautifulSoup
import schedule
import time
from dataclasses import dataclass
from typing import List, Dict, Optional
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class Product:
    asin: str
    title: str
    price: float
    rating: float
    review_count: int
    category: str
    description: str
    features: List[str]
    quantum_score: float = 0.0

class QuantumAnalyzer:
    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.session = None
        self.scoring_weights = {
            'rating': 0.25,
            'review_count': 0.15,
            'price_value': 0.20,
            'feature_analysis': 0.25,
            'sentiment_score': 0.15
        }
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def analyze_trending_products(self, categories: List[str]) -> Dict:
        """Analisi prodotti trending con approccio quantistico"""
        logger.info("🔬 Avvio analisi trending products...")
        
        results = {}
        for category in categories:
            logger.info(f"📊 Analizzando categoria: {category}")
            
            # 1. Scraping dati Amazon (simulato)
            products = await self.scrape_category_products(category)
            
            # 2. Analisi AI per ogni prodotto
            analyzed_products = []
            for product in products:
                quantum_score = await self.calculate_quantum_score(product)
                product.quantum_score = quantum_score
                analyzed_products.append(product)
            
            # 3. Ranking basato su quantum score
            top_products = sorted(analyzed_products, key=lambda p: p.quantum_score, reverse=True)[:10]
            
            results[category] = {
                'products': [self.product_to_dict(p) for p in top_products],
                'analysis_timestamp': datetime.now().isoformat(),
                'total_analyzed': len(products),
                'avg_quantum_score': np.mean([p.quantum_score for p in top_products])
            }
            
        return results

    async def scrape_category_products(self, category: str) -> List[Product]:
        """Scraping responsabile con rispetto robots.txt"""
        # Simula scraping (sostituire con implementazione reale)
        logger.info(f"🕷️ Scraping {category} products...")
        
        # In produzione, usare Amazon Product Advertising API
        mock_products = [
            Product(
                asin=f"B{str(i).zfill(9)}",
                title=f"Prodotto {category} {i}",
                price=round(np.random.uniform(29.99, 299.99), 2),
                rating=round(np.random.uniform(3.5, 5.0), 1),
                review_count=int(np.random.uniform(50, 5000)),
                category=category,
                description=f"Descrizione dettagliata prodotto {i}",
                features=[f"Feature {j}" for j in range(3)]
            )
            for i in range(50)  # 50 prodotti per categoria
        ]
        
        await asyncio.sleep(1)  # Simula tempo scraping
        return mock_products

    async def calculate_quantum_score(self, product: Product) -> float:
        """Calcolo Quantum Score con AI analysis"""
        
        # 1. Score base da metriche oggettive
        rating_score = (product.rating / 5.0) * self.scoring_weights['rating']
        
        # Review count score (logaritmico)
        review_score = min(np.log10(product.review_count + 1) / 4, 1.0) * self.scoring_weights['review_count']
        
        # Price-value analysis
        category_avg_price = await self.get_category_average_price(product.category)
        price_value_score = self.calculate_price_value_score(product.price, category_avg_price)
        price_value_score *= self.scoring_weights['price_value']
        
        # 2. AI analysis delle features
        feature_score = await self.analyze_features_with_ai(product)
        feature_score *= self.scoring_weights['feature_analysis']
        
        # 3. Sentiment analysis delle recensioni
        sentiment_score = await self.analyze_review_sentiment(product.asin)
        sentiment_score *= self.scoring_weights['sentiment_score']
        
        # Quantum Score finale
        quantum_score = rating_score + review_score + price_value_score + feature_score + sentiment_score
        
        logger.info(f"📈 Quantum Score per {product.title}: {quantum_score:.2f}")
        return round(quantum_score * 10, 1)  # Scale 0-10

    async def get_category_average_price(self, category: str) -> float:
        """Calcola prezzo medio categoria"""
        # Simula database lookup
        category_averages = {
            'tech': 199.99,
            'home': 89.99,
            'fitness': 79.99,
            'kitchen': 129.99
        }
        return category_averages.get(category, 99.99)

    def calculate_price_value_score(self, price: float, avg_price: float) -> float:
        """Score basato su rapporto qualità-prezzo"""
        if price <= avg_price * 0.8:  # Ottimo valore
            return 1.0
        elif price <= avg_price * 1.2:  # Buon valore
            return 0.7
        else:  # Sopra media
            return 0.4

    async def analyze_features_with_ai(self, product: Product) -> float:
        """Analisi AI delle caratteristiche prodotto"""
        try:
            prompt = f"""
            Analizza le seguenti caratteristiche del prodotto e assegna un punteggio 0-1:
            
            Prodotto: {product.title}
            Categoria: {product.category}
            Caratteristiche: {', '.join(product.features)}
            Descrizione: {product.description}
            
            Valuta:
            - Innovazione tecnologica
            - Utilità pratica
            - Qualità costruttiva percepita
            - Completezza features
            
            Rispondi solo con un numero decimale tra 0 e 1.
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=10,
                temperature=0.1
            )
            
            score = float(response.choices[0].message.content.strip())
            return max(0.0, min(1.0, score))
            
        except Exception as e:
            logger.error(f"AI analysis error: {e}")
            return 0.5  # Default score

    async def analyze_review_sentiment(self, asin: str) -> float:
        """Sentiment analysis delle recensioni"""
        try:
            # Simula sentiment analysis
            # In produzione: scraping recensioni + NLP analysis
            sentiment_score = np.random.uniform(0.3, 0.9)
            return sentiment_score
            
        except Exception as e:
            logger.error(f"Sentiment analysis error: {e}")
            return 0.5

    async def generate_content_suggestions(self, products: List[Dict]) -> Dict:
        """Genera suggerimenti per contenuti con AI"""
        try:
            top_products = products[:5]
            
            prompt = f"""
            Basandoti su questi top 5 prodotti, genera suggerimenti per contenuti:
            
            {json.dumps([p['title'] for p in top_products], indent=2)}
            
            Genera:
            1. 3 titoli accattivanti per articoli
            2. 5 keyword SEO rilevanti
            3. 2 idee per video review
            4. Angolo unico per recensione scientifica
            
            Formato JSON.
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.7
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            logger.error(f"Content generation error: {e}")
            return {}

    def product_to_dict(self, product: Product) -> Dict:
        """Converte Product in dict per JSON"""
        return {
            'asin': product.asin,
            'title': product.title,
            'price': product.price,
            'rating': product.rating,
            'review_count': product.review_count,
            'category': product.category,
            'quantum_score': product.quantum_score,
            'features': product.features
        }

    async def save_analysis_results(self, results: Dict):
        """Salva risultati in formato utilizzabile dal sito"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Salva dati completi per backup
        with open(f'assets/data/analysis_{timestamp}.json', 'w') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        # Salva dati per sito (formato ottimizzato)
        site_data = {
            'last_update': datetime.now().isoformat(),
            'categories': {}
        }
        
        for category, data in results.items():
            site_data['categories'][category] = {
                'top_products': data['products'][:5],  # Solo top 5
                'avg_score': data['avg_quantum_score'],
                'total_analyzed': data['total_analyzed']
            }
        
        with open('assets/data/quantum_data.json', 'w') as f:
            json.dump(site_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 Risultati salvati: {len(results)} categorie analizzate")

async def main():
    """Main execution function"""
    categories = ['tech', 'home', 'fitness', 'kitchen']
    
    async with QuantumAnalyzer() as analyzer:
        logger.info("🚀 Avvio QuantumAnalyzer...")
        
        # Analisi prodotti trending
        results = await analyzer.analyze_trending_products(categories)
        
        # Salva risultati
        await analyzer.save_analysis_results(results)
        
        # Genera suggerimenti contenuti
        all_products = []
        for category_data in results.values():
            all_products.extend(category_data['products'])
        
        content_suggestions = await analyzer.generate_content_suggestions(all_products)
        
        with open('assets/data/content_suggestions.json', 'w') as f:
            json.dump(content_suggestions, f, indent=2, ensure_ascii=False)
        
        logger.info("✅ Analisi completata con successo!")

def schedule_analysis():
    """Pianifica analisi automatiche"""
    # Analisi completa ogni 6 ore
    schedule.every(6).hours.do(lambda: asyncio.run(main()))
    
    # Quick update ogni ora
    schedule.every().hour.do(lambda: asyncio.run(quick_update()))
    
    logger.info("⏰ Scheduler configurato: analisi ogni 6 ore")
    
    while True:
        schedule.run_pending()
        time.sleep(60)

async def quick_update():
    """Update veloce per dati real-time"""
    logger.info("⚡ Quick update in corso...")
    
    # Update prezzi e availability
    try:
        with open('assets/data/quantum_data.json', 'r') as f:
            data = json.load(f)
        
        # Simula update prezzi
        for category in data['categories']:
            for product in data['categories'][category]['top_products']:
                # Variazione prezzo ±5%
                price_change = np.random.uniform(-0.05, 0.05)
                product['price'] = round(product['price'] * (1 + price_change), 2)
        
        data['last_update'] = datetime.now().isoformat()
        
        with open('assets/data/quantum_data.json', 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info("✅ Quick update completato")
        
    except Exception as e:
        logger.error(f"Quick update error: {e}")

if __name__ == "__main__":
    if len(os.sys.argv) > 1 and os.sys.argv[1] == "schedule":
        schedule_analysis()
    else:
        asyncio.run(main())
