# backend/app/agents/graph/nodes/analyzer_node.py

from app.agents.analyser.agent import AnalyzerAgent
from app.agents.graph.state import AgentState

analyzer = AnalyzerAgent()

def analyzer_node(state: AgentState) -> AgentState:
    # Run analysis and increment iteration counter to prevent infinite loops
    state = analyzer.run(state)
    state["analysis_iterations"] = state.get("analysis_iterations", 0) + 1
    return state
