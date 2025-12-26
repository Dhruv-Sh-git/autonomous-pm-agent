from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct
import uuid

client = QdrantClient(host="qdrant", port=6333)
COLLECTION_NAME = "documents"


def store_chunks(
    chunks,
    embeddings,
    user_id,
    project_id,
    document_id
):
    points = []

    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "text": chunk,
                    "user_id": user_id,
                    "project_id": project_id,
                    "document_id": document_id
                }
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )
