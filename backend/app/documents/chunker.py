# app/documents/chunker.py

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50):
    """
    Splits the input text into overlapping chunks.
    
    Args:
        text (str): The full text to chunk.
        chunk_size (int): Maximum size of each chunk.
        overlap (int): Number of overlapping characters between chunks.
    
    Returns:
        List[str]: A list of text chunks.
    """
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap  # move start with overlap

    return chunks
