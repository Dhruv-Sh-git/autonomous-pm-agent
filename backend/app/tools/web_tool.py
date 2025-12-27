# backend/app/tools/web_tool.py

from typing import List
from tavily import TavilyClient
from app.agents.graph.state import ResearchResult


class WebSearchTool:
    def __init__(self, api_key: str):
        self.client = TavilyClient(api_key=api_key)

    def run(self, query: str) -> List[ResearchResult]:
        response = self.client.search(
            query=query,
            search_depth="advanced",
            max_results=5
        )

        results: List[ResearchResult] = []

        for item in response.get("results", []):
            results.append({
                "source": "web",
                "content": item.get("content", ""),
                "metadata": {
                    "url": item.get("url"),
                    "title": item.get("title")
                }
            })

        return results
