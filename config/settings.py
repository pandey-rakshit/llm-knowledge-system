import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


def _validate_env(var_name: str) -> str:
    value = os.getenv(var_name)
    if not value:
        raise EnvironmentError(f"Missing required environment variable: {var_name}")
    return value


@dataclass(frozen=True)
class AppSettings:
    # Chunking
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", 800))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", 150))

    # Retrieval
    TOP_K: int = int(os.getenv("TOP_K", 4))

    # Embeddings (free / local-first)
    EMBEDDING_PROVIDER: str = os.getenv("EMBEDDING_PROVIDER", "huggingface")
    EMBEDDING_MODEL: str = os.getenv(
        "EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
    )

    # LLM (Groq)
    LLM_PROVIDER: str = "groq"
    LLM_MODEL: str = os.getenv("LLM_MODEL", "llama-3.1-8b-instant")
    LLM_TEMPERATURE: float = 0.6

    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", 768))

    # API Keys
    GROQ_API_KEY: str = _validate_env("GROQ_API_KEY")

    # Tavily
    TAVILY_API_KEY: str = _validate_env("TAVILY_API_KEY")

    # Safety
    ALLOW_TOOLS: bool = False

    UPLOAD_DIR = "data/uploads"
    FAISS_DIR = "data/faiss"


settings = AppSettings()
