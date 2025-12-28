from typing import Any, Dict, List
from uuid import uuid4

from .chunker import DocumentChunker
from .loaders import detect_loader


class DocumentProcessor:
    def __init__(self):
        self.chunker = DocumentChunker()

    def process(self, source: str) -> List[Dict[str, Any]]:
        loader = detect_loader(source)
        raw_docs = loader.load(source)

        doc_id = str(uuid4())
        for doc in raw_docs:
            doc["metadata"]["doc_id"] = doc_id

        return self.chunker.chunk(raw_docs)
