import random
from datetime import datetime, timedelta

otp_store = {}

def generate_otp(email: str):
    otp = str(random.randint(100000, 999999))
    otp_store[email] = {
        "otp": otp,
        "expires": datetime.utcnow() + timedelta(minutes=5)
    }
    return otp

def verify_otp(email: str, otp: str):
    data = otp_store.get(email)
    if not data:
        return False
    if data["expires"] < datetime.utcnow():
        return False
    return data["otp"] == otp
