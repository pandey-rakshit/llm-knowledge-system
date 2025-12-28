from langchain_core.retrievers import BaseRetriever

from config import settings


class RetrieverService:
    def __init__(self, vector_store_service):
        self.vector_store_service = vector_store_service

    def build_retriever(self) -> BaseRetriever:
        store = self.vector_store_service.get_store()
        return store.as_retriever(search_kwargs={"k": settings.TOP_K})
