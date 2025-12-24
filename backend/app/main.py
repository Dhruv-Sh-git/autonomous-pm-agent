from fastapi import FastAPI
from app.db.database import engine
from app.db.models import Base
from app.auth.routes import router as auth_router

# 1️⃣ Create FastAPI app FIRST
app = FastAPI(title="Autonomous PM Agent API")

# 2️⃣ Register routers
app.include_router(auth_router)

# 3️⃣ Create database tables
Base.metadata.create_all(bind=engine)

# 4️⃣ Health check
@app.get("/")
def health():
    return {"status": "Backend running"}
