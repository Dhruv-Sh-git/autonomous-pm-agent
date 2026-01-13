"""Central LLM factory functions.

All agents and RAG flows should obtain their chat model from here so that
the same Groq model and API are used consistently across the system.
"""

import json
import os
from typing import Any, TypeVar

from langchain_groq import ChatGroq


GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")

T = TypeVar("T")


def get_agent_llm() -> ChatGroq:
    """LLM used by planner / analyzer / PRD / research agents.

    Uses Groq via langchain_groq, no OpenAI dependency.
    """

    # Cap completion length to keep total tokens within free/on-demand limits.
    return ChatGroq(
        model=GROQ_MODEL,
        temperature=0,
        max_tokens=800,
    )


def get_rag_llm() -> ChatGroq:
    """LLM used for RAG-style flows where some creativity is allowed."""

    return ChatGroq(
        model=GROQ_MODEL,
        temperature=0.2,
        max_tokens=800,
    )


def parse_llm_json(raw: str) -> Any:
    """Best-effort JSON parsing for LLM responses.

    Handles common patterns like Markdown code fences and leading/trailing
    text before/after the JSON object.
    Raises ValueError if no JSON object can be parsed.
    """

    if raw is None:
        raise ValueError("Empty LLM response")

    text = raw.strip()

    # Strip Markdown code fences if present
    if text.startswith("```"):
        # Remove first fence
        text = text.split("\n", 1)[1] if "\n" in text else ""
        # Remove trailing fence
        if "```" in text:
            text = text.rsplit("```", 1)[0]
        text = text.strip()

    # Fast path: try as-is
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Fuzzy path: take substring from first "{" to last "}"
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        candidate = text[start : end + 1]
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            pass

    raise ValueError("Failed to parse JSON from LLM response")
