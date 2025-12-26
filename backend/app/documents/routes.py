from fastapi import APIRouter, UploadFile, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.db.database import get_db
from app.db.models import Document
from app.documents.parser import extract_text_from_pdf
from app.documents.chunker import chunk_text
from app.documents.embeddings import embed_text
from app.rag.store import store_chunks

router = APIRouter()

@router.post("/{project_id}")
def upload_document(
    project_id: str,
    file: UploadFile,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # 1️⃣ Extract text from uploaded file
    content = extract_text_from_pdf(file)

    # 2️⃣ Save document metadata in DB
    document = Document(
        filename=file.filename,
        project_id=project_id,
        user_id=current_user.id
    )
    db.add(document)
    db.commit()
    db.refresh(document)

    # 3️⃣ Chunk the extracted text
    chunks = chunk_text(content)

    # 4️⃣ Create embeddings for each chunk
    embeddings = embed_text(chunks)

    # 5️⃣ Store chunks & embeddings in vector DB
    store_chunks(
        chunks=chunks,
        embeddings=embeddings,
        user_id=current_user.id,
        project_id=project_id,
        document_id=document.id
    )

    return {"status": "Document uploaded & indexed"}
