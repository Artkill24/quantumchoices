#!/usr/bin/env python3
"""
QuantumChoices - Mock Data Generator
Genera dati di esempio per test e demo
"""

import json
import random
import uuid
from datetime import datetime, timedelta
import os

class MockDataGenerator:
    def __init__(self):
        self.categories = ['tech', 'home', 'fitness', 'kitchen', 'fashion', 'gaming']
        self.brands = ['Apple', 'Samsung', 'Sony', 'LG', 'Nike', 'Adidas', 'Dyson', 'KitchenAid']
        
    def generate_products(self, count=100):
        """Genera prodotti mock"""
        products = []
        
        for i in range(count):
            category = random.choice(self.categories)
            brand = random.choice(self.brands)
            
            product = {
                'asin': f'B{str(random.randint(10**8, 10**9-1)).zfill(9)}',
                'title': f'{brand} {self.get_product_name(category)} {random.randint(1, 99)}',
                'category': category,
                'price': round(random.uniform(29.99, 999.99), 2),
                'original_price': round(random.uniform(50.0, 1200.0), 2),
                'rating': round(random.uniform(3.5, 5.0), 1),
                'review_count': random.randint(50, 5000),
                'quantum_score': round(random.uniform(6.0, 10.0), 1),
                'features': self.get_product_features(category),
                'description': f'Eccellente {category} di {brand} con caratteristiche avanzate',
                'image_url': f'https://via.placeholder.com/400x400?text={category}',
                'availability': random.choice(['In Stock', 'Limited', 'Pre-order']),
                'shipping': random.choice(['Prime', 'Standard', 'Express']),
                'seller': random.choice(['Amazon', brand, 'Third Party']),
                'last_updated': datetime.now().isoformat(),
                'trending': random.choice([True, False]),
                'deal': random.choice([True, False]) if random.random() < 0.3 else False
            }
            
            # Calcola sconto
            if product['original_price'] > product['price']:
                discount = round(((product['original_price'] - product['price']) / product['original_price']) * 100)
                product['discount_percentage'] = discount
            
            products.append(product)
        
        return products
    
    def get_product_name(self, category):
        """Genera nomi prodotti per categoria"""
        names = {
            'tech': ['MacBook', 'iPhone', 'Galaxy', 'Monitor', 'Laptop', 'Tablet', 'Smartwatch'],
            'home': ['Aspirapolvere', 'Umidificatore', 'Diffusore', 'Lampada', 'Termostato'],
            'fitness': ['Tapis Roulant', 'Cyclette', 'Pesi', 'Yoga Mat', 'Protein Shaker'],
            'kitchen': ['Friggitrice', 'Robot Cucina', 'Frullatore', 'Caffettiera', 'Forno'],
            'fashion': ['Sneakers', 'Giacca', 'Jeans', 'T-Shirt', 'Orologio'],
            'gaming': ['Console', 'Controller', 'Headset', 'Tastiera', 'Mouse']
        }
        return random.choice(names.get(category, ['Prodotto']))
    
    def get_product_features(self, category):
        """Genera features per categoria"""
        features = {
            'tech': ['Wi-Fi 6', 'Bluetooth 5.0', 'USB-C', '4K Display', 'Touch Screen'],
            'home': ['Smart Control', 'Energy Efficient', 'Quiet Operation', 'HEPA Filter'],
            'fitness': ['Heart Rate Monitor', 'Bluetooth', 'Waterproof', 'Long Battery'],
            'kitchen': ['Stainless Steel', 'Dishwasher Safe', 'Multiple Settings', 'Timer'],
            'fashion': ['Comfortable Fit', 'Durable Material', 'Stylish Design', 'All Sizes'],
            'gaming': ['RGB Lighting', 'Mechanical Keys', '144Hz', 'Low Latency']
        }
        
        category_features = features.get(category, ['High Quality', 'Reliable', 'Modern'])
        return random.sample(category_features, min(3, len(category_features)))
    
    def generate_analytics_data(self):
        """Genera dati analytics"""
        return {
            'daily_stats': self.generate_daily_stats(),
            'conversion_funnel': self.generate_conversion_funnel(),
            'revenue_data': self.generate_revenue_data(),
            'user_behavior': self.generate_user_behavior(),
            'email_performance': self.generate_email_performance()
        }
    
    def generate_daily_stats(self):
        """Genera statistiche giornaliere"""
        days = []
        base_date = datetime.now() - timedelta(days=30)
        
        for i in range(30):
            date = base_date + timedelta(days=i)
            days.append({
                'date': date.strftime('%Y-%m-%d'),
                'visitors': random.randint(800, 2000),
                'page_views': random.randint(2000, 5000),
                'affiliate_clicks': random.randint(100, 400),
                'conversions': random.randint(20, 80),
                'revenue': round(random.uniform(150.0, 800.0), 2),
                'bounce_rate': round(random.uniform(0.3, 0.7), 2),
                'avg_session_duration': random.randint(120, 300)
            })
        
        return days
    
    def generate_conversion_funnel(self):
        """Genera dati funnel conversioni"""
        total_visitors = 10000
        return {
            'visitors': total_visitors,
            'product_views': int(total_visitors * 0.65),
            'affiliate_clicks': int(total_visitors * 0.25),
            'conversions': int(total_visitors * 0.08),
            'revenue': round(total_visitors * 0.08 * 45.50, 2)
        }
    
    def generate_revenue_data(self):
        """Genera dati revenue"""
        months = []
        base_date = datetime.now() - timedelta(days=365)
        
        for i in range(12):
            date = base_date + timedelta(days=i*30)
            months.append({
                'month': date.strftime('%Y-%m'),
                'revenue': round(random.uniform(2000.0, 8000.0), 2),
                'orders': random.randint(100, 400),
                'avg_order_value': round(random.uniform(35.0, 85.0), 2),
                'commission_rate': round(random.uniform(0.03, 0.08), 3)
            })
        
        return months
    
    def generate_user_behavior(self):
        """Genera dati comportamento utenti"""
        return {
            'top_categories': [
                {'category': 'tech', 'views': 3245, 'conversions': 127},
                {'category': 'home', 'views': 2876, 'conversions': 98},
                {'category': 'fitness', 'views': 2234, 'conversions': 89},
                {'category': 'kitchen', 'views': 1998, 'conversions': 76}
            ],
            'device_breakdown': {
                'mobile': 0.68,
                'desktop': 0.25,
                'tablet': 0.07
            },
            'traffic_sources': {
                'organic': 0.45,
                'direct': 0.22,
                'social': 0.18,
                'email': 0.15
            }
        }
    
    def generate_email_performance(self):
        """Genera dati performance email"""
        campaigns = []
        
        campaign_types = ['newsletter', 'product_alert', 'promotional', 'reengagement']
        
        for campaign_type in campaign_types:
            campaigns.append({
                'type': campaign_type,
                'sent': random.randint(5000, 15000),
                'delivered': random.randint(4800, 14500),
                'opened': random.randint(1200, 4000),
                'clicked': random.randint(150, 800),
                'conversions': random.randint(20, 120),
                'revenue': round(random.uniform(500.0, 2500.0), 2),
                'last_sent': (datetime.now() - timedelta(days=random.randint(1, 7))).isoformat()
            })
        
        return campaigns
    
    def generate_subscribers(self, count=1000):
        """Genera subscribers email"""
        subscribers = []
        
        for i in range(count):
            signup_date = datetime.now() - timedelta(days=random.randint(1, 365))
            last_activity = signup_date + timedelta(days=random.randint(0, 30))
            
            subscriber = {
                'id': str(uuid.uuid4()),
                'email': f'user{i+1}@example.com',
                'name': f'User {i+1}',
                'signup_date': signup_date.isoformat(),
                'last_activity': last_activity.isoformat(),
                'engagement_score': round(random.uniform(0.1, 1.0), 2),
                'segments': random.sample(['newsletter', 'tech_enthusiasts', 'price_sensitive', 'high_engagement'], 2),
                'preferences': {
                    'categories': random.sample(self.categories, 2),
                    'frequency': random.choice(['daily', 'weekly', 'monthly']),
                    'interests': random.sample(['deals', 'reviews', 'tech_news', 'recommendations'], 2)
                },
                'status': random.choice(['active', 'inactive', 'unsubscribed']),
                'total_clicks': random.randint(0, 50),
                'total_conversions': random.randint(0, 10)
            }
            
            subscribers.append(subscriber)
        
        return subscribers
    
    def save_all_mock_data(self):
        """Salva tutti i dati mock"""
        # Assicura che le directory esistano
        os.makedirs('assets/data', exist_ok=True)
        
        print("🔄 Generating mock data...")
        
        # Genera e salva prodotti
        products = self.generate_products(150)
        
        # Organizza per categoria
        quantum_data = {
            'last_update': datetime.now().isoformat(),
            'categories': {}
        }
        
        for category in self.categories:
            category_products = [p for p in products if p['category'] == category]
            top_products = sorted(category_products, key=lambda x: x['quantum_score'], reverse=True)[:10]
            
            quantum_data['categories'][category] = {
                'top_products': top_products,
                'total_analyzed': len(category_products),
                'avg_quantum_score': round(sum(p['quantum_score'] for p in category_products) / len(category_products), 1) if category_products else 0,
                'price_range': {
                    'min': min(p['price'] for p in category_products) if category_products else 0,
                    'max': max(p['price'] for p in category_products) if category_products else 0
                }
            }
        
        with open('assets/data/quantum_data.json', 'w') as f:
            json.dump(quantum_data, f, indent=2, ensure_ascii=False)
        
        # Salva analytics
        analytics = self.generate_analytics_data()
        with open('assets/data/analytics_data.json', 'w') as f:
            json.dump(analytics, f, indent=2, ensure_ascii=False)
        
        # Salva subscribers
        subscribers = self.generate_subscribers(1200)
        with open('assets/data/subscribers.json', 'w') as f:
            json.dump([s.__dict__ if hasattr(s, '__dict__') else s for s in subscribers], f, indent=2, ensure_ascii=False)
        
        # Salva health report
        health_report = {
            'timestamp': datetime.now().isoformat(),
            'overall_score': 96.5,
            'overall_status': 'healthy',
            'metrics': {
                'availability': {'value': 99.9, 'threshold': 99.0, 'status': 'healthy'},
                'response_time': {'value': 1.2, 'threshold': 3.0, 'status': 'healthy'},
                'ai_services': {'value': 100, 'threshold': 95, 'status': 'healthy'},
                'affiliate_links': {'value': 98.5, 'threshold': 90, 'status': 'healthy'},
                'email_delivery': {'value': 97.2, 'threshold': 95, 'status': 'healthy'}
            }
        }
        
        with open('assets/data/health_report.json', 'w') as f:
            json.dump(health_report, f, indent=2)
        
        # Genera content suggestions
        content_suggestions = {
            'articles': [
                'I Migliori Smartphone 2025: Analisi Scientifica Completa',
                'Robot Aspirapolvere: Guida all\'Acquisto con AI Analysis',
                'Fitness Tech: Wearables che Cambiano la Vita',
                'Smart Home 2025: Dispositivi Essenziali per Casa Intelligente'
            ],
            'keywords': [
                'migliori smartphone 2025',
                'robot aspirapolvere recensioni',
                'fitness tracker confronto',
                'smart home dispositivi',
                'tecnologia casa intelligente'
            ],
            'video_ideas': [
                'Unboxing e Test iPhone 15 Pro Max',
                'Confronto Robot Aspirapolvere Top 5'
            ],
            'email_campaigns': [
                'Black Friday Tech Deals 2025',
                'Primavera: Rinnova Casa con Smart Devices'
            ],
            'generated_at': datetime.now().isoformat()
        }
        
        with open('assets/data/content_suggestions.json', 'w') as f:
            json.dump(content_suggestions, f, indent=2, ensure_ascii=False)
        
        print("✅ Mock data generated successfully!")
        print(f"📊 Products: {len(products)}")
        print(f"📧 Subscribers: {len(subscribers)}")
        print(f"📈 Analytics: 30 days of data")
        print(f"🏥 Health metrics: All systems operational")

def main():
    generator = MockDataGenerator()
    generator.save_all_mock_data()

if __name__ == "__main__":
    main()
