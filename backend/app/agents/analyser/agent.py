# backend/app/agents/analyzer/agent.py

import json
from typing import List

from app.agents.graph.state import AgentState, AnalysisResult, ResearchResult
from app.core.llm import get_agent_llm, parse_llm_json


class AnalyzerAgent:
    def __init__(self):
        self.llm = get_agent_llm()

    def run(self, state: AgentState) -> AgentState:
        # Truncate very large research payloads so prompts stay within
        # Groq's token limits on the on-demand tier.
        def _truncate_research(
            items: List[ResearchResult],
            max_items: int = 5,
            max_chars: int = 1200,
        ) -> List[ResearchResult]:
            trimmed: List[ResearchResult] = []
            for item in items[:max_items]:
                content = item.get("content", "")
                if isinstance(content, str) and len(content) > max_chars:
                    content = content[:max_chars]
                trimmed.append(
                    {
                        "source": item.get("source", "unknown"),
                        "content": content,
                        "metadata": item.get("metadata", {}),
                    }
                )
            return trimmed

        internal_research = _truncate_research(state["internal_research"])
        external_research = _truncate_research(state["external_research"])

        prompt = f"""
You are a senior product analyst AI.

Goal:
{state['goal']}

Internal Research:
{json.dumps(internal_research, indent=2)}

External Research:
{json.dumps(external_research, indent=2)}

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
        try:
            analysis: AnalysisResult = parse_llm_json(response.content)
        except ValueError:
          # Fallback: minimal, low-confidence analysis to keep graph running
            analysis = {
                "insights": [],
                "gaps": ["Failed to parse analysis JSON from LLM."],
                "confidence": 0.0,
            }

        state["analysis"] = analysis
        return state
