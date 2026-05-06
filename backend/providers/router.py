import json
import redis
from dataclasses import dataclass

r = redis.Redis()

@dataclass
class RoutingCriteria:
    task_type: str
    max_cost_per_call: float | None = None
    require_vision: bool = False
    require_long_context: bool = False
    latency_budget_ms: int | None = None
    prefer_fine_tuned: bool = False


class ModelRouter:
    def __init__(self):
        pass

    def _load_models(self):
        data = r.get("router:models")
        return json.loads(data) if data else []

    def route(self, criteria: RoutingCriteria):
        models = self._load_models()

        # Vision filter
        if criteria.require_vision:
            models = [m for m in models if m["vision"]]

        # Long context
        if criteria.require_long_context:
            models = [m for m in models if m["context_window"] > 100_000]

        # Evaluation rule
        if criteria.task_type == "evaluation":
            models = [m for m in models if m["is_judge"]]

        # Fine-tuned preference
        if criteria.prefer_fine_tuned:
            ft = [m for m in models if m.get("fine_tuned")]
            if ft:
                models = ft

        # Cost filtering (rough estimate)
        if criteria.max_cost_per_call:
            models = [
                m for m in models
                if m["avg_cost"] <= criteria.max_cost_per_call
            ]

        # Default: cheapest
        if not models:
            raise ValueError("No model satisfies constraints")

        models.sort(key=lambda x: x["avg_cost"])
        return models[0]