# backend/app/agents/graph/nodes/research_node.py

from app.agents.research.agent import ResearchAgent
from app.agents.graph.state import AgentState
from app.tools.vector_tool import VectorSearchTool
from app.tools.web_tool import WebSearchTool
from app.core.dependencies import get_vector_retriever, get_tavily_key

research_agent = ResearchAgent()

# Initialize retriever - may be None if Qdrant unavailable
retriever = get_vector_retriever()
vector_tool = VectorSearchTool(retriever) if retriever else None
web_tool = WebSearchTool(get_tavily_key())


def research_node(state: AgentState) -> AgentState:
    queries = research_agent.run(state)

    if state["plan"]["needs_internal_research"] and vector_tool:
        for q in queries.get("internal_queries", []):
            try:
                results = vector_tool.run(
                    query=q,
                    user_id=state["user_id"],
                    project_id=state["project_id"]
                )
                state["internal_research"].extend(results)
            except Exception as e:
                print(f"[Research] Vector search failed: {e}")
    elif state["plan"]["needs_internal_research"]:
        print("[Research] Vector search not available, skipping internal research")

    if state["plan"]["needs_external_research"]:
        for q in queries.get("external_queries", []):
            results = web_tool.run(q)
            state["external_research"].extend(results)

    return state
