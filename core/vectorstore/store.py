import os
from typing import Any, Dict, List

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from config import settings
from core.embedding import get_embedding_provider

FAISS_DIR = settings.FAISS_DIR


class VectorStoreService:
    def __init__(self):
        self.embedding_provider = get_embedding_provider()
        self.store: FAISS | None = None
        self._chunks: List[Dict[str, Any]] = []

        os.makedirs(FAISS_DIR, exist_ok=True)
        self._load_index()

    def add_documents(self, chunks: List[Dict[str, Any]]) -> None:
        self._chunks.extend(chunks)
        self._rebuild_and_persist()

    def remove_document(self, filename: str) -> None:
        self._chunks = [
            c for c in self._chunks if c["metadata"].get("title") != filename
        ]
        self._rebuild_and_persist()

    def _rebuild_and_persist(self):
        if not self._chunks:
            self.store = None
            self._clear_disk()
            return

        documents = [
            Document(
                page_content=c["content"],
                metadata=c["metadata"],
            )
            for c in self._chunks
        ]

        self.store = FAISS.from_documents(
            documents,
            self.embedding_provider.model,
        )

        self.store.save_local(FAISS_DIR)

    def _load_index(self):
        index_path = os.path.join(FAISS_DIR, "index.faiss")
        if not os.path.exists(index_path):
            return

        self.store = FAISS.load_local(
            FAISS_DIR,
            self.embedding_provider.model,
            allow_dangerous_deserialization=True,
        )

    def _clear_disk(self):
        for f in os.listdir(FAISS_DIR):
            os.remove(os.path.join(FAISS_DIR, f))

    def get_store(self) -> FAISS:
        if self.store is None:
            raise RuntimeError("Vector store is empty")
        return self.store
