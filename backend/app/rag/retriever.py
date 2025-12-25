import numpy as np
from app.documents.embeddings import index, document_store, model


def retrieve_context(query: str, top_k=3):
    query_vec = model.encode([query])
    distances, indices = index.search(np.array(query_vec), top_k)

    return [document_store[i] for i in indices[0]]
