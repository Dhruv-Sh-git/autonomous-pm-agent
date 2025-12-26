# app/documents/embeddings.py
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load the model
model = SentenceTransformer("all-MiniLM-L6-v2")

# FAISS index for vector storage
index = faiss.IndexFlatL2(384)
document_store = []

def embed_text(text: str):
    """
    Embeds a text string by splitting it into chunks.
    """
    chunks = [text[i:i+500] for i in range(0, len(text), 500)]
    embeddings = model.encode(chunks)
    index.add(np.array(embeddings).astype('float32'))
    document_store.extend(chunks)
    return embeddings

def embed_query(query: str):
    """
    Embeds a query string (single string, not chunked) to search in the index.
    """
    embedding = model.encode([query])
    return np.array(embedding).astype('float32')

