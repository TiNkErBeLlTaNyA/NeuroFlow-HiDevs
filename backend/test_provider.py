import asyncio
from providers.openai_provider import OpenAIProvider
from providers.base import ChatMessage

async def main():
    provider = OpenAIProvider(api_key=None)

    print("Embedding test:")
    emb = await provider.embed(["hello world"])
    print(len(emb), "vectors")

    print("\nStreaming test:")
    async for token in provider.stream([
        ChatMessage(role="user", content="Say one word")
    ]):
        print(token, end="", flush=True)

asyncio.run(main())