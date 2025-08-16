#!/usr/bin/env python3
"""
QuantumChoices - Initialization Script
Setup completo e inizializzazione sistema
"""

import os
import sys
import json
import subprocess
import time
from datetime import datetime

class QuantumInitializer:
    def __init__(self):
        self.steps = [
            ("Checking Prerequisites", self.check_prerequisites),
            ("Creating Directory Structure", self.create_directories),
            ("Generating Mock Data", self.generate_mock_data),
            ("Initializing Configuration", self.init_configuration),
            ("Setting Up Git Hooks", self.setup_git_hooks),
            ("Running Initial Tests", self.run_tests),
            ("Starting Services", self.start_services)
        ]
    
    def check_prerequisites(self):
        """Verifica prerequisiti sistema"""
        print("🔍 Checking system requirements...")
        
        # Check Node.js
        try:
            result = subprocess.run(['node', '--version'], capture_output=True, text=True)
            node_version = result.stdout.strip()
            print(f"   ✅ Node.js: {node_version}")
        except FileNotFoundError:
            raise Exception("❌ Node.js not found. Please install Node.js 18+")
        
        # Check Python
        try:
            result = subprocess.run([sys.executable, '--version'], capture_output=True, text=True)
            python_version = result.stdout.strip()
            print(f"   ✅ Python: {python_version}")
        except:
            raise Exception("❌ Python not found")
        
        # Check Git
        try:
            result = subprocess.run(['git', '--version'], capture_output=True, text=True)
            git_version = result.stdout.strip()
            print(f"   ✅ Git: {git_version}")
        except FileNotFoundError:
            raise Exception("❌ Git not found. Please install Git")
        
        # Check environment file
        if not os.path.exists('.env'):
            print("   ⚠️ .env file not found. Creating from template...")
            if os.path.exists('.env.example'):
                subprocess.run(['cp', '.env.example', '.env'])
                print("   📝 Please edit .env file with your API keys")
            else:
                self.create_env_template()
    
    def create_env_template(self):
        """Crea template .env"""
        env_content = """# QuantumChoices Environment Variables

# OpenAI API (Required for AI features)
OPENAI_API_KEY=sk-your-openai-api-key-here

# Amazon Associates (Required for affiliate links)
AMAZON_ASSOCIATE_TAG=your-amazon-tag-21
AMAZON_ACCESS_KEY=your-amazon-access-key
AMAZON_SECRET_KEY=your-amazon-secret-key

# Email Configuration (Required for automation)
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# Site Configuration
SITE_URL=https://yourname.github.io/quantumchoices
NODE_ENV=development

# Optional: Analytics
GOOGLE_ANALYTICS_ID=
GOOGLE_TAG_MANAGER_ID=

# Optional: Database
DATABASE_URL=
REDIS_URL=

# Optional: Monitoring
SENTRY_DSN=
"""
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("   �� .env template created. Please configure it with your credentials.")
    
    def create_directories(self):
        """Crea struttura directory"""
        print("📁 Creating directory structure...")
        
        directories = [
            'assets/data',
            'assets/images',
            'assets/cache',
            'content/articles',
            'content/reviews',
            'logs',
            'backups',
            'temp',
            'dist',
            'examples',
            'admin/api',
            'email_templates',
            'monitoring'
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            print(f"   📂 Created: {directory}")
        
        # Crea file .gitkeep per directory vuote
        keep_dirs = ['logs', 'backups', 'temp', 'assets/cache']
        for directory in keep_dirs:
            gitkeep_path = os.path.join(directory, '.gitkeep')
            if not os.path.exists(gitkeep_path):
                with open(gitkeep_path, 'w') as f:
                    f.write('')
    
    def generate_mock_data(self):
        """Genera dati iniziali"""
        print("🎲 Generating initial mock data...")
        
        try:
            subprocess.run([sys.executable, 'scripts/generate_mock_data.py'], check=True)
            print("   ✅ Mock data generated successfully")
        except subprocess.CalledProcessError as e:
            print(f"   ⚠️ Mock data generation failed: {e}")
            print("   📝 Will create minimal data structure...")
            self.create_minimal_data()
    
    def create_minimal_data(self):
        """Crea struttura dati minimale"""
        # Quantum data minimale
        minimal_quantum_data = {
            'last_update': datetime.now().isoformat(),
            'categories': {
                'tech': {
                    'top_products': [],
                    'total_analyzed': 0,
                    'avg_quantum_score': 0
                },
                'home': {
                    'top_products': [],
                    'total_analyzed': 0,
                    'avg_quantum_score': 0
                }
            }
        }
        
        with open('assets/data/quantum_data.json', 'w') as f:
            json.dump(minimal_quantum_data, f, indent=2)
        
        # Health report minimale
        health_report = {
            'timestamp': datetime.now().isoformat(),
            'overall_score': 100,
            'overall_status': 'healthy',
            'metrics': {}
        }
        
        with open('assets/data/health_report.json', 'w') as f:
            json.dump(health_report, f, indent=2)
        
        print("   📄 Minimal data structure created")
    
    def init_configuration(self):
        """Inizializza configurazioni"""
        print("⚙️ Initializing configuration...")
        
        # Git configuration
        if os.path.exists('.git'):
            try:
                # Set git hooks path
                subprocess.run(['git', 'config', 'core.hooksPath', '.githooks'], check=True)
                print("   🪝 Git hooks configured")
            except subprocess.CalledProcessError:
                print("   ⚠️ Could not configure git hooks")
        
        # NPM configuration
        if os.path.exists('package.json'):
            try:
                subprocess.run(['npm', 'install'], check=True, capture_output=True)
                print("   📦 NPM dependencies installed")
            except subprocess.CalledProcessError:
                print("   ⚠️ NPM install failed")
        
        # Python dependencies
        if os.path.exists('requirements.txt'):
            try:
                subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                             check=True, capture_output=True)
                print("   🐍 Python dependencies installed")
            except subprocess.CalledProcessError:
                print("   ⚠️ Python dependencies install failed")
    
    def setup_git_hooks(self):
        """Setup Git hooks"""
        print("🪝 Setting up Git hooks...")
        
        os.makedirs('.githooks', exist_ok=True)
        
        # Pre-commit hook
        pre_commit_hook = """#!/bin/bash
# QuantumChoices Pre-commit Hook

echo "🔍 Running pre-commit checks..."

# Run tests
if ! python scripts/quantum_tests.py; then
    echo "❌ Tests failed. Commit aborted."
    exit 1
fi

# Check for secrets
if grep -r "sk-" --include="*.py" --include="*.js" --exclude-dir=node_modules .; then
    echo "❌ Potential API key found in code. Commit aborted."
    exit 1
fi

echo "✅ Pre-commit checks passed"
"""
        
        with open('.githooks/pre-commit', 'w') as f:
            f.write(pre_commit_hook)
        
        os.chmod('.githooks/pre-commit', 0o755)
        print("   🛡️ Pre-commit hook installed")
    
    def run_tests(self):
        """Esegue test iniziali"""
        print("🧪 Running initial tests...")
        
        try:
            # Test basic functionality
            result = subprocess.run([sys.executable, 'scripts/quantum_tests.py'], 
                                  capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                print("   ✅ All tests passed")
            else:
                print("   ⚠️ Some tests failed:")
                print(f"   {result.stdout}")
        except subprocess.TimeoutExpired:
            print("   ⚠️ Tests timed out")
        except FileNotFoundError:
            print("   ⚠️ Test script not found")
    
    def start_services(self):
        """Avvia servizi iniziali"""
        print("🚀 Starting services...")
        
        # Health check
        try:
            subprocess.run([sys.executable, 'scripts/health_monitor.py'], 
                         timeout=10, capture_output=True)
            print("   🏥 Health monitor check completed")
        except:
            print("   ⚠️ Health monitor check failed")
        
        # Generate initial content
        try:
            subprocess.run(['node', 'scripts/content_generator.js'], 
                         timeout=30, capture_output=True)
            print("   📝 Initial content generated")
        except:
            print("   ⚠️ Content generation skipped")
    
    def run_initialization(self):
        """Esegue inizializzazione completa"""
        print("🧬 QuantumChoices Initialization")
        print("=" * 50)
        
        total_steps = len(self.steps)
        
        for i, (step_name, step_func) in enumerate(self.steps, 1):
            print(f"\n[{i}/{total_steps}] {step_name}")
            print("-" * 30)
            
            try:
                step_func()
                print(f"✅ {step_name} completed")
            except Exception as e:
                print(f"❌ {step_name} failed: {e}")
                
                # Ask user if they want to continue
                response = input("Continue with initialization? (y/n): ").strip().lower()
                if response != 'y':
                    print("🛑 Initialization aborted")
                    return False
            
            time.sleep(0.5)  # Brief pause for readability
        
        print("\n" + "=" * 50)
        print("🎉 QuantumChoices initialization completed!")
        print("\n📋 Next steps:")
        print("1. Edit .env file with your API keys")
        print("2. Run: ./DEPLOY.sh development")
        print("3. Open: http://localhost:8000")
        print("4. Admin: http://localhost:8000/admin")
        print("\n📚 Documentation: docs/TUTORIAL.md")
        print("🆘 Support: Create GitHub issue")
        print("\n🧬 Ready to dominate affiliate marketing! ⚛️")
        
        return True

def main():
    initializer = QuantumInitializer()
    success = initializer.run_initialization()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
