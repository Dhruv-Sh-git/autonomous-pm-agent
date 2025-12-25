from app.rag.retriever import retrieve_context
from app.rag.generator import generate_answer


def rag_pipeline(query: str):
    context = retrieve_context(query)
    return generate_answer(query, "\n".join(context))
