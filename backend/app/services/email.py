import os
from app.config import settings

def _send_via_sendgrid(to: str, subject: str, body: str) -> bool:
    """Send email via SendGrid."""
    if not settings.SENDGRID_API_KEY:
        raise Exception("SENDGRID_API_KEY is not configured")
    
    try:
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import Mail
        
        message = Mail(
            from_email=settings.EMAIL_FROM or "noreply@voting.system",
            to_emails=to,
            subject=subject,
            html_content=body
        )
        
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        return response.status_code == 202
    except ImportError:
        raise Exception("sendgrid package not installed")
    except Exception as e:
        raise Exception(f"Failed to send email: {str(e)}")

def send_email_async(to: str, subject: str, body: str):
    """Queue email for async sending."""
    # Placeholder for async email queueing
    return _send_via_sendgrid(to, subject, body)
