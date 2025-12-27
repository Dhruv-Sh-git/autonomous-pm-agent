# backend/app/agents/graph/nodes/prd_node.py

from app.agents.prd.agent import PRDGeneratorAgent
from app.agents.graph.state import AgentState

prd_agent = PRDGeneratorAgent()

def prd_node(state: AgentState) -> AgentState:
    return prd_agent.run(state)
