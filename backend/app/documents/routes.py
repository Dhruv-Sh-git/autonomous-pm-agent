from fastapi import APIRouter, UploadFile, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.db.database import SessionLocal
from app.db.models import Document, User
from app.documents.parser import extract_text_from_pdf
from app.documents.embeddings import embed_text

router = APIRouter(prefix="/documents", tags=["Documents"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/{project_id}")
async def upload_document(
    project_id: str,
    file: UploadFile,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    # 1️⃣ Extract text from PDF
    content = extract_text_from_pdf(await file.read())

    # 2️⃣ CREATE EMBEDDINGS HERE 👇
    embed_text(content)

    # 3️⃣ Save document to DB
    doc = Document(
        project_id=project_id,
        filename=file.filename,
        content=content
    )
    db.add(doc)
    db.commit()

    return {"message": "Document uploaded & embedded"}
