from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, Distance, VectorParams
import uuid


client = QdrantClient(host="qdrant", port=6333)
COLLECTION_NAME = "documents"
VECTOR_SIZE = 384  # all-MiniLM-L6-v2 embedding dimension


def _ensure_collection():
    """Create the Qdrant collection if it doesn't exist yet.

    Uses the vector size that matches the SentenceTransformer model
    configured in app.documents.embeddings.
    """

    collections = client.get_collections()
    existing = {c.name for c in collections.collections}

    if COLLECTION_NAME not in existing:
        client.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
        )


def store_chunks(
    chunks,
    embeddings,
    user_id,
    project_id,
    document_id,
):
    # Ensure collection exists with the right configuration
    _ensure_collection()

    points = []

    for chunk, embedding in zip(chunks, embeddings):
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "text": chunk,
                    "user_id": user_id,
                    "project_id": project_id,
                    "document_id": document_id,
                },
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
    )
