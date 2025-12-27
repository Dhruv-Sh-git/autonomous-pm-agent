from typing import Any, Dict, List

from qdrant_client import QdrantClient

from app.documents.embeddings import embed_query


client = QdrantClient(host="qdrant", port=6333)


def retrieve_chunks(query_embedding, user_id, project_id, limit: int = 5):
    """Legacy helper that searches Qdrant by a precomputed embedding.

    Kept for backwards compatibility; new code should use VectorRetriever.
    """
    search = client.search(
        collection_name="documents",
        query_vector=query_embedding,
        limit=limit,
        query_filter={
            "must": [
                {"key": "user_id", "match": {"value": user_id}},
                {"key": "project_id", "match": {"value": project_id}},
            ]
        },
    )

    return [hit.payload.get("text", "") for hit in search]


class VectorRetriever:
    """High-level retriever used by tools.VectorSearchTool.

    Exposes a .search(query, user_id, project_id, limit) method that returns
    a list of {"content": str, "metadata": dict} objects.
    """

    def __init__(self, client: QdrantClient, collection_name: str = "documents") -> None:
        self.client = client
        self.collection_name = collection_name

    def search(
        self,
        query: str,
        user_id: str,
        project_id: str,
        limit: int = 5,
    ) -> List[Dict[str, Any]]:
        # Embed query using the same model as used for document chunks
        query_vec = embed_query(query)[0]

        search = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vec.tolist(),
            limit=limit,
            query_filter={
                "must": [
                    {"key": "user_id", "match": {"value": user_id}},
                    {"key": "project_id", "match": {"value": project_id}},
                ]
            },
        )

        results: List[Dict[str, Any]] = []
        for hit in search:
            payload = hit.payload or {}
            text = payload.get("text") or payload.get("content", "")

            # Everything except the main text goes into metadata
            metadata = dict(payload)
            metadata.pop("text", None)
            metadata.pop("content", None)

            results.append({"content": text, "metadata": metadata})

        return results
