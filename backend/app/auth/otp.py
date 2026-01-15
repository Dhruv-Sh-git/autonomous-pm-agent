import os
import random
from datetime import datetime, timedelta
import resend

otp_store = {}


def generate_otp(email: str) -> str:
    otp = str(random.randint(100000, 999999))
    otp_store[email] = {
        "otp": otp,
        "expires": datetime.utcnow() + timedelta(minutes=5),
    }
    return otp


def verify_otp(email: str, otp: str) -> bool:
    data = otp_store.get(email)
    if not data:
        return False
    if data["expires"] < datetime.utcnow():
        return False
    return data["otp"] == otp


def send_otp_email(to_email: str, otp: str) -> None:
    """Send OTP via Resend Email API.

    Expected env vars (set in backend/.env):
      RESEND_API_KEY, RESEND_FROM_EMAIL
    """

    api_key = os.getenv("RESEND_API_KEY")
    from_email = os.getenv("RESEND_FROM_EMAIL", "onboarding@resend.dev")

    if not api_key:
        # Fallback to dev-mode logging if Resend is not configured
        print("[OTP] Resend API key not configured. OTP:", otp)
        return

    resend.api_key = api_key

    try:
        params = {
            "from": from_email,
            "to": [to_email],
            "subject": "Your login code",
            "html": f"<p>Your one-time login code is: <strong>{otp}</strong></p><p>This code will expire in 5 minutes.</p>"
        }
        
        email_response = resend.Emails.send(params)
        print(f"[OTP] Email sent successfully!")
        print(f"[OTP] Response: {email_response}")
        print(f"[OTP] To: {to_email}")
        print(f"[OTP] From: {from_email}")
        print(f"[OTP] OTP: {otp}")
    except Exception as e:
        # Don't crash auth flow if email sending fails; log for now.
        print("[OTP] Failed to send email!")
        print(f"[OTP] Error: {e}")
        print(f"[OTP] API Key configured: {bool(api_key)}")
        print(f"[OTP] From: {from_email}")
        print(f"[OTP] To: {to_email}")
        print(f"[OTP] OTP for debugging: {otp}")
