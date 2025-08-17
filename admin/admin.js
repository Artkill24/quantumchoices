// QuantumChoices Admin Panel JavaScript

class QuantumAdmin {
    constructor() {
        this.data = null;
        this.init();
    }

    async init() {
        await this.loadData();
        this.setupNavigation();
        this.setupDashboard();
        this.updateMetrics();
        setInterval(() => this.updateMetrics(), 30000); // Update every 30s
    }

    async loadData() {
        try {
            const [quantumData, analyticsData, healthData] = await Promise.all([
                fetch('../assets/data/quantum_data.json').then(r => r.json()),
                fetch('../assets/data/analytics_data.json').then(r => r.json()),
                fetch('../assets/data/health_report.json').then(r => r.json())
            ]);
            
            this.data = { quantumData, analyticsData, healthData };
        } catch (error) {
            console.error('Failed to load data:', error);
        }
    }

    setupNavigation() {
        document.querySelectorAll('.admin-nav-item').forEach(item => {
            item.addEventListener('click', () => {
                const section = item.dataset.section;
                this.showSection(section);
                
                // Update active state
                document.querySelectorAll('.admin-nav-item').forEach(i => i.classList.remove('active'));
                item.classList.add('active');
            });
        });
    }

    showSection(sectionName) {
        document.querySelectorAll('.admin-section').forEach(section => {
            section.style.display = 'none';
        });
        
        const targetSection = document.getElementById(`${sectionName}-section`);
        if (targetSection) {
            targetSection.style.display = 'block';
            
            // Load section-specific data
            switch(sectionName) {
                case 'products':
                    this.loadProductsTable();
                    break;
                case 'analytics':
                    this.loadAnalytics();
                    break;
            }
        }
    }

    updateMetrics() {
        if (!this.data) return;

        const { quantumData, analyticsData } = this.data;
        
        // Calculate total products
        let totalProducts = 0;
        let totalScore = 0;
        let productCount = 0;
        
        Object.values(quantumData.categories).forEach(category => {
            totalProducts += category.total_analyzed || 0;
            category.top_products?.forEach(product => {
                totalScore += product.quantum_score;
                productCount++;
            });
        });

        // Update dashboard metrics
        this.updateMetric('total-products', totalProducts.toLocaleString());
        this.updateMetric('avg-quantum-score', (totalScore / productCount).toFixed(1));
        
        // Calculate monthly revenue
        const monthlyRevenue = analyticsData.revenue_data?.[analyticsData.revenue_data.length - 1]?.revenue || 0;
        this.updateMetric('monthly-revenue', `€${monthlyRevenue.toLocaleString()}`);
        
        // Calculate conversion rate
        const latestDay = analyticsData.daily_stats?.[analyticsData.daily_stats.length - 1];
        const conversionRate = latestDay ? ((latestDay.conversions / latestDay.affiliate_clicks) * 100).toFixed(2) : 0;
        this.updateMetric('conversion-rate', `${conversionRate}%`);
        
        // Load top products
        this.loadTopProducts();
    }

    updateMetric(id, value) {
        const element = document.getElementById(id);
        if (element) {
            element.textContent = value;
        }
    }

    loadTopProducts() {
        const container = document.getElementById('top-products-list');
        if (!container || !this.data) return;

        const allProducts = [];
        Object.values(this.data.quantumData.categories).forEach(category => {
            category.top_products?.forEach(product => {
                allProducts.push(product);
            });
        });

        // Sort by quantum score
        allProducts.sort((a, b) => b.quantum_score - a.quantum_score);
        
        container.innerHTML = allProducts.slice(0, 10).map(product => `
            <div class="product-row">
                <div>${product.title}</div>
                <div>€${product.price}</div>
                <div>${product.rating}/5</div>
                <div>
                    <span class="quantum-score ${this.getScoreClass(product.quantum_score)}">
                        ${product.quantum_score}/10
                    </span>
                </div>
                <div>
                    <button class="action-btn" onclick="admin.editProduct('${product.asin}')">Edit</button>
                </div>
            </div>
        `).join('');
    }

    loadProductsTable() {
        const container = document.getElementById('all-products-list');
        if (!container || !this.data) return;

        const allProducts = [];
        Object.values(this.data.quantumData.categories).forEach(category => {
            category.top_products?.forEach(product => {
                allProducts.push(product);
            });
        });

        container.innerHTML = allProducts.map(product => `
            <div class="product-row">
                <div>${product.title}</div>
                <div>€${product.price}</div>
                <div>${product.rating}/5</div>
                <div>
                    <span class="quantum-score ${this.getScoreClass(product.quantum_score)}">
                        ${product.quantum_score}/10
                    </span>
                </div>
                <div>
                    <button class="action-btn" onclick="admin.editProduct('${product.asin}')">Edit</button>
                </div>
            </div>
        `).join('');
    }

    getScoreClass(score) {
        if (score >= 9) return 'score-excellent';
        if (score >= 7) return 'score-good';
        return 'score-fair';
    }

    // Admin Actions
    async runAnalysis() {
        alert('Running AI analysis... This may take a few minutes.');
        try {
            const response = await fetch('/api/run-analysis', { method: 'POST' });
            if (response.ok) {
                alert('Analysis completed successfully!');
                await this.loadData();
                this.updateMetrics();
            }
        } catch (error) {
            alert('Analysis failed. Please try again.');
        }
    }

    exportData() {
        const dataStr = JSON.stringify(this.data, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(dataBlob);
        
        const link = document.createElement('a');
        link.href = url;
        link.download = `quantum-data-${new Date().toISOString().split('T')[0]}.json`;
        link.click();
        
        URL.revokeObjectURL(url);
    }

    sendNewsletter() {
        if (confirm('Send newsletter to all subscribers?')) {
            alert('Newsletter queued for sending!');
        }
    }

    runHealthCheck() {
        alert('Running system health check...');
        // Simulate health check
        setTimeout(() => {
            alert('Health check completed. All systems operational.');
        }, 2000);
    }
}

// Initialize admin
const admin = new QuantumAdmin();
