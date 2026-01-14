from langgraph.graph import StateGraph, END

from app.agents.graph.state import AgentState
from app.agents.graph.nodes.planner_node import planner_node
from app.agents.graph.nodes.research_node import research_node
from app.agents.graph.nodes.analyzer_node import analyzer_node
from app.agents.graph.nodes.prd_node import prd_node


def confidence_router(state: AgentState) -> str:
    confidence = state["analysis"]["confidence"]
    threshold = state["plan"]["confidence_threshold"]
    iterations = state.get("analysis_iterations", 0)

    # Hard cap on analysis loops to avoid infinite recursion in the graph.
    MAX_ANALYSIS_ITERATIONS = 3

    if confidence >= threshold or iterations >= MAX_ANALYSIS_ITERATIONS:
        return "generate_prd"
    return "research"


def build_agent_graph():
    graph = StateGraph(AgentState)

    # ---- NODES ----
    graph.add_node("planner", planner_node)
    graph.add_node("research", research_node)
    graph.add_node("analyze", analyzer_node)
    graph.add_node("generate_prd", prd_node)

    # ---- ENTRY ----
    graph.set_entry_point("planner")

    # ---- EDGES ----
    graph.add_edge("planner", "research")
    graph.add_edge("research", "analyze")

    graph.add_conditional_edges(
        "analyze",
        confidence_router,
        {
            "generate_prd": "generate_prd",
            "research": "research"
        }
    )

    graph.add_edge("generate_prd", END)

    # ---- COMPILE ----
    return graph.compile()
