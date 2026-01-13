# app/llm/groq_client.py

"""Simple helper for chat-style calls to Groq.

Backed by langchain_groq.ChatGroq so it uses the same Groq model and
API surface as the rest of the agent and LangGraph stack.
"""

import os

from langchain_groq import ChatGroq


GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")

_llm = ChatGroq(
    model=GROQ_MODEL,
    temperature=0.2,
)


def ask_llm(prompt: str) -> str:
    """Send a prompt to Groq and return the response text content."""

    response = _llm.invoke(prompt)
    return response.content
