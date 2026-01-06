from fastapi import APIRouter, Depends
from app.utils.security import get_current_user
from app.config import settings
from app.services.email import _send_via_sendgrid
from app.utils.security import admin_only

router = APIRouter(prefix="/test")

@router.get("/protected")
def protected(user = Depends(get_current_user)):
    return {
        "message": "You are authenticated",
        "email": user.email,
        "role": user.role
    }


@router.get('/ping')
def ping():
    return {"message": "pong"}


@router.get('/')
def root():
    return {"message": "Backend is alive!"}


@router.get('/email/check')
def email_check():
    return {"sendgrid_configured": bool(settings.SENDGRID_API_KEY), "email_from": settings.EMAIL_FROM}


@router.post('/email/test')
def email_test(to: str, subject: str = "Test Email", body: str = "This is a test email", admin=Depends(admin_only)):
    """Admin-only endpoint to try sending a single test email via SendGrid (raises on failure)."""
    try:
        _send_via_sendgrid(to, subject, body)
        return {"message": "Test email sent (or accepted by SendGrid)"}
    except Exception as exc:
        return {"error": str(exc)}
