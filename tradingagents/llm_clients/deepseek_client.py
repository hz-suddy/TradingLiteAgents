import os
from typing import Any, Optional

from langchain_openai import ChatOpenAI

from .base_client import BaseLLMClient
from .validators import validate_model


class DeepSeekClient(BaseLLMClient):
    """Client for DeepSeek models via OpenAI-compatible API.
    
    DeepSeek provides an OpenAI-compatible endpoint, so we use ChatOpenAI
    with a custom base_url.
    """

    def __init__(
        self,
        model: str,
        base_url: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(model, base_url, **kwargs)

    def get_llm(self) -> Any:
        """Return configured ChatOpenAI instance for DeepSeek."""
        llm_kwargs = {"model": self.model}

        # Use DeepSeek's OpenAI-compatible endpoint
        llm_kwargs["base_url"] = self.base_url or "https://api.deepseek.com/v1"
        
        # Get API key from environment
        api_key = self.kwargs.get("api_key") or os.environ.get("DEEPSEEK_API_KEY")
        if api_key:
            llm_kwargs["api_key"] = api_key

        # Pass through supported kwargs
        for key in ("timeout", "max_retries", "api_key", "callbacks", "http_client", "http_async_client"):
            if key in self.kwargs:
                llm_kwargs[key] = self.kwargs[key]

        return ChatOpenAI(**llm_kwargs)

    def validate_model(self) -> bool:
        """Validate model for DeepSeek provider."""
        return validate_model("deepseek", self.model)
