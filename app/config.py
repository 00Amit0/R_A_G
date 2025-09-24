import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    mongo_uri: str = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
    mongo_db: str = os.getenv('MONGO_DB', 'rag_db')
    embedding_model: str = os.getenv('EMBEDDING_MODEL', 'sentence-transformers/all-MiniLM-L6-v2')
    generator_model: str = os.getenv('GENERATOR_MODEL', 'gpt2')
    use_mongo_vector_index: bool = os.getenv('USE_MONGO_VECTOR_INDEX', 'false').lower() == 'true'
    chunk_size: int = int(os.getenv('CHUNK_SIZE', '500'))
    chunk_overlap: int = int(os.getenv('CHUNK_OVERLAP', '50'))
    top_k: int = int(os.getenv('TOP_K', '4'))


settings = Settings()