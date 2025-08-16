// QuantumChoices - Core JavaScript
class QuantumCore {
    constructor() {
        this.init();
    }

    init() {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setupCore());
        } else {
            this.setupCore();
        }
    }

    setupCore() {
        this.setupAnimations();
        this.setupStatsCounter();
        this.setupSearch();
        this.setupCategoryNavigation();
    }

    setupAnimations() {
        // Scroll animations
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                }
            });
        }, { threshold: 0.1 });

        // Observe animated elements
        document.querySelectorAll('.category-card, .product-card, .step').forEach(el => {
            observer.observe(el);
        });

        // Parallax for hero
        window.addEventListener('scroll', () => {
            const scrolled = window.pageYOffset;
            const hero = document.querySelector('.quantum-hero');
            if (hero) {
                const speed = scrolled * 0.5;
                hero.style.transform = `translateY(${speed}px)`;
            }
        });
    }

    setupStatsCounter() {
        const stats = document.querySelectorAll('.stat-number');
        stats.forEach(stat => {
            const target = parseInt(stat.dataset.count);
            this.animateCounter(stat, target);
        });
    }

    animateCounter(element, target) {
        let current = 0;
        const increment = target / 100;
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            element.textContent = Math.floor(current).toLocaleString();
        }, 20);
    }

    setupSearch() {
        const searchInput = document.getElementById('quantum-search');
        const searchBtn = document.querySelector('.search-btn');
        
        if (searchInput && searchBtn) {
            searchBtn.addEventListener('click', () => {
                this.performSearch(searchInput.value);
            });

            searchInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.performSearch(searchInput.value);
                }
            });
        }
    }

    performSearch(query) {
        if (!query.trim()) return;
        
        console.log(`🔍 Searching for: ${query}`);
        // Implementa logica di ricerca
        alert(`Ricerca per: "${query}" - Feature in development!`);
    }

    setupCategoryNavigation() {
        const categoryCards = document.querySelectorAll('.category-card');
        categoryCards.forEach(card => {
            card.addEventListener('click', () => {
                const category = card.dataset.category;
                this.showCategoryProducts(category);
            });
        });
    }

    showCategoryProducts(category) {
        console.log(`📂 Showing products for: ${category}`);
        
        // Scroll to top picks section
        const topPicks = document.getElementById('top-picks');
        if (topPicks) {
            topPicks.scrollIntoView({ behavior: 'smooth' });
        }
        
        // Highlight selected category
        document.querySelectorAll('.category-card').forEach(card => {
            card.classList.remove('selected');
        });
        
        const selectedCard = document.querySelector(`.category-card[data-category="${category}"]`);
        if (selectedCard) {
            selectedCard.classList.add('selected');
        }
    }

    trackAffiliateClick(productId) {
        console.log(`🎯 Affiliate click: ${productId}`);
        
        // Google Analytics
        if (typeof gtag !== 'undefined') {
            gtag('event', 'affiliate_click', {
                'product_id': productId,
                'event_category': 'engagement'
            });
        }
    }
}

// Initialize
const quantumCore = new QuantumCore();

// Global functions
window.quantumCore = quantumCore;
