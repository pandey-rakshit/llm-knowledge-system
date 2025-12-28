from abc import ABC, abstractmethod
from typing import Any, Dict, List


class DocumentLoader(ABC):
    @abstractmethod
    def load(self, source: str) -> List[Dict[str, Any]]:
        """
        Load raw documents.
        Returns list of dicts with keys: content, metadata
        """
        pass
