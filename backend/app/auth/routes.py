from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models import User
from .otp import generate_otp, verify_otp, send_otp_email
from .jwt import create_jwt
from .schemas import SendOTPRequest, VerifyOTPRequest
router = APIRouter(prefix="/auth")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/send-otp")
def send_otp(payload: SendOTPRequest):
    otp = generate_otp(payload.email)
    # Send OTP via email instead of printing to console
    send_otp_email(payload.email, otp)
    return {"message": "OTP sent"}

@router.post("/verify-otp")
def verify(payload: VerifyOTPRequest, db: Session = Depends(get_db)):
    if not verify_otp(payload.email, payload.otp):
        return {"error": "Invalid OTP"}

    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        user = User(email=payload.email)
        db.add(user)
        db.commit()
        db.refresh(user)

    token = create_jwt(str(user.id))
    return {"token": token}
