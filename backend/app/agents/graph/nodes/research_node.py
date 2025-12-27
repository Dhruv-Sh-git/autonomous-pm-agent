# backend/app/agents/graph/nodes/research_node.py

from app.agents.research.agent import ResearchAgent
from app.agents.graph.state import AgentState
from app.tools.vector_tool import VectorSearchTool
from app.tools.web_tool import WebSearchTool
from app.core.dependencies import get_vector_retriever, get_tavily_key

research_agent = ResearchAgent()

vector_tool = VectorSearchTool(get_vector_retriever())
web_tool = WebSearchTool(get_tavily_key())


def research_node(state: AgentState) -> AgentState:
    queries = research_agent.run(state)

    if state["plan"]["needs_internal_research"]:
        for q in queries.get("internal_queries", []):
            results = vector_tool.run(
                query=q,
                user_id=state["user_id"],
                project_id=state["project_id"]
            )
            state["internal_research"].extend(results)

    if state["plan"]["needs_external_research"]:
        for q in queries.get("external_queries", []):
            results = web_tool.run(q)
            state["external_research"].extend(results)

    return state
