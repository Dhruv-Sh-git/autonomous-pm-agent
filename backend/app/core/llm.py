# app/core/llm.py

from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq

def get_agent_llm():
    return ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

def get_rag_llm():
    return ChatGroq(
        model="llama-3.1-70b",
        temperature=0.2
    )
