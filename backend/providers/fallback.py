class FallbackChain:
    def __init__(self, providers):
        self.providers = providers

    async def run(self, messages):
        last_error = None

        for provider in self.providers:
            try:
                return await provider.complete(messages)
            except Exception as e:
                last_error = e
                continue

        raise last_error