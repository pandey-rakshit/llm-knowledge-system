import os
from typing import List

from langchain_core.documents import Document
from langchain_tavily import TavilySearch

from config.settings import settings


class TavilySearchService:
    def __init__(self, max_results: int = 5, topic: str = "general"):
        os.environ["TAVILY_API_KEY"] = settings.TAVILY_API_KEY

        self.search_tool = TavilySearch(
            max_results=max_results,
            topic=topic,
        )

    def search(self, query: str) -> List[Document]:
        results = self.search_tool.invoke(query)

        documents: List[Document] = []

        if not results or not results.get("results"):
            return documents

        for item in results["results"]:
            documents.append(
                Document(
                    page_content=item.get("content", ""),
                    metadata={
                        "source_type": "web",
                        "title": item.get("title", "Web Result"),
                        "url": item.get("url"),
                        "source_id": "tavily",
                    },
                )
            )

        return documents
