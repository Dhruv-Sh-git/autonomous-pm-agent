# backend/app/agents/planner/agent.py

from langchain_openai import ChatOpenAI
from app.agents.graph.state import AgentState, PlannerOutput
import json


class PlannerAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0
        )

    def run(self, state: AgentState) -> AgentState:
        prompt = f"""
You are a senior Product Manager AI.

User Goal:
{state['goal']}

Decide:
- Steps required to achieve this goal
- Whether internal documents are needed
- Whether external web research is needed
- A confidence threshold (0–1)

Respond ONLY in valid JSON with this schema:

{{
  "steps": [
    {{
      "name": "string",
      "description": "string",
      "tool": "vector_db | web | null"
    }}
  ],
  "needs_internal_research": true | false,
  "needs_external_research": true | false,
  "confidence_threshold": 0.0
}}
"""

        response = self.llm.invoke(prompt)
        plan: PlannerOutput = json.loads(response.content)

        state["plan"] = plan
        return state
