#!/usr/bin/env python3
"""
QuantumChoices - Email Automation System
Gestione automatica campagne email
"""

import smtplib
import json
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import schedule
import time
import logging
from jinja2 import Template

class EmailAutomation:
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        self.email_user = os.getenv('EMAIL_USER')
        self.email_password = os.getenv('EMAIL_PASSWORD')
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def load_subscribers(self):
        """Carica lista subscribers"""
        try:
            with open('assets/data/subscribers.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def load_template(self, template_name):
        """Carica template email"""
        template_path = f'email_templates/{template_name}.html'
        try:
            with open(template_path, 'r') as f:
                return Template(f.read())
        except FileNotFoundError:
            return Template(self.get_default_template())

    def get_default_template(self):
        """Template email di default"""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; }
                .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2rem; text-align: center; }
                .content { padding: 2rem; }
                .product { border: 1px solid #eee; padding: 1rem; margin: 1rem 0; border-radius: 8px; }
                .score { background: #3498db; color: white; padding: 0.25rem 0.5rem; border-radius: 4px; }
                .footer { background: #f8f9fa; padding: 1rem; text-align: center; font-size: 0.875rem; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>⚛️ QuantumChoices</h1>
                    <p>{{ subject }}</p>
                </div>
                <div class="content">
                    {{ content }}
                </div>
                <div class="footer">
                    <p>© 2025 QuantumChoices - Decisioni d'acquisto scientifiche</p>
                    <p><a href="{{ unsubscribe_url }}">Disiscriviti</a></p>
                </div>
            </div>
        </body>
        </html>
        """

    def send_email(self, to_email, subject, content, template_name='newsletter'):
        """Invia singola email"""
        try:
            template = self.load_template(template_name)
            html_content = template.render(
                subject=subject,
                content=content,
                unsubscribe_url=f"https://quantumchoices.com/unsubscribe?email={to_email}"
            )

            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.email_user
            msg['To'] = to_email

            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_user, self.email_password)
                server.send_message(msg)

            self.logger.info(f"Email sent successfully to {to_email}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to send email to {to_email}: {e}")
            return False

    def send_newsletter(self):
        """Invia newsletter settimanale"""
        self.logger.info("📧 Sending weekly newsletter...")
        
        # Carica dati prodotti
        try:
            with open('assets/data/quantum_data.json', 'r') as f:
                quantum_data = json.load(f)
        except FileNotFoundError:
            self.logger.error("Quantum data not found")
            return

        # Seleziona top products
        top_products = []
        for category in quantum_data['categories'].values():
            top_products.extend(category['top_products'][:2])

        top_products.sort(key=lambda x: x['quantum_score'], reverse=True)
        top_products = top_products[:5]

        # Genera contenuto newsletter
        content = self.generate_newsletter_content(top_products)
        subject = f"🧬 QuantumChoices Weekly: Top 5 Prodotti Scientificamente Testati"

        # Invia a tutti i subscribers
        subscribers = self.load_subscribers()
        sent_count = 0
        
        for subscriber in subscribers:
            if subscriber.get('status') == 'active':
                if self.send_email(subscriber['email'], subject, content):
                    sent_count += 1
                time.sleep(1)  # Rate limiting

        self.logger.info(f"Newsletter sent to {sent_count} subscribers")

    def generate_newsletter_content(self, products):
        """Genera contenuto newsletter"""
        content = """
        <h2>🏆 Top 5 Prodotti della Settimana</h2>
        <p>I nostri algoritmi AI hanno analizzato migliaia di prodotti. Ecco i vincitori:</p>
        """
        
        for i, product in enumerate(products, 1):
            content += f"""
            <div class="product">
                <h3>{i}. {product['title']}</h3>
                <p><strong>Quantum Score:</strong> <span class="score">{product['quantum_score']}/10</span></p>
                <p><strong>Prezzo:</strong> €{product['price']}</p>
                <p><strong>Rating:</strong> {product['rating']}/5 ({product['review_count']} recensioni)</p>
                <p><a href="https://amazon.it/dp/{product['asin']}?tag=quantumchoic-21" 
                      style="background: #3498db; color: white; padding: 0.5rem 1rem; text-decoration: none; border-radius: 4px;">
                   🛒 Vedi su Amazon
                </a></p>
            </div>
            """

        content += """
        <h3>🔬 Metodologia Scientifica</h3>
        <p>Ogni prodotto è analizzato usando 47 parametri quantificabili e algoritmi AI avanzati per garantire raccomandazioni oggettive.</p>
        """

        return content

    def send_price_alerts(self):
        """Invia alert prezzi"""
        self.logger.info("💰 Checking for price drops...")
        
        # Logic per price drops (da implementare)
        # Confronta prezzi attuali con precedenti
        pass

    def schedule_campaigns(self):
        """Pianifica campagne automatiche"""
        # Newsletter ogni lunedì alle 09:00
        schedule.every().monday.at("09:00").do(self.send_newsletter)
        
        # Price alerts ogni giorno alle 08:00
        schedule.every().day.at("08:00").do(self.send_price_alerts)
        
        self.logger.info("📅 Email campaigns scheduled")
        
        while True:
            schedule.run_pending()
            time.sleep(60)

def main():
    """Main function"""
    automation = EmailAutomation()
    
    if len(os.sys.argv) > 1:
        command = os.sys.argv[1]
        if command == "newsletter":
            automation.send_newsletter()
        elif command == "schedule":
            automation.schedule_campaigns()
    else:
        print("Usage: python email_automation.py [newsletter|schedule]")

if __name__ == "__main__":
    main()
