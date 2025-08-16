#!/bin/bash
# QuantumChoices - One-Click Deploy Script

set -e

echo "🚀 QuantumChoices Deployment Script"
echo "=================================="

# Check if we're in the right directory
if [ ! -f "package.json" ] || [ ! -f "index.html" ]; then
    echo "❌ Error: Please run this script from the QuantumChoices root directory"
    exit 1
fi

# Check environment
if [ -z "$1" ]; then
    echo "Usage: ./DEPLOY.sh [production|staging|development]"
    echo "Example: ./DEPLOY.sh production"
    exit 1
fi

ENVIRONMENT=$1

echo "🎯 Deploying to: $ENVIRONMENT"
echo ""

# Pre-deployment checks
echo "🔍 Running pre-deployment checks..."

# Check Node.js version
NODE_VERSION=$(node --version | cut -d'v' -f2)
if [ "$(printf '%s\n' "18.0.0" "$NODE_VERSION" | sort -V | head -n1)" != "18.0.0" ]; then
    echo "❌ Node.js 18+ required. Current: $NODE_VERSION"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python --version 2>&1 | cut -d' ' -f2)
if [ "$(printf '%s\n' "3.11.0" "$PYTHON_VERSION" | sort -V | head -n1)" != "3.11.0" ]; then
    echo "❌ Python 3.11+ required. Current: $PYTHON_VERSION"
    exit 1
fi

echo "✅ Environment checks passed"

# Install dependencies
echo "📦 Installing dependencies..."
npm ci --silent
pip install -r requirements.txt --quiet

echo "✅ Dependencies installed"

# Validate configuration
echo "🔑 Validating configuration..."
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Copy .env.example and configure it."
    exit 1
fi

python scripts/validate_keys.py
if [ $? -ne 0 ]; then
    echo "❌ Configuration validation failed"
    exit 1
fi

echo "✅ Configuration validated"

# Run tests
echo "🧪 Running tests..."
python scripts/quantum_tests.py
if [ $? -ne 0 ]; then
    echo "❌ Tests failed. Fix issues before deploying."
    exit 1
fi

echo "✅ Tests passed"

# Security hardening
echo "🔐 Running security hardening..."
./scripts/security_hardening.sh

echo "✅ Security hardening completed"

# Build application
echo "🔨 Building application..."
npm run build

echo "✅ Build completed"

# Run AI analysis
echo "🤖 Running AI analysis..."
python scripts/quantum_analyzer.py

echo "✅ AI analysis completed"

# Generate content
echo "📝 Generating initial content..."
node scripts/content_generator.js

echo "✅ Content generated"

# Performance optimization
echo "⚡ Optimizing performance..."
./scripts/optimize_performance.sh

echo "✅ Performance optimized"

# Environment-specific deployment
case $ENVIRONMENT in
    "production")
        echo "🌐 Deploying to production..."
        
        # GitHub Pages deployment
        if [ -d ".git" ]; then
            git add .
            git commit -m "🚀 Production deployment $(date)"
            git push origin main
            echo "✅ Pushed to GitHub Pages"
        fi
        
        # Cloudflare Workers (if configured)
        if [ -f "cloudflare/wrangler.toml" ]; then
            cd cloudflare
            npx wrangler publish --env production
            cd ..
            echo "✅ Deployed to Cloudflare Workers"
        fi
        
        # Vercel (if configured)
        if [ -f "vercel.json" ]; then
            npx vercel --prod --yes
            echo "✅ Deployed to Vercel"
        fi
        
        ;;
        
    "staging")
        echo "🔧 Deploying to staging..."
        
        # Deploy to staging branch
        if [ -d ".git" ]; then
            git checkout -b staging 2>/dev/null || git checkout staging
            git add .
            git commit -m "🔧 Staging deployment $(date)"
            git push origin staging
            echo "✅ Deployed to staging"
        fi
        
        ;;
        
    "development")
        echo "💻 Setting up development environment..."
        
        # Start development server
        echo "🚀 Starting development server..."
        echo "   - Frontend: http://localhost:8000"
        echo "   - Admin: http://localhost:8000/admin"
        echo "   - Health: http://localhost:8000/health"
        echo ""
        echo "Press Ctrl+C to stop the server"
        
        # Start services
        npm run dev &
        DEV_PID=$!
        
        # Cleanup on exit
        trap "kill $DEV_PID 2>/dev/null" EXIT
        
        wait $DEV_PID
        exit 0
        ;;
        
    *)
        echo "❌ Unknown environment: $ENVIRONMENT"
        exit 1
        ;;
esac

# Post-deployment verification
echo "🔍 Running post-deployment verification..."

# Wait for deployment to be ready
sleep 10

# Check if site is accessible
SITE_URL="https://$(whoami).github.io/quantumchoices"
if [ "$ENVIRONMENT" = "production" ]; then
    SITE_URL="https://quantumchoices.com"
fi

HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$SITE_URL" || echo "000")

if [ "$HTTP_STATUS" = "200" ]; then
    echo "✅ Site is accessible: $SITE_URL"
else
    echo "⚠️ Site may not be ready yet (HTTP $HTTP_STATUS): $SITE_URL"
fi

# Final health check
echo "🏥 Running final health check..."
python scripts/health_monitor.py

echo ""
echo "🎉 DEPLOYMENT COMPLETED SUCCESSFULLY!"
echo "=================================="
echo "Environment: $ENVIRONMENT"
echo "Site URL: $SITE_URL"
echo "Admin Panel: $SITE_URL/admin"
echo "Health Dashboard: $SITE_URL/health"
echo ""
echo "📊 Next Steps:"
echo "1. 📈 Monitor analytics at $SITE_URL/admin"
echo "2. 📧 Set up email campaigns"
echo "3. 🔍 Monitor health metrics"
echo "4. 💰 Track conversion rates"
echo "5. 🎯 Optimize based on AI insights"
echo ""
echo "📚 Documentation: docs/TUTORIAL.md"
echo "🆘 Support: Create GitHub issue"
echo ""
echo "🧬 Built with Einstein-level precision ⚛️"
