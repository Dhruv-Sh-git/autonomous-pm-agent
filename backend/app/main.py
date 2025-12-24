from fastapi import FastAPI
from app.db.database import engine
from app.db.models import Base
from app.auth.routes import router as auth_router
from app.projects.routes import router as project_router

app = FastAPI(title="Autonomous PM Agent API")

app.include_router(auth_router)
app.include_router(project_router)

Base.metadata.create_all(bind=engine)

@app.get("/")
def health():
    return {"status": "Backend running"}
