#!/usr/bin/env python3
"""
QuantumChoices - Health Monitoring System
Monitoraggio continuo delle performance
"""

import asyncio
import aiohttp
import json
import time
import psutil
import logging
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
import os
import requests
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class HealthMetric:
    name: str
    value: float
    threshold: float
    status: str
    timestamp: datetime

class QuantumHealthMonitor:
    def __init__(self):
        self.base_url = os.getenv('MONITOR_URL', 'https://quantumchoices.github.io')
        self.alert_email = os.getenv('ALERT_EMAIL', 'admin@quantumchoices.com')
        self.metrics_history = []
        self.alert_thresholds = {
            'response_time': 3.0,  # seconds
            'error_rate': 0.05,    # 5%
            'cpu_usage': 80.0,     # %
            'memory_usage': 85.0,  # %
            'availability': 99.0   # %
        }
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    async def check_website_availability(self) -> HealthMetric:
        """Check availability del sito"""
        try:
            start_time = time.time()
            
            async with aiohttp.ClientSession() as session:
                async with session.get(self.base_url, timeout=10) as response:
                    response_time = time.time() - start_time
                    
                    status = 'healthy' if response.status == 200 else 'unhealthy'
                    
                    return HealthMetric(
                        name='availability',
                        value=100.0 if response.status == 200 else 0.0,
                        threshold=self.alert_thresholds['availability'],
                        status=status,
                        timestamp=datetime.now()
                    )
                    
        except Exception as e:
            self.logger.error(f"Availability check failed: {e}")
            return HealthMetric(
                name='availability',
                value=0.0,
                threshold=self.alert_thresholds['availability'],
                status='critical',
                timestamp=datetime.now()
            )

    async def check_response_time(self) -> HealthMetric:
        """Check tempo di risposta"""
        endpoints = [
            '/',
            '/assets/data/quantum_data.json',
            '/manifest.json'
        ]
        
        response_times = []
        
        for endpoint in endpoints:
            try:
                start_time = time.time()
                
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"{self.base_url}{endpoint}", timeout=5) as response:
                        response_time = time.time() - start_time
                        response_times.append(response_time)
                        
            except Exception as e:
                self.logger.warning(f"Response time check failed for {endpoint}: {e}")
                response_times.append(10.0)  # Penalty for failed requests
        
        avg_response_time = sum(response_times) / len(response_times)
        status = 'healthy' if avg_response_time < self.alert_thresholds['response_time'] else 'warning'
        
        return HealthMetric(
            name='response_time',
            value=avg_response_time,
            threshold=self.alert_thresholds['response_time'],
            status=status,
            timestamp=datetime.now()
        )

    async def check_api_health(self) -> HealthMetric:
        """Check health delle API"""
        api_endpoints = [
            '/assets/data/quantum_data.json',
            '/assets/data/content_suggestions.json'
        ]
        
        healthy_endpoints = 0
        
        for endpoint in api_endpoints:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"{self.base_url}{endpoint}") as response:
                        if response.status == 200:
                            # Validate JSON
                            data = await response.json()
                            if data:  # Non-empty response
                                healthy_endpoints += 1
                                
            except Exception as e:
                self.logger.warning(f"API health check failed for {endpoint}: {e}")
        
        health_percentage = (healthy_endpoints / len(api_endpoints)) * 100
        status = 'healthy' if health_percentage >= 90 else 'warning'
        
        return HealthMetric(
            name='api_health',
            value=health_percentage,
            threshold=90.0,
            status=status,
            timestamp=datetime.now()
        )

    def check_system_resources(self) -> List[HealthMetric]:
        """Check risorse sistema"""
        metrics = []
        
        # CPU Usage
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_status = 'healthy' if cpu_percent < self.alert_thresholds['cpu_usage'] else 'warning'
        
        metrics.append(HealthMetric(
            name='cpu_usage',
            value=cpu_percent,
            threshold=self.alert_thresholds['cpu_usage'],
            status=cpu_status,
            timestamp=datetime.now()
        ))
        
        # Memory Usage
        memory = psutil.virtual_memory()
        memory_status = 'healthy' if memory.percent < self.alert_thresholds['memory_usage'] else 'warning'
        
        metrics.append(HealthMetric(
            name='memory_usage',
            value=memory.percent,
            threshold=self.alert_thresholds['memory_usage'],
            status=memory_status,
            timestamp=datetime.now()
        ))
        
        # Disk Usage
        disk = psutil.disk_usage('/')
        disk_percent = (disk.used / disk.total) * 100
        disk_status = 'healthy' if disk_percent < 80 else 'warning'
        
        metrics.append(HealthMetric(
            name='disk_usage',
            value=disk_percent,
            threshold=80.0,
            status=disk_status,
            timestamp=datetime.now()
        ))
        
        return metrics

    async def check_content_freshness(self) -> HealthMetric:
        """Check freschezza dei contenuti"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/assets/data/quantum_data.json") as response:
                    data = await response.json()
                    
                    last_update = datetime.fromisoformat(data.get('last_update', '2000-01-01T00:00:00'))
                    hours_since_update = (datetime.now() - last_update).total_seconds() / 3600
                    
                    # Content should be updated at least every 6 hours
                    status = 'healthy' if hours_since_update < 6 else 'warning'
                    
                    return HealthMetric(
                        name='content_freshness',
                        value=hours_since_update,
                        threshold=6.0,
                        status=status,
                        timestamp=datetime.now()
                    )
                    
        except Exception as e:
            self.logger.error(f"Content freshness check failed: {e}")
            return HealthMetric(
                name='content_freshness',
                value=24.0,  # Assume stale
                threshold=6.0,
                status='critical',
                timestamp=datetime.now()
            )

    async def check_affiliate_links(self) -> HealthMetric:
        """Check validità link affiliati"""
        try:
            # Sample di link Amazon da testare
            test_links = [
                'https://amazon.it/dp/B08N5WRWNW?tag=quantumchoic-21',
                'https://amazon.it/dp/B08N5WRWNW?tag=quantumchoic-21'
            ]
            
            working_links = 0
            
            for link in test_links:
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.head(link, timeout=5) as response:
                            if response.status in [200, 301, 302]:
                                working_links += 1
                except:
                    pass
            
            link_health = (working_links / len(test_links)) * 100
            status = 'healthy' if link_health >= 80 else 'warning'
            
            return HealthMetric(
                name='affiliate_links',
                value=link_health,
                threshold=80.0,
                status=status,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            self.logger.error(f"Affiliate link check failed: {e}")
            return HealthMetric(
                name='affiliate_links',
                value=0.0,
                threshold=80.0,
                status='critical',
                timestamp=datetime.now()
            )

    async def run_health_check(self) -> Dict:
        """Esegue check completo"""
        self.logger.info("🔍 Running health check...")
        
        # Collect all metrics
        all_metrics = []
        
        # Website checks
        availability = await self.check_website_availability()
        response_time = await self.check_response_time()
        api_health = await self.check_api_health()
        content_freshness = await self.check_content_freshness()
        affiliate_links = await self.check_affiliate_links()
        
        all_metrics.extend([availability, response_time, api_health, content_freshness, affiliate_links])
        
        # System checks
        system_metrics = self.check_system_resources()
        all_metrics.extend(system_metrics)
        
        # Calculate overall health score
        healthy_metrics = sum(1 for metric in all_metrics if metric.status == 'healthy')
        overall_score = (healthy_metrics / len(all_metrics)) * 100
        
        health_report = {
            'timestamp': datetime.now().isoformat(),
            'overall_score': overall_score,
            'overall_status': self.get_overall_status(overall_score),
            'metrics': {metric.name: {
                'value': metric.value,
                'threshold': metric.threshold,
                'status': metric.status,
                'timestamp': metric.timestamp.isoformat()
            } for metric in all_metrics}
        }
        
        # Store metrics
        self.metrics_history.append(health_report)
        
        # Keep only last 24 hours of data
        cutoff_time = datetime.now() - timedelta(hours=24)
        self.metrics_history = [
            report for report in self.metrics_history 
            if datetime.fromisoformat(report['timestamp']) > cutoff_time
        ]
        
        # Save to file
        self.save_health_report(health_report)
        
        # Check for alerts
        await self.check_alerts(all_metrics)
        
        return health_report

    def get_overall_status(self, score: float) -> str:
        """Determina status generale"""
        if score >= 90:
            return 'healthy'
        elif score >= 70:
            return 'warning'
        else:
            return 'critical'

    def save_health_report(self, report: Dict):
        """Salva report salute"""
        with open('assets/data/health_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        # Save historical data
        with open('assets/data/health_history.json', 'w') as f:
            json.dump(self.metrics_history, f, indent=2)

    async def check_alerts(self, metrics: List[HealthMetric]):
        """Check per alert da inviare"""
        critical_metrics = [m for m in metrics if m.status == 'critical']
        warning_metrics = [m for m in metrics if m.status == 'warning']
        
        if critical_metrics:
            await self.send_alert('critical', critical_metrics)
        elif len(warning_metrics) > 2:  # Multiple warnings
            await self.send_alert('warning', warning_metrics)

    async def send_alert(self, severity: str, metrics: List[HealthMetric]):
        """Invia alert email"""
        try:
            subject = f"🚨 QuantumChoices Health Alert - {severity.upper()}"
            
            body = f"""
            QuantumChoices Health Alert
            
            Severity: {severity.upper()}
            Time: {datetime.now().isoformat()}
            
            Issues detected:
            """
            
            for metric in metrics:
                body += f"""
                - {metric.name}: {metric.value:.2f} (threshold: {metric.threshold})
                  Status: {metric.status}
                """
            
            body += f"""
            
            Please check the system immediately.
            
            Health Dashboard: {self.base_url}/health
            """
            
            # Send email (simplified)
            self.logger.warning(f"ALERT: {subject}")
            self.logger.warning(body)
            
            # In produzione: implementare invio email reale
            
        except Exception as e:
            self.logger.error(f"Failed to send alert: {e}")

    async def generate_health_dashboard(self):
        """Genera dashboard HTML per monitoraggio"""
        if not self.metrics_history:
            return
        
        latest_report = self.metrics_history[-1]
        
        dashboard_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>QuantumChoices Health Dashboard</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .status-healthy {{ color: green; }}
                .status-warning {{ color: orange; }}
                .status-critical {{ color: red; }}
                .metric {{ margin: 10px 0; padding: 10px; border: 1px solid #ddd; }}
                .score {{ font-size: 2em; font-weight: bold; }}
            </style>
        </head>
        <body>
            <h1>🔍 QuantumChoices Health Dashboard</h1>
            
            <div class="score status-{latest_report['overall_status']}">
                Overall Health: {latest_report['overall_score']:.1f}%
            </div>
            
            <h2>System Metrics</h2>
            
            {''.join([
                f'''
                <div class="metric">
                    <strong>{name.replace('_', ' ').title()}:</strong> 
                    <span class="status-{data['status']}">{data['value']:.2f} 
                    (threshold: {data['threshold']})</span>
                    <br><small>Last updated: {data['timestamp']}</small>
                </div>
                '''
                for name, data in latest_report['metrics'].items()
            ])}
            
            <p><em>Last updated: {latest_report['timestamp']}</em></p>
        </body>
        </html>
        """
        
        with open('health_dashboard.html', 'w') as f:
            f.write(dashboard_html)

async def main():
    """Main monitoring loop"""
    monitor = QuantumHealthMonitor()
    
    while True:
        try:
            health_report = await monitor.run_health_check()
            await monitor.generate_health_dashboard()
            
            print(f"🏥 Health Score: {health_report['overall_score']:.1f}% ({health_report['overall_status']})")
            
            # Sleep for 5 minutes
            await asyncio.sleep(300)
            
        except KeyboardInterrupt:
            print("Monitoring stopped by user")
            break
        except Exception as e:
            print(f"Monitoring error: {e}")
            await asyncio.sleep(60)  # Wait 1 minute on error

if __name__ == "__main__":
    asyncio.run(main())
