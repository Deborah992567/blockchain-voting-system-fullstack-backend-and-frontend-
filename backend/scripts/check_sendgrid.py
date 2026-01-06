"""Simple script to confirm SendGrid API key and attempt a lightweight send.
Usage:
  SENDGRID_API_KEY=your_key TEST_EMAIL=you@example.com python backend/scripts/check_sendgrid.py
"""
import os
import sys
from app.config import settings

API_KEY = os.getenv('SENDGRID_API_KEY', settings.SENDGRID_API_KEY)
TEST_EMAIL = os.getenv('TEST_EMAIL') or settings.EMAIL_FROM

if not API_KEY:
    print("SENDGRID_API_KEY not set. Set it in environment and retry.")
    sys.exit(2)

try:
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail
except Exception as e:
    print("sendgrid package not installed. Install via: pip install sendgrid")
    sys.exit(2)

client = SendGridAPIClient(API_KEY)
message = Mail(from_email=settings.EMAIL_FROM, to_emails=TEST_EMAIL, subject="SendGrid Test", html_content="<p>SendGrid test from blockchain-voting-system</p>")
try:
    resp = client.send(message)
    print("SendGrid response status:", resp.status_code)
    if resp.status_code >= 400:
        print("SendGrid returned error:", resp.body)
        sys.exit(1)
    print("Test email sent (accepted by SendGrid)")
except Exception as e:
    print("Failed to send test email:", str(e))
    sys.exit(1)
