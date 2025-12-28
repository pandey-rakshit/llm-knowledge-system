from config import settings

from .base import EmbeddingProvider
from .huggingface import HuggingFaceEmbeddingProvider


def get_embedding_provider() -> EmbeddingProvider:
    if settings.EMBEDDING_PROVIDER == "huggingface":
        return HuggingFaceEmbeddingProvider()

    raise ValueError(f"Unsupported embedding provider: {settings.EMBEDDING_PROVIDER}")
