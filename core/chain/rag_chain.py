from typing import List

from langchain_core.messages import HumanMessage, SystemMessage

from core.llm import get_llm_provider
from core.retriever import RetrieverService
from core.router import QueryRouter, QueryType
from tools.tavily_search import TavilySearchService


class RAGChain:
    def __init__(self, retriever_service: RetrieverService):
        self.retriever_service = retriever_service
        self.llm = get_llm_provider()
        self.router = QueryRouter()

    def run(self, query: str, web_enabled: bool = False, extra_docs: List = None):

        route = self.router.route(query, web_enabled)

        # GREETING
        if route.query_type == QueryType.GREETING:
            answer = self.llm.invoke(
                [
                    SystemMessage(
                        content="You are a helpful assistant. Keep replies short."
                    ),
                    HumanMessage(content=query),
                ]
            )
            return {"answer": answer, "sources": []}

        context_docs = []

        if extra_docs:
            context_docs.extend(extra_docs)

        # DOCUMENT (only if docs exist)
        if route.query_type in {QueryType.DOCUMENT, QueryType.HYBRID}:
            try:
                retriever = self.retriever_service.build_retriever()
                context_docs.extend(retriever.invoke(query))
            except RuntimeError:
                pass

        # WEB (always allowed if enabled)
        if web_enabled:
            context_docs.extend(TavilySearchService().search(query))

        if not context_docs:
            return {
                "answer": "I don't have enough information to answer this question.",
                "sources": [],
            }

        context_blocks = []
        sources = []

        for i, doc in enumerate(context_docs, 1):
            metadata = doc.metadata
            if metadata.get("source_type") == "web":
                context_blocks.append(f"[Web {i}] {doc.page_content}")
                sources.append(f"[Web] {metadata.get('title')} - {metadata.get('url')}")
            elif metadata.get("source_type") == "wikipedia":
                context_blocks.append(f"[Wikipedia {i}] {doc.page_content}")
                sources.append(
                    f"[Wikipedia] {metadata.get('title')} - {metadata.get('url')}"
                )
            else:
                context_blocks.append(f"[Doc {i}] {doc.page_content}")
                sources.append(
                    f"""[Doc] {doc.metadata.get('title')} -
                     Chunk {doc.metadata.get('chunk_index')}"""
                )

        context = "\n\n".join(context_blocks)
        answer = self.llm.invoke(
            [
                SystemMessage(
                    content=(
                        "Answer ONLY using the provided context. "
                        "Cite sources using [Doc X] or [Web X]. "
                        "If the answer is not present, say you don't know."
                    )
                ),
                HumanMessage(content=f"Context:\n{context}\n\nQuestion:\n{query}"),
            ]
        )

        return {"answer": answer, "sources": sources}
