import jwt
import os
from fastapi import HTTPException, status
from datetime import datetime

SECRET = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"


def create_jwt(user_id: str):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow().timestamp() + (7 * 24 * 60 * 60)
    }
    return jwt.encode(payload, SECRET, algorithm=ALGORITHM)


def verify_jwt(token: str):
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
