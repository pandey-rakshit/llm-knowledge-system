from dataclasses import dataclass
from enum import Enum

from langchain_core.messages import HumanMessage, SystemMessage

from core.llm import get_llm_provider


class QueryType(str, Enum):
    GREETING = "GREETING"
    DOCUMENT = "DOCUMENT"
    WEB = "WEB"
    HYBRID = "HYBRID"
    REFUSE = "REFUSE"


@dataclass(frozen=True)
class QueryRoute:
    query_type: QueryType
    allow_web: bool


class QueryRouter:
    def __init__(self):
        self.llm = get_llm_provider()
        self.system_prompt = (
            "You are an intent classifier for a search system.\n"
            "Classify the user query into exactly ONE label:\n"
            "GREETING, DOCUMENT, WEB, HYBRID\n"
            "Return ONLY the label.\n"
            "No Extra Text"
        )

    def route(self, query: str, web_enabled: bool) -> QueryRoute:
        raw = (
            self.llm.invoke(
                [
                    SystemMessage(content=self.system_prompt),
                    HumanMessage(content=query),
                ]
            )
            .strip()
            .upper()
        )

        try:
            intent = QueryType(raw)
        except ValueError:
            intent = QueryType.DOCUMENT

        if intent == QueryType.GREETING:
            return QueryRoute(QueryType.GREETING, False)

        if web_enabled:
            return QueryRoute(intent, True)

        if intent == QueryType.WEB:
            return QueryRoute(QueryType.REFUSE, False)

        if intent == QueryType.HYBRID:
            return QueryRoute(QueryType.DOCUMENT, False)

        return QueryRoute(intent, False)
