from typing import Any, Dict, List

from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import settings


class DocumentChunker:
    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            separators=["\n\n", "\n", " ", ""],
        )

    def chunk(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        chunks: List[Dict[str, Any]] = []

        for doc in documents:
            texts = self.splitter.split_text(doc["content"])
            for idx, text in enumerate(texts):
                chunks.append(
                    {
                        "content": text,
                        "metadata": {
                            **doc["metadata"],
                            "chunk_index": idx,
                        },
                    }
                )

        return chunks
