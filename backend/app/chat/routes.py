from fastapi import APIRouter, Depends
from app.auth.dependencies import get_current_user
from app.documents.embeddings import embed_query
from app.rag.retriever import retrieve_chunks
from app.llm.groq_client import ask_llm
from app.chat.schemas import ChatRequest

router = APIRouter()

@router.post("/{project_id}")
def chat_with_project(
    project_id: str,
    data: ChatRequest,
    current_user=Depends(get_current_user)
):
    message = data.message

    # 1️⃣ Embed user query
    query_embedding = embed_query(message)

    # 2️⃣ Retrieve relevant chunks
    context_chunks = retrieve_chunks(
        query_embedding=query_embedding,
        user_id=current_user.id,
        project_id=project_id
    )

    # 3️⃣ Build context
    context = "\n".join(context_chunks)

    # 4️⃣ Create prompt
    prompt = f"""
Answer the question using the context below.
If the answer is not in the context, say you don't know.

Context:
{context}

Question:
{message}
"""

    # 5️⃣ Call LLM (Groq)
    response = ask_llm(prompt)

    return {"answer": response}
