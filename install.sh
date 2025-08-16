#!/bin/bash
# QuantumChoices One-Line Installer

set -e

echo "🧬 QuantumChoices Installer"
echo "=========================="

# Check prerequisites
echo "🔍 Checking prerequisites..."

if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js 18+"
    exit 1
fi

if ! command -v python &> /dev/null; then
    echo "❌ Python not found. Please install Python 3.11+"
    exit 1
fi

if ! command -v git &> /dev/null; then
    echo "❌ Git not found. Please install Git"
    exit 1
fi

echo "✅ Prerequisites check passed"

# Clone repository
echo "📂 Cloning QuantumChoices..."
git clone https://github.com/username/quantumchoices.git
cd quantumchoices

# Install dependencies
echo "📦 Installing dependencies..."
npm install
pip install -r requirements.txt

# Setup environment
echo "⚙️ Setting up environment..."
cp .env.example .env

echo ""
echo "🎉 Installation completed!"
echo ""
echo "📋 Next steps:"
echo "1. Edit .env file with your API keys:"
echo "   nano .env"
echo ""
echo "2. Deploy to production:"
echo "   ./DEPLOY.sh production"
echo ""
echo "3. Or start development:"
echo "   ./DEPLOY.sh development"
echo ""
echo "📚 Read the tutorial: docs/TUTORIAL.md"
echo "🆘 Need help? Create a GitHub issue"
echo ""
echo "🧬 Built with Einstein-level precision ⚛️"
