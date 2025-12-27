# backend/app/agents/run.py

from app.agents.graph.graph import build_agent_graph
from app.agents.graph.state import AgentState

graph = build_agent_graph()


def run_agent(
    user_id: str,
    project_id: str,
    goal: str
) -> AgentState:
    initial_state: AgentState = {
        "user_id": user_id,
        "project_id": project_id,
        "goal": goal,
        "plan": None,
        "internal_research": [],
        "external_research": [],
        "analysis": None,
        "final_output": None,
        "errors": []
    }

    return graph.invoke(initial_state)
