from sentence_transformers import SentenceTransformer
from app.config import settings


class EmbeddingModel:
    def __init__(self, model_name: str = None):
        self.model_name = model_name or settings.embedding_model
        self._model = None


    @property
    def model(self):
        if self._model is None:
            print(f'Loading embedding model: {self.model_name}')
            self._model = SentenceTransformer(self.model_name)
        return self._model


    def embed(self, texts):
    # texts: str or list[str]
        return self.model.encode(texts, show_progress_bar=False, convert_to_numpy=True)


# Singleton wrapper
_embedder = None


def get_embedder():
    global _embedder
    if _embedder is None:
        _embedder = EmbeddingModel()
    return _embedder