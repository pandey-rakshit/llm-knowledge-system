from config import settings

from .base import LLMProvider
from .groq import GroqLLMProvider


def get_llm_provider() -> LLMProvider:
    if settings.LLM_PROVIDER == "groq":
        return GroqLLMProvider()

    raise ValueError(f"Unsupported LLM provider: {settings.LLM_PROVIDER}")
