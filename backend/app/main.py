from dotenv import load_dotenv

# 1️⃣ Load environment variables FIRST
load_dotenv()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import engine
from app.db.models import Base

from app.auth.routes import router as auth_router
from app.projects.routes import router as project_router
from app.documents.routes import router as document_router
from app.chat.routes import router as chat_router

# 1️⃣ Create FastAPI app FIRST
app = FastAPI(
    title="Autonomous PM Agent API",
    version="1.0.0"
)

# 2️⃣ CORS (needed for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3️⃣ Create DB tables
Base.metadata.create_all(bind=engine)

# 4️⃣ Register routers
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(project_router, prefix="/projects", tags=["Projects"])
app.include_router(document_router, prefix="/documents", tags=["Documents"])
app.include_router(chat_router, prefix="/chat", tags=["Chat"])

# 5️⃣ Health check
@app.get("/")
def health():
    return {"status": "Backend running 🚀"}
