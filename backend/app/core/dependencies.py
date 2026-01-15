# backend/app/core/dependencies.py

import os
from functools import lru_cache
from typing import Optional

from qdrant_client import QdrantClient

from app.rag.retriever import VectorRetriever


@lru_cache(maxsize=1)
def get_vector_retriever() -> Optional[VectorRetriever]:
    """Singleton-style access to the vector retriever used by VectorSearchTool.

    Uses QDRANT_* env vars that are already defined in .env / docker-compose.
    Returns None if Qdrant is not available (graceful degradation).
    """
    qdrant_host = os.getenv("QDRANT_HOST", "qdrant")
    qdrant_port = int(os.getenv("QDRANT_PORT", "6333"))

    try:
        client = QdrantClient(host=qdrant_host, port=qdrant_port, timeout=5)
        # Test connection
        client.get_collections()
        retriever = VectorRetriever(client=client)
        print(f"[Qdrant] Connected successfully to {qdrant_host}:{qdrant_port}")
        return retriever
    except Exception as e:
        print(f"[Qdrant] Not available: {e}")
        print("[Qdrant] Continuing without vector search capability")
        return None


def get_tavily_key() -> str:
    """Return Tavily API key from environment.

    This is used by WebSearchTool.
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise RuntimeError("TAVILY_API_KEY is not set in the environment")
    return api_key
