# backend/app/core/dependencies.py

import os
from functools import lru_cache

from qdrant_client import QdrantClient

from app.rag.retriever import VectorRetriever


@lru_cache(maxsize=1)
def get_vector_retriever() -> VectorRetriever:
    """Singleton-style access to the vector retriever used by VectorSearchTool.

    Uses QDRANT_* env vars that are already defined in .env / docker-compose.
    """
    qdrant_host = os.getenv("QDRANT_HOST", "qdrant")
    qdrant_port = int(os.getenv("QDRANT_PORT", "6333"))

    client = QdrantClient(host=qdrant_host, port=qdrant_port)
    retriever = VectorRetriever(client=client)
    return retriever


def get_tavily_key() -> str:
    """Return Tavily API key from environment.

    This is used by WebSearchTool.
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise RuntimeError("TAVILY_API_KEY is not set in the environment")
    return api_key
