from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ScenarioDefinition:
    scenario_id: str
    benchmark_id: str
    title: str
    description: str
    standin_trigger_path: str
    create_investigation_body: dict[str, Any]


SCENARIOS: dict[str, ScenarioDefinition] = {
    "b03": ScenarioDefinition(
        scenario_id="b03",
        benchmark_id="b03",
        title="Database connection exhaustion",
        description="checkout-api error rate high after deployment reduced DB pool size",
        standin_trigger_path="/playground/scenarios/b03/trigger",
        create_investigation_body={
            "benchmark_id": "b03",
            "signal": {
                "kind": "alert",
                "fired_at": "2026-09-28T14:36:00Z",
                "service": "checkout-api",
                "description": "checkout-api error rate high",
            },
        },
    ),
}


def list_scenarios() -> list[ScenarioDefinition]:
    return list(SCENARIOS.values())


def get_scenario(scenario_id: str) -> ScenarioDefinition | None:
    return SCENARIOS.get(scenario_id)
