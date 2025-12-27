# backend/app/agents/prd/agent.py

from langchain_openai import ChatOpenAI
from app.agents.graph.state import AgentState


class PRDGeneratorAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0
        )

    def run(self, state: AgentState) -> AgentState:
        analysis = state["analysis"]

        prompt = f"""
You are an expert Product Manager AI.

Goal:
{state['goal']}

Validated Insights:
{analysis['insights']}

Known Gaps:
{analysis['gaps']}

Generate a Product Requirements Document in MARKDOWN format
with the following sections:

- Problem Statement
- Goals & Success Metrics
- Target Users
- Functional Requirements
- Non-Functional Requirements
- Out of Scope
- Open Questions

Rules:
- Use only the provided insights
- Do NOT invent research
- Be concise and structured
"""

        response = self.llm.invoke(prompt)
        state["final_output"] = response.content
        return state
