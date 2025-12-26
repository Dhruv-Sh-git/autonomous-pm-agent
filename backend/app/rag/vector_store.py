from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct
import uuid

client = QdrantClient(host="qdrant", port=6333)
COLLECTION = "documents"

def store_chunks(chunks, embeddings, user_id, project_id, document_id):
    points = []

    for i, vector in enumerate(embeddings):
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={
                    "user_id": user_id,
                    "project_id": project_id,
                    "document_id": document_id,
                    "text": chunks[i]
                }
            )
        )

    client.upsert(collection_name=COLLECTION, points=points)
