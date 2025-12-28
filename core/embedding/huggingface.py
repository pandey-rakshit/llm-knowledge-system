from typing import List

from langchain_huggingface import HuggingFaceEmbeddings

from config import settings

from .base import EmbeddingProvider


class HuggingFaceEmbeddingProvider(EmbeddingProvider):
    def __init__(self):
        self.model = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self.model.embed_documents(texts)

    def embed_query(self, text: str) -> List[float]:
        return self.model.embed_query(text)
