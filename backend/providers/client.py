import redis
from .router import ModelRouter, RoutingCriteria
from .openai_provider import OpenAIProvider
from .anthropic_provider import AnthropicProvider
from opentelemetry import trace

tracer = trace.get_tracer(__name__)
r = redis.Redis()


class NeuroFlowClient:
    _instance = None

    def __init__(self):
        self.router = ModelRouter()

        self.providers = {
            "openai": OpenAIProvider(api_key="YOUR_KEY"),
            "anthropic": AnthropicProvider(api_key="YOUR_KEY")
        }

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = NeuroFlowClient()
        return cls._instance

    async def chat(self, messages, routing_criteria: RoutingCriteria):
        model_cfg = self.router.route(routing_criteria)
        provider = self.providers[model_cfg["provider"]]

        with tracer.start_as_current_span("llm_call") as span:
            result = await provider.complete(messages)

            span.set_attributes({
                "model": result.model,
                "input_tokens": result.input_tokens,
                "output_tokens": result.output_tokens,
                "cost_usd": result.cost_usd,
                "latency_ms": result.latency_ms
            })

        self._track_metrics(result)

        return result

    async def embed(self, texts: list[str]):
        provider = self.providers["openai"]
        return await provider.embed(texts)

    def _track_metrics(self, result):
        r.incr(f"metrics:model:{result.model}:calls")
        r.incrbyfloat(f"metrics:model:{result.model}:cost_usd", result.cost_usd)