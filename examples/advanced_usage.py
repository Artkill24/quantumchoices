#!/usr/bin/env python3
"""
QuantumChoices - Advanced Usage Examples
Esempi di utilizzo avanzato del sistema
"""

import asyncio
import json
import os
import sys
from datetime import datetime, timedelta

def print_example(title, description):
    """Print formatted example header"""
    print(f"\n{'='*60}")
    print(f"🚀 {title}")
    print(f"{'='*60}")
    print(f"📝 {description}")
    print("-" * 60)

def example_1_custom_analysis():
    """Esempio 1: Analisi personalizzata prodotti"""
    print_example(
        "Custom Product Analysis",
        "Esempio di come personalizzare l'algoritmo di analisi"
    )
    
    print("""
# Esempio: Custom Quantum Score Algorithm

def calculate_custom_score(product, weights=None):
    if weights is None:
        weights = {
            'rating': 0.30,
            'reviews': 0.20,
            'price_value': 0.25,
            'features': 0.25
        }
    
    # Rating score (0-1)
    rating_score = product['rating'] / 5.0
    
    # Review count score (logarithmic)
    import math
    review_score = min(math.log10(product['review_count'] + 1) / 4, 1.0)
    
    # Price value score
    price_score = calculate_price_value(product['price'], product['category'])
    
    # Feature score (AI analysis)
    feature_score = analyze_features_ai(product['features'])
    
    # Calculate weighted score
    total_score = (
        rating_score * weights['rating'] +
        review_score * weights['reviews'] +
        price_score * weights['price_value'] +
        feature_score * weights['features']
    )
    
    return round(total_score * 10, 1)  # Scale to 0-10

# Usage
product = {
    'title': 'iPhone 15 Pro',
    'rating': 4.8,
    'review_count': 1250,
    'price': 1199.99,
    'category': 'tech',
    'features': ['A17 Pro chip', '48MP camera', 'Titanium design']
}

custom_score = calculate_custom_score(product)
print(f"Custom Quantum Score: {custom_score}/10")
    """)

def example_2_seasonal_campaigns():
    """Esempio 2: Campagne stagionali"""
    print_example(
        "Seasonal Campaign Automation",
        "Automazione per campagne email stagionali"
    )
    
    print("""
# Esempio: Seasonal Email Campaign

import datetime

def create_seasonal_campaign():
    current_month = datetime.datetime.now().month
    
    # Determine season and focus
    if current_month in [11, 12, 1]:  # Winter/Christmas
        season_config = {
            'name': 'Holiday Tech Gifts',
            'categories': ['tech', 'gaming'],
            'theme': 'christmas',
            'discount_focus': True,
            'urgency': 'high'
        }
    elif current_month in [6, 7, 8]:  # Summer
        season_config = {
            'name': 'Summer Fitness',
            'categories': ['fitness', 'outdoor'],
            'theme': 'summer',
            'discount_focus': False,
            'urgency': 'medium'
        }
    else:
        season_config = {
            'name': 'Monthly Best Picks',
            'categories': ['tech', 'home'],
            'theme': 'general',
            'discount_focus': False,
            'urgency': 'low'
        }
    
    return season_config

# Generate campaign content
def generate_seasonal_content(config, products):
    subject_templates = {
        'christmas': "🎄 {name}: Perfect Tech Gifts",
        'summer': "☀️ {name}: Get Ready for Summer",
        'general': "🚀 {name}: Latest Recommendations"
    }
    
    subject = subject_templates[config['theme']].format(name=config['name'])
    
    # Filter products by seasonal categories
    seasonal_products = [
        p for p in products 
        if p['category'] in config['categories']
    ]
    
    # Sort by quantum score
    top_products = sorted(
        seasonal_products, 
        key=lambda x: x['quantum_score'], 
        reverse=True
    )[:5]
    
    return {
        'subject': subject,
        'products': top_products,
        'config': config
    }

# Usage example
products = load_quantum_data()  # Your product data
campaign_config = create_seasonal_campaign()
campaign_content = generate_seasonal_content(campaign_config, products)

print(f"Campaign: {campaign_content['subject']}")
print(f"Products: {len(campaign_content['products'])}")
    """)

def example_3_ab_testing():
    """Esempio 3: A/B Testing avanzato"""
    print_example(
        "Advanced A/B Testing",
        "Sistema di A/B testing per ottimizzare conversioni"
    )
    
    print("""
# Esempio: A/B Testing Framework

class ABTestManager:
    def __init__(self):
        self.tests = {}
        self.user_variants = {}
    
    def create_test(self, test_name, variants, traffic_split=0.5):
        self.tests[test_name] = {
            'variants': variants,
            'traffic_split': traffic_split,
            'created_at': datetime.now(),
            'results': {'A': {'views': 0, 'clicks': 0}, 'B': {'views': 0, 'clicks': 0}}
        }
    
    def get_user_variant(self, user_id, test_name):
        key = f"{user_id}_{test_name}"
        
        if key not in self.user_variants:
            # Assign variant based on hash
            import hashlib
            hash_value = int(hashlib.md5(key.encode()).hexdigest(), 16)
            variant = 'A' if hash_value % 100 < 50 else 'B'
            self.user_variants[key] = variant
        
        return self.user_variants[key]
    
    def track_view(self, user_id, test_name):
        variant = self.get_user_variant(user_id, test_name)
        self.tests[test_name]['results'][variant]['views'] += 1
    
    def track_click(self, user_id, test_name):
        variant = self.get_user_variant(user_id, test_name)
        self.tests[test_name]['results'][variant]['clicks'] += 1
    
    def get_test_results(self, test_name):
        test = self.tests[test_name]
        results = {}
        
        for variant, data in test['results'].items():
            conversion_rate = (data['clicks'] / data['views']) * 100 if data['views'] > 0 else 0
            results[variant] = {
                'views': data['views'],
                'clicks': data['clicks'],
                'conversion_rate': round(conversion_rate, 2)
            }
        
        return results

# Usage
ab_manager = ABTestManager()

# Create test for CTA buttons
ab_manager.create_test('cta_button', {
    'A': 'Acquista su Amazon',
    'B': '🛒 Compra Ora - Spedizione Gratis'
})

# Track user interactions
user_id = "user_123"
variant = ab_manager.get_user_variant(user_id, 'cta_button')
ab_manager.track_view(user_id, 'cta_button')

# When user clicks
ab_manager.track_click(user_id, 'cta_button')

# Get results
results = ab_manager.get_test_results('cta_button')
print("A/B Test Results:", results)
    """)

