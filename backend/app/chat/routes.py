from fastapi import APIRouter, Depends
from app.llm.groq_client import call_llm
from app.rag.retriever import retrieve_context
from app.auth.dependencies import get_current_user
from app.db.models import User

router = APIRouter()

SYSTEM_PROMPT = """
You are an autonomous product manager.
Use the provided context to answer.
If the answer is not in context, say you don't know.
"""

@router.post("/{project_id}")
def chat(project_id: str, query: str, user: User = Depends(get_current_user)):
    context = retrieve_context(query, project_id)

    final_prompt = f"""
Context:
{context}

User Question:
{query}
"""

    answer = call_llm(SYSTEM_PROMPT, final_prompt)

    return {"answer": answer}
