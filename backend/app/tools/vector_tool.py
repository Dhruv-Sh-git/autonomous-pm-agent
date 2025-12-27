# backend/app/tools/vector_tool.py

from typing import List
from app.agents.graph.state import ResearchResult


class VectorSearchTool:
    def __init__(self, retriever):
        """
        retriever: your existing semantic search function or class
        """
        self.retriever = retriever

    def run(self, query: str, user_id: str, project_id: str) -> List[ResearchResult]:
        docs = self.retriever.search(
            query=query,
            user_id=user_id,
            project_id=project_id
        )

        results: List[ResearchResult] = []

        for doc in docs:
            results.append({
                "source": "vector_db",
                "content": doc["content"],
                "metadata": doc.get("metadata", {})
            })

        return results
