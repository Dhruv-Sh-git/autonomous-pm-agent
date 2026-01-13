from uuid import UUID

from fastapi import APIRouter, UploadFile, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.auth.dependencies import get_current_user
from app.db.database import get_db
from app.db.models import Document
from app.documents.parser import extract_text_from_pdf, extract_text_from_csv
from app.documents.chunker import chunk_text
from app.documents.embeddings import embed_text
from app.rag.store import store_chunks

router = APIRouter(prefix="/upload")

@router.post("/{project_id}")
def upload_document(
    project_id: str,
    file: UploadFile,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    # Validate project_id format (must be a UUID)
    try:
        project_uuid = UUID(project_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid project_id. Must be a UUID.",
        )

    # 1️⃣ Extract text from uploaded file
    file_bytes = file.file.read()

    # Decide parser based on content type / filename
    content_type = file.content_type or ""
    filename_lower = (file.filename or "").lower()

    try:
        if "pdf" in content_type or filename_lower.endswith(".pdf"):
            content = extract_text_from_pdf(file_bytes)
        elif "csv" in content_type or filename_lower.endswith(".csv"):
            content = extract_text_from_csv(file_bytes)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported file type. Only PDF and CSV are supported.",
            )
    except HTTPException:
        # Re-raise intentional HTTP errors
        raise
    except Exception:
        # Any parsing error should be a 400 (bad file)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to parse the uploaded file.",
        )

    if not content or not content.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No text could be extracted from the document.",
        )

    # 2️⃣ Save document metadata and raw content in DB
    try:
        document = Document(
            id=None,
            filename=file.filename,
            project_id=project_uuid,
            user_id=current_user.id,
            content=content,
        )
        db.add(document)
        db.commit()
        db.refresh(document)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save document metadata.",
        )

    # 3️⃣ Chunk the extracted text
    chunks = chunk_text(content)

    if not chunks:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Document is empty after processing.",
        )

    # 4️⃣ Create embeddings for each chunk
    try:
        embeddings = embed_text(chunks)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate embeddings for the document.",
        )

    # 5️⃣ Store chunks & embeddings in vector DB
    try:
        store_chunks(
            chunks=chunks,
            embeddings=embeddings,
            user_id=current_user.id,
            project_id=str(project_uuid),
            document_id=str(document.id),
        )
    except Exception:
        # At this point the document is in the SQL DB, but vector indexing failed
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Document saved but failed to index in vector store.",
        )

    return {"status": "Document uploaded & indexed"}
