from pathlib import Path
from typing import Any, Dict, List

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    WikipediaLoader,
)
from langchain_core.documents import Document

from .base import DocumentLoader


class PDFDocumentLoader(DocumentLoader):
    def load(self, source: str) -> List[Dict[str, Any]]:
        loader = PyPDFLoader(source)
        docs = loader.load()

        return [
            {
                "content": doc.page_content,
                "metadata": {
                    **doc.metadata,
                    "source_type": "pdf",
                    "source": source,
                },
            }
            for doc in docs
        ]


class TextDocumentLoader(DocumentLoader):
    def load(self, source: str) -> List[Dict[str, Any]]:
        loader = TextLoader(source, encoding="utf-8")
        docs = loader.load()

        return [
            {
                "content": doc.page_content,
                "metadata": {
                    **doc.metadata,
                    "source_type": "text",
                    "source": source,
                },
            }
            for doc in docs
        ]


class WikipediaDocumentLoader(DocumentLoader):
    def load(self, source: str):
        loader = WikipediaLoader(query=source, load_max_docs=5)
        docs = loader.load()

        return [
            Document(
                page_content=doc.page_content,
                metadata={
                    "source_type": "wikipedia",
                    "source": source,
                    "title": doc.metadata.get("title"),
                    "url": doc.metadata.get("source"),
                },
            )
            for doc in docs
        ]


def detect_loader(path: str) -> DocumentLoader:
    ext = Path(path).suffix.lower()

    if ext == ".pdf":
        return PDFDocumentLoader()
    if ext in {".txt", ".md"}:
        return TextDocumentLoader()

    raise ValueError(f"Unsupported document type: {path}")
