import jwt
import os
from datetime import datetime, timedelta

SECRET = os.getenv("JWT_SECRET")

def create_jwt(user_id: str):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(days=7)
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")
