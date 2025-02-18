# src/monitoring/alerts.py
import smtplib
from email.mime.text import MIMEText
from src.monitoring.logger import logger
import requests # Telegram notifier

class EmailNotifier:
    def __init__(self, config: dict):
        self.smtp_server = config["smtp_server"]
        self.smtp_port = config["smtp_port"]
        self.email = config["email"]
        self.password = config["password"]

    def send_alert(self, subject: str, message: str, recipient: str):
        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = self.email
        msg["To"] = recipient

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email, self.password)
                server.sendmail(self.email, recipient, msg.as_string())
            logger.info(f"Alert email sent to {recipient}")
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
      
      
      
         
# src/monitoring/alerts.py
class TelegramNotifier:
    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id

    def send_alert(self, message: str):
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message
        }
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            logger.error(f"Telegram alert failed: {response.text}")            