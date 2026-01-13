# backend/app/agents/research/agent.py

import json

from app.agents.graph.state import AgentState
from app.core.llm import get_agent_llm, parse_llm_json


class ResearchAgent:
    def __init__(self):
        self.llm = get_agent_llm()

    def run(self, state: AgentState) -> dict:
        prompt = f"""
You are a research agent.

Goal:
{state['goal']}

Planner Instructions:
{json.dumps(state['plan'], indent=2)}

Decide:
- What queries to run on internal documents
- What queries to run on the web

Respond ONLY in JSON:
{{
  "internal_queries": ["..."],
  "external_queries": ["..."]
}}
"""

        response = self.llm.invoke(prompt)
        try:
          return parse_llm_json(response.content)
        except ValueError:
          # Fallback to an empty research plan so pipeline can still proceed
          return {"internal_queries": [], "external_queries": []}
