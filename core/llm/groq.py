from typing import List

from langchain_core.messages import BaseMessage
from langchain_groq import ChatGroq

from config import settings

from .base import LLMProvider


class GroqLLMProvider(LLMProvider):
    def __init__(self):
        self.client = ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model=settings.LLM_MODEL,
            max_tokens=settings.MAX_TOKENS,
        )

    def invoke(self, messages: List[BaseMessage]) -> str:
        response = self.client.invoke(messages)
        return response.content
