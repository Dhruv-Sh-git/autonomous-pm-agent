import os
import random
import smtplib
from datetime import datetime, timedelta
from email.message import EmailMessage

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
    """Send OTP via SMTP using credentials from environment variables.

    Expected env vars (set in backend/.env):
      SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, SMTP_FROM, SMTP_USE_TLS
    """

    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    from_email = os.getenv("SMTP_FROM", smtp_user or "")
    use_tls = os.getenv("SMTP_USE_TLS", "true").lower() == "true"

    if not smtp_user or not smtp_password:
        # Fallback to dev-mode logging if email is not configured
        print("[OTP] SMTP credentials not configured. OTP:", otp)
        return

    msg = EmailMessage()
    msg["Subject"] = "Your login code"
    msg["From"] = from_email
    msg["To"] = to_email
    msg.set_content(
        f"Your one-time login code is: {otp}\n\n"
        "This code will expire in 5 minutes."
    )

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            if use_tls:
                server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
        print(f"[OTP] Sent OTP email to {to_email}")
    except Exception as e:
        # Don't crash auth flow if email sending fails; log for now.
        print("[OTP] Failed to send email:", e)
