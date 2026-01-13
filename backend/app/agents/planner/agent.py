# backend/app/agents/planner/agent.py

import json

from app.agents.graph.state import AgentState, PlannerOutput
from app.core.llm import get_agent_llm, parse_llm_json


class PlannerAgent:
    def __init__(self):
        self.llm = get_agent_llm()

    def run(self, state: AgentState) -> AgentState:
        # Guard against extremely long goals; frontend already limits
        # length but API clients might not.
        goal = state["goal"]
        if isinstance(goal, str) and len(goal) > 1500:
            goal = goal[:1500]

        prompt = f"""
You are a senior Product Manager AI.

User Goal:
{goal}

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
        try:
            plan: PlannerOutput = parse_llm_json(response.content)
        except ValueError:
            # As a last resort, fall back to an empty, safe plan
            plan = {
                "steps": [],
                "needs_internal_research": False,
                "needs_external_research": False,
                "confidence_threshold": 0.0,
            }

        state["plan"] = plan
        return state
