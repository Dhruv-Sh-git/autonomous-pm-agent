# backend/app/agents/graph/nodes/planner_node.py

from app.agents.planner.agent import PlannerAgent
from app.agents.graph.state import AgentState

planner = PlannerAgent()

def planner_node(state: AgentState) -> AgentState:
    return planner.run(state)
