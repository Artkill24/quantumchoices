# 🚀 QuantumChoices - Deployment Guide Einstein-Level

## Overview
Guida completa per deployment di QuantumChoices, sistema di affiliate marketing con AI automation.

## Prerequisites

### Required Services
- GitHub account con GitHub Pages abilitato
- OpenAI API key per AI features
- Amazon Associates account
- SMTP server per email automation (Gmail consigliato)

### Required Tools
```bash
# Node.js 18+
node --version

# Python 3.11+
python --version

# Git
git --version
```

## Quick Start Deployment

### 1. Repository Setup
```bash
# Clone/Create repository
git clone https://github.com/username/quantumchoices.git
cd quantumchoices

# Install dependencies
npm install
pip install -r requirements.txt
```

### 2. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit with your credentials
nano .env
```

Required environment variables:
```env
OPENAI_API_KEY=sk-your-openai-key
AMAZON_ACCESS_KEY=your-amazon-access-key
AMAZON_SECRET_KEY=your-amazon-secret-key
AMAZON_ASSOCIATE_TAG=your-amazon-tag
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
SITE_URL=https://username.github.io/quantumchoices
```

### 3. GitHub Secrets Setup
In GitHub Repository Settings > Secrets:

```
OPENAI_API_KEY
AMAZON_ACCESS_KEY
AMAZON_SECRET_KEY
EMAIL_USER
EMAIL_PASSWORD
```

### 4. Enable GitHub Pages
1. Repository Settings → Pages
2. Source: GitHub Actions
3. Custom domain (optional): quantumchoices.com

### 5. Initial Deployment
```bash
# Run initial setup
npm run build
python scripts/quantum_analyzer.py

# Commit and push
git add .
git commit -m "🚀 Initial QuantumChoices deployment"
git push origin main
```

## Advanced Configuration

### Custom Domain Setup
1. Add CNAME file:
```bash
echo "quantumchoices.com" > CNAME
```

2. DNS Configuration:
```
Type: CNAME
Name: www
Value: username.github.io
```

### SSL Certificate
GitHub Pages automatically provides SSL for `.github.io` domains and custom domains.

### CDN Setup (Optional)
For improved performance, consider Cloudflare:

1. Add site to Cloudflare
2. Update DNS nameservers
3. Enable caching rules for static assets

## Automation Setup

### 1. AI Content Generation
Automated content generation runs every 6 hours via GitHub Actions.

Manual trigger:
```bash
node scripts/content_generator.js
```

### 2. Email Automation
Setup SMTP credentials and run:
```bash
python scripts/email_automation.py schedule
```

### 3. Health Monitoring
Continuous monitoring:
```bash
python scripts/health_monitor.py
```

## Performance Optimization

### 1. Image Optimization
```bash
# Optimize images
npm run optimize-images
```

### 2. Caching Strategy
- Static assets: 1 year cache
- API data: 5 minutes cache
- HTML: No cache

### 3. SEO Optimization
- Automatic sitemap generation
- Rich snippets implementation
- Meta tags optimization

## Security Configuration

### 1. API Rate Limiting
Amazon API calls are rate-limited to prevent quota exhaustion.

### 2. CORS Headers
```javascript
// In your hosting configuration
Access-Control-Allow-Origin: https://quantumchoices.com
Access-Control-Allow-Methods: GET, POST
```

### 3. Content Security Policy
```html
<meta http-equiv="Content-Security-Policy" 
      content="default-src 'self'; script-src 'self' 'unsafe-inline' https://apis.google.com">
```

## Monitoring & Analytics

### 1. Google Analytics Setup
1. Create GA4 property
2. Add tracking ID to environment
3. Enable enhanced ecommerce

### 2. Health Monitoring
Access health dashboard at `/health_dashboard.html`

### 3. Performance Monitoring
- Lighthouse CI integration
- Core Web Vitals tracking
- Real User Monitoring (RUM)

## Troubleshooting

### Common Issues

**Build Failures**
```bash
# Check logs
npm run build --verbose

# Clear cache
npm ci
```

**API Errors**
```bash
# Verify credentials
python -c "import openai; print('OpenAI OK')"

# Test Amazon API
curl "https://webservices.amazon.it/paapi5/getitems"
```

**Deployment Issues**
```bash
# Check GitHub Actions logs
# Verify secrets are set
# Check repository permissions
```

### Performance Issues
1. Run Lighthouse audit
2. Check Core Web Vitals
3. Optimize critical rendering path
4. Enable compression

## Scaling Considerations

### High Traffic
- Enable CDN
- Implement caching layers
- Consider serverless functions

### Content Volume
- Implement pagination
- Use lazy loading
- Optimize database queries

### International Expansion
- Multi-language support
- Regional Amazon affiliates
- Currency conversion

## Backup & Recovery

### Data Backup
```bash
# Backup analytics data
cp assets/data/*.json backup/

# Backup email lists
cp email_templates/* backup/templates/
```

### Disaster Recovery
1. Repository is the source of truth
2. All data in Git history
3. Automated backups to cloud storage

## Maintenance

### Regular Tasks
- Update dependencies monthly
- Review performance metrics weekly
- Update content automation rules
- Monitor affiliate link validity

### Security Updates
```bash
# Update dependencies
npm audit fix
pip check

# Security scan
npm audit
safety check
```

## Support

### Documentation
- Technical docs: `/docs/`
- API reference: `/docs/api/`
- Contributing guide: `/docs/CONTRIBUTING.md`

### Getting Help
- GitHub Issues for bugs
- Discussions for questions
- Email support for critical issues

---

**🎯 Success Metrics**

After deployment, monitor these KPIs:
- Page load time < 3 seconds
- Lighthouse score > 90
- Affiliate conversion rate
- Email engagement rates
- User retention metrics

**🚀 Next Steps**

1. Run initial deployment
2. Verify all systems operational
3. Set up monitoring alerts
4. Launch marketing campaigns
5. Iterate based on analytics

Good luck with your QuantumChoices deployment! 🧬⚛️
