from app.config import settings

def chunk_text(text: str, chunk_size: int = None, overlap: int = None):
    if chunk_size is None:
        chunk_size = settings.chunk_size
    if overlap is None:
        overlap = settings.chunk_overlap

    tokens = []
    start = 0
    n = len(text)
    while start < n:
        end = start + chunk_size
        chunk = text[start:end]
        tokens.append(chunk)
        start = end - overlap if end - overlap > start else end
    return tokens