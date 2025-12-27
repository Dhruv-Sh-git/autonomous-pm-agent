# backend/app/agents/analyzer/agent.py

from langchain_openai import ChatOpenAI
from app.agents.graph.state import AgentState, AnalysisResult
import json


class AnalyzerAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0
        )

    def run(self, state: AgentState) -> AgentState:
        prompt = f"""
You are a senior product analyst AI.

Goal:
{state['goal']}

Internal Research:
{state['internal_research']}

External Research:
{state['external_research']}

Tasks:
1. Extract key insights
2. Identify missing information or weak evidence
3. Assign an overall confidence score between 0 and 1

Respond ONLY in JSON:
{{
  "insights": ["..."],
  "gaps": ["..."],
  "confidence": 0.0
}}
"""

        response = self.llm.invoke(prompt)
        analysis: AnalysisResult = json.loads(response.content)

        state["analysis"] = analysis
        return state
