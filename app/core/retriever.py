import numpy as np
from app.db.mongo import fetch_all_docs
from app.core.embeddings import get_embedder
from app.config import settings

def _cosine_sim(a: np.ndarray, b: np.ndarray):
    if a is None or b is None:
        return -1.0
    a_norm = np.linalg.norm(a)
    b_norm = np.linalg.norm(b)
    if a_norm == 0 or b_norm == 0:
        return -1.0
    return float(np.dot(a, b) / (a_norm * b_norm))

def retrieve(query: str, top_k: int = None):
    if top_k is None:
        top_k = settings.top_k

    embedder = get_embedder()
    q_emb = embedder.embed([query])[0]

    all_docs = fetch_all_docs()
    scores = []
    for d in all_docs:
        emb = d.get('embedding')
        if emb is None:
            continue
        sim = _cosine_sim(q_emb, np.array(emb, dtype=float))
        scores.append((sim, d))

    scores.sort(key=lambda x: x[0], reverse=True)
    top = scores[:top_k]
    results = [{'score': s[0], 'doc': s[1]} for s in top]
    return results