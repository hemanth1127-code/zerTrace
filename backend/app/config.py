import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GOOGLE_API_KEY: str = ""
    GEMMA_MODEL: str = "gemma-4-26b-a4b-it"
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    CHROMA_PERSIST_DIRECTORY: str = "./data/chroma"
    UPLOAD_DIRECTORY: str = "./data/uploads"
    CHUNK_SIZE: int = 800
    CHUNK_OVERLAP: int = 150
    TOP_K: int = 3
    RELEVANCE_THRESHOLD: float = 0.25
    ENABLE_RERANKER: bool = False
    FRONTEND_ORIGIN: str = "http://localhost:5174"
    MAX_UPLOAD_MB: int = 20

    class Config:
        env_file = ".env"

settings = Settings()
