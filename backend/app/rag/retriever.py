from typing import Any, Dict, List

from qdrant_client import QdrantClient
from qdrant_client.http.models import Filter, FieldCondition, MatchValue

from app.documents.embeddings import embed_query


client = QdrantClient(host="qdrant", port=6333)


def _search_points(
    qdrant: QdrantClient,
    collection_name: str,
    query_vector,
    query_filter: Dict[str, Any],
    limit: int,
):
    """Compatibility wrapper for Qdrant search.

    Tries multiple client methods to support different qdrant-client versions:

    1. ``.search`` (newer high-level API)
    2. ``.search_points`` (older API)
    3. ``.query_points`` (alternative modern API)
    """

    def _normalize(result):
        """Return a plain list of scored points for any backend result."""

        # QueryResponse (from `query_points`) exposes `.points`
        if hasattr(result, "points"):
            return result.points

        return result

    # Newer qdrant-client versions expose `.search`
    if hasattr(qdrant, "search"):
        res = qdrant.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=limit,
            query_filter=query_filter,
        )
        return _normalize(res)

    # Older / alternative API: `.search_points` with Filter
    if hasattr(qdrant, "search_points"):
        flt = Filter(
            must=[
                FieldCondition(
                    key=cond["key"],
                    match=MatchValue(value=cond["match"]["value"]),
                )
                for cond in query_filter.get("must", [])
            ]
        )
        res = qdrant.search_points(
            collection_name=collection_name,
            query=query_vector,
            limit=limit,
            filter=flt,
        )
        return _normalize(res)

    # Some recent versions expose `.query_points` instead
    if hasattr(qdrant, "query_points"):
        flt = Filter(
            must=[
                FieldCondition(
                    key=cond["key"],
                    match=MatchValue(value=cond["match"]["value"]),
                )
                for cond in query_filter.get("must", [])
            ]
        )
        res = qdrant.query_points(
            collection_name=collection_name,
            query=query_vector,
            query_filter=flt,
            limit=limit,
        )
        return _normalize(res)

    raise RuntimeError("QdrantClient has no compatible search method (tried 'search', 'search_points', 'query_points')")


def retrieve_chunks(query_embedding, user_id, project_id, limit: int = 5):
    """Legacy helper that searches Qdrant by a precomputed embedding.

    Kept for backwards compatibility; new code should use VectorRetriever.
    """
    search = _search_points(
        qdrant=client,
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

        search = _search_points(
            qdrant=self.client,
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
