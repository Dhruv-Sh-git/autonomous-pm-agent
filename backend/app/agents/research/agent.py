# backend/app/agents/research/agent.py

from langchain_openai import ChatOpenAI
from app.agents.graph.state import AgentState
import json


class ResearchAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0
        )

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
        return json.loads(response.content)
