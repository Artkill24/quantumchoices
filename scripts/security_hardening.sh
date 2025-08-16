#!/bin/bash
# QuantumChoices Security Hardening

echo "🔐 Starting security hardening..."

# Update all dependencies
echo "📦 Updating dependencies..."
npm audit fix
pip install --upgrade -r requirements.txt

# Generate security headers
echo "🛡️ Configuring security headers..."
cat > .htaccess << 'SEC_EOF'
# Security Headers
Header always set X-Content-Type-Options nosniff
Header always set X-Frame-Options DENY
Header always set X-XSS-Protection "1; mode=block"
Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
Header always set Referrer-Policy "strict-origin-when-cross-origin"
Header always set Permissions-Policy "geolocation=(), microphone=(), camera=()"

# Content Security Policy
Header always set Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' https://apis.google.com https://www.googletagmanager.com; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; connect-src 'self' https:; font-src 'self' https:; object-src 'none'; media-src 'self'; frame-src 'none';"

# Hide server information
ServerTokens Prod
Header unset Server
Header unset X-Powered-By
SEC_EOF

# Rate limiting configuration
echo "⚡ Setting up rate limiting..."
cat > config/rate-limit.js << 'RATE_EOF'
const rateLimit = require('express-rate-limit');

const createRateLimit = (windowMs, max, message) => {
    return rateLimit({
        windowMs,
        max,
        message: { error: message },
        standardHeaders: true,
        legacyHeaders: false,
        handler: (req, res) => {
            res.status(429).json({
                error: 'Too many requests',
                retryAfter: Math.round(windowMs / 1000)
            });
        }
    });
};

module.exports = {
    general: createRateLimit(15 * 60 * 1000, 100, 'Too many requests'),
    api: createRateLimit(15 * 60 * 1000, 50, 'Too many API requests'),
    auth: createRateLimit(15 * 60 * 1000, 5, 'Too many authentication attempts')
};
RATE_EOF

# API key validation
echo "🔑 Setting up API key validation..."
cat > scripts/validate_keys.py << 'KEY_EOF'
#!/usr/bin/env python3
import os
import re
import sys

def validate_api_keys():
    """Validate API key formats"""
    keys = {
        'OPENAI_API_KEY': r'^sk-[a-zA-Z0-9]{48}$',
        'AMAZON_ACCESS_KEY': r'^[A-Z0-9]{20}$',
        'AMAZON_SECRET_KEY': r'^[a-zA-Z0-9+/]{40}$'
    }
    
    for key_name, pattern in keys.items():
        key_value = os.getenv(key_name)
        if not key_value:
            print(f"❌ {key_name} not set")
            return False
        
        if not re.match(pattern, key_value):
            print(f"❌ {key_name} invalid format")
            return False
        
        print(f"✅ {key_name} valid")
    
    return True

if __name__ == "__main__":
    if not validate_api_keys():
        sys.exit(1)
    print("🔑 All API keys validated successfully")
KEY_EOF

chmod +x scripts/validate_keys.py

# Security scan script
echo "🔍 Setting up security scanner..."
cat > scripts/security_scan.py << 'SCAN_EOF'
#!/usr/bin/env python3
import subprocess
import json
import os

def run_security_scan():
    """Run comprehensive security scan"""
    results = {}
    
    # NPM audit
    try:
        npm_result = subprocess.run(['npm', 'audit', '--json'], 
                                  capture_output=True, text=True)
        npm_data = json.loads(npm_result.stdout)
        results['npm_vulnerabilities'] = npm_data.get('metadata', {}).get('vulnerabilities', 0)
    except:
        results['npm_vulnerabilities'] = 'error'
    
    # Python safety check
    try:
        safety_result = subprocess.run(['safety', 'check', '--json'], 
                                     capture_output=True, text=True)
        safety_data = json.loads(safety_result.stdout)
        results['python_vulnerabilities'] = len(safety_data)
    except:
        results['python_vulnerabilities'] = 'error'
    
    # File permission check
    sensitive_files = ['.env', 'config/', 'scripts/']
    results['file_permissions'] = {}
    
    for file_path in sensitive_files:
        if os.path.exists(file_path):
            stat = os.stat(file_path)
            results['file_permissions'][file_path] = oct(stat.st_mode)[-3:]
    
    return results

if __name__ == "__main__":
    results = run_security_scan()
    print("🔍 Security Scan Results:")
    print(json.dumps(results, indent=2))
SCAN_EOF

chmod +x scripts/security_scan.py

# Environment validation
echo "🌍 Setting up environment validation..."
python scripts/validate_keys.py

echo "✅ Security hardening completed!"
echo ""
echo "🔐 Security checklist:"
echo "✅ Dependencies updated"
echo "✅ Security headers configured"
echo "✅ Rate limiting enabled"
echo "✅ API keys validated"
echo "✅ Security scanner ready"
echo ""
echo "🔍 Run security scan: python scripts/security_scan.py"
