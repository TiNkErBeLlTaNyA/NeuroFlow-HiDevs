import time
from anthropic import AsyncAnthropic
from typing import AsyncGenerator
from .base import BaseLLMProvider, ChatMessage, GenerationResult

class AnthropicProvider(BaseLLMProvider):
    def __init__(self, api_key: str, model: str = "claude-3-haiku-20240307"):
        self.client = AsyncAnthropic(api_key=api_key)
        self.model = model

    def _split_system(self, messages):
        system = None
        filtered = []

        for m in messages:
            if m.role == "system":
                system = m.content
            else:
                filtered.append({"role": m.role, "content": m.content})

        return system, filtered

    async def complete(self, messages: list[ChatMessage], **kwargs) -> GenerationResult:
        start = time.time()
        system, msgs = self._split_system(messages)

        res = await self.client.messages.create(
            model=self.model,
            system=system,
            messages=msgs,
            **kwargs
        )

        latency = (time.time() - start) * 1000

        input_tokens = res.usage.input_tokens
        output_tokens = res.usage.output_tokens

        return GenerationResult(
            content=res.content[0].text,
            model=self.model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            latency_ms=latency,
            cost_usd=0.0,  # add pricing table if needed
            finish_reason=res.stop_reason
        )

    async def stream(self, messages: list[ChatMessage], **kwargs) -> AsyncGenerator[str, None]:
        system, msgs = self._split_system(messages)

        stream = await self.client.messages.create(
            model=self.model,
            system=system,
            messages=msgs,
            stream=True,
            **kwargs
        )

        async for event in stream:
            if event.type == "content_block_delta":
                yield event.delta.text

    async def embed(self, texts: list[str]) -> list[list[float]]:
        raise NotImplementedError("Anthropic embeddings not supported")

    @property
    def cost_per_input_token(self) -> float:
        return 0.0

    @property
    def cost_per_output_token(self) -> float:
        return 0.0

    @property
    def context_window(self) -> int:
        return 200_000