# backend/app/agents/graph/nodes/analyzer_node.py

from app.agents.analyser.agent import AnalyzerAgent
from app.agents.graph.state import AgentState

analyzer = AnalyzerAgent()

def analyzer_node(state: AgentState) -> AgentState:
    return analyzer.run(state)
