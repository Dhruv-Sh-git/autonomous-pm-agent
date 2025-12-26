from qdrant_client import QdrantClient

client = QdrantClient(host="qdrant", port=6333)

def retrieve_chunks(query_embedding, user_id, project_id, limit=5):
    search = client.search(
        collection_name="documents",
        query_vector=query_embedding,
        limit=limit,
        query_filter={
            "must": [
                {"key": "user_id", "match": {"value": user_id}},
                {"key": "project_id", "match": {"value": project_id}},
            ]
        }
    )

    return [hit.payload["text"] for hit in search]
