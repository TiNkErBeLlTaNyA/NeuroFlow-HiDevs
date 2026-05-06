from abc import ABC, abstractmethod
from typing import AsyncGenerator
from dataclasses import dataclass


@dataclass
class ChatMessage:
    role: str  # "system" | "user" | "assistant"
    content: str | list  # str for text, list for multi-modal


@dataclass
class GenerationResult:
    content: str
    model: str
    input_tokens: int
    output_tokens: int
    latency_ms: float
    cost_usd: float
    finish_reason: str


class BaseLLMProvider(ABC):

    @abstractmethod
    async def complete(
        self,
        messages: list[ChatMessage],
        **kwargs
    ) -> GenerationResult:
        """Run a full completion (non-streaming)."""
        pass

    @abstractmethod
    async def stream(
        self,
        messages: list[ChatMessage],
        **kwargs
    ) -> AsyncGenerator[str, None]:
        """Stream tokens progressively."""
        pass

    @abstractmethod
    async def embed(
        self,
        texts: list[str]
    ) -> list[list[float]]:
        """Generate embeddings for input texts."""
        pass

    @property
    @abstractmethod
    def cost_per_input_token(self) -> float:
        """Cost per input token (USD)."""
        pass

    @property
    @abstractmethod
    def cost_per_output_token(self) -> float:
        """Cost per output token (USD)."""
        pass

    @property
    @abstractmethod
    def context_window(self) -> int:
        """Maximum context window size."""
        pass