def example_4_ml_recommendations():
    """Esempio 4: Machine Learning Recommendations"""
    print_example(
        "ML-Powered Recommendations",
        "Sistema di raccomandazioni basato su Machine Learning"
    )
    
    print("""
# Esempio: ML Recommendation Engine

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class QuantumRecommendationEngine:
    def __init__(self):
        self.products = []
        self.user_interactions = {}
        self.similarity_matrix = None
        self.vectorizer = TfidfVectorizer(stop_words='english')
    
    def add_product(self, product):
        self.products.append(product)
    
    def train_similarity_model(self):
        # Create feature vectors from product descriptions and features
        product_texts = []
        for product in self.products:
            text = f"{product['title']} {product['description']} {' '.join(product.get('features', []))}"
            product_texts.append(text)
        
        # Calculate TF-IDF matrix
        tfidf_matrix = self.vectorizer.fit_transform(product_texts)
        
        # Calculate cosine similarity
        self.similarity_matrix = cosine_similarity(tfidf_matrix)
    
    def get_similar_products(self, product_id, num_recommendations=5):
        if self.similarity_matrix is None:
            self.train_similarity_model()
        
        # Find product index
        product_index = None
        for i, product in enumerate(self.products):
            if product['id'] == product_id:
                product_index = i
                break
        
        if product_index is None:
            return []
        
        # Get similarity scores
        similarity_scores = self.similarity_matrix[product_index]
        
        # Get top similar products
        similar_indices = np.argsort(similarity_scores)[::-1][1:num_recommendations+1]
        
        return [self.products[i] for i in similar_indices]
    
    def track_user_interaction(self, user_id, product_id, interaction_type):
        if user_id not in self.user_interactions:
            self.user_interactions[user_id] = {}
        
        if product_id not in self.user_interactions[user_id]:
            self.user_interactions[user_id][product_id] = []
        
        self.user_interactions[user_id][product_id].append({
            'type': interaction_type,
            'timestamp': datetime.now()
        })
    
    def get_user_recommendations(self, user_id, num_recommendations=5):
        if user_id not in self.user_interactions:
            # New user - return top rated products
            top_products = sorted(self.products, key=lambda x: x['quantum_score'], reverse=True)
            return top_products[:num_recommendations]
        
        # Get user's interacted products
        user_products = list(self.user_interactions[user_id].keys())
        
        # Find similar products for each interacted product
        all_recommendations = []
        for product_id in user_products:
            similar = self.get_similar_products(product_id, 3)
            all_recommendations.extend(similar)
        
        # Remove duplicates and products user already interacted with
        seen = set(user_products)
        unique_recommendations = []
        for product in all_recommendations:
            if product['id'] not in seen:
                unique_recommendations.append(product)
                seen.add(product['id'])
        
        # Sort by quantum score
        unique_recommendations.sort(key=lambda x: x['quantum_score'], reverse=True)
        
        return unique_recommendations[:num_recommendations]

# Usage
rec_engine = QuantumRecommendationEngine()

# Add products
products = [
    {'id': '1', 'title': 'iPhone 15 Pro', 'description': 'Latest smartphone', 'features': ['A17 chip', '48MP camera'], 'quantum_score': 9.5},
    {'id': '2', 'title': 'MacBook Air M3', 'description': 'Lightweight laptop', 'features': ['M3 chip', 'Retina display'], 'quantum_score': 9.2},
    # ... more products
]

for product in products:
    rec_engine.add_product(product)

# Track user interaction
rec_engine.track_user_interaction('user123', '1', 'view')
rec_engine.track_user_interaction('user123', '1', 'click')

# Get recommendations
recommendations = rec_engine.get_user_recommendations('user123')
print(f"Recommendations for user123: {len(recommendations)} products")
    """)

def main():
    """Esegue tutti gli esempi"""
    print("🧬 QuantumChoices - Advanced Usage Examples")
    print("=" * 60)
    print("📚 Questa guida mostra esempi avanzati di utilizzo del sistema")
    
    examples = [
        example_1_custom_analysis,
        example_2_seasonal_campaigns,
        example_3_ab_testing,
        example_4_ml_recommendations
    ]
    
    for example_func in examples:
        try:
            example_func()
            input("\n▶️ Premi ENTER per continuare al prossimo esempio...")
        except KeyboardInterrupt:
            print("\n👋 Esempi interrotti dall'utente")
            break
        except Exception as e:
            print(f"\n❌ Errore nell'esempio: {e}")
    
    print("\n�� Esempi completati!")
    print("📖 Per ulteriori dettagli, consulta la documentazione completa")

if __name__ == "__main__":
    main()
