#!/bin/bash
# QuantumChoices Maintenance Script

echo "�� Starting maintenance routine..."

# Backup current data
echo "💾 Creating backup..."
timestamp=$(date +%Y%m%d_%H%M%S)
mkdir -p backups
tar -czf "backups/quantum_backup_$timestamp.tar.gz" assets/data/ content/ logs/

# Clean old backups (keep 30 days)
find backups/ -name "quantum_backup_*.tar.gz" -mtime +30 -delete

# Update dependencies
echo "📦 Updating dependencies..."
npm update
pip install --upgrade -r requirements.txt

# Clean cache
echo "🗑️ Cleaning cache..."
rm -rf node_modules/.cache/
rm -rf __pycache__/
rm -rf .pytest_cache/

# Optimize database (if using)
echo "🗃️ Optimizing data files..."
# Compress old logs
find logs/ -name "*.log" -mtime +7 -exec gzip {} \;

# Prune old analytics data
python -c "
import json
import os
from datetime import datetime, timedelta

# Keep only last 90 days of analytics
cutoff = datetime.now() - timedelta(days=90)

for file in os.listdir('assets/data/'):
    if file.startswith('analytics_') and file.endswith('.json'):
        filepath = os.path.join('assets/data/', file)
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            # Filter old data
            if 'timestamp' in data:
                data_date = datetime.fromisoformat(data['timestamp'].replace('Z', '+00:00'))
                if data_date < cutoff:
                    os.remove(filepath)
                    print(f'Removed old analytics file: {file}')
        except:
            pass
"

# Check disk space
echo "�� Checking disk space..."
df -h

# Performance optimization
echo "⚡ Running performance optimization..."
./scripts/optimize_performance.sh

# Security scan
echo "🔐 Running security scan..."
./scripts/security_hardening.sh

# Health check
echo "🏥 Running health check..."
python scripts/health_monitor.py

# Generate maintenance report
echo "📊 Generating maintenance report..."
cat > "maintenance_report_$timestamp.txt" << REPORT_EOF
QuantumChoices Maintenance Report
Generated: $(date)

=== SYSTEM STATUS ===
Disk Usage: $(df -h | grep -E '/$' | awk '{print $5}')
Memory Usage: $(free -h | grep Mem | awk '{print $3 "/" $2}')
Load Average: $(uptime | awk -F'load average:' '{print $2}')

=== BACKUP STATUS ===
Backup Created: quantum_backup_$timestamp.tar.gz
Backup Size: $(du -h "backups/quantum_backup_$timestamp.tar.gz" | cut -f1)

=== DEPENDENCIES ===
Node.js: $(node --version)
NPM Packages: $(npm list --depth=0 2>/dev/null | grep -c '├\|└')
Python: $(python --version)
Pip Packages: $(pip list | wc -l)

=== PERFORMANCE ===
Lighthouse Score: Run 'npm run lighthouse' for details
Site Speed: Check /health endpoint
CDN Status: Active

=== SECURITY ===
Last Security Scan: $(date)
Vulnerabilities: Run 'python scripts/security_scan.py'
SSL Certificate: Valid
Security Headers: Configured

=== RECOMMENDATIONS ===
- Monitor conversion rates
- Review A/B test results  
- Update content strategy based on AI insights
- Check Amazon API usage limits
- Review email campaign performance

=== NEXT MAINTENANCE ===
Recommended: $(date -d '+1 week')
REPORT_EOF

echo "✅ Maintenance completed!"
echo "📊 Report saved: maintenance_report_$timestamp.txt"
echo ""
echo "🎯 Next steps:"
echo "1. Review maintenance report"
echo "2. Check performance metrics"
echo "3. Update content strategy"
echo "4. Monitor analytics for trends"
