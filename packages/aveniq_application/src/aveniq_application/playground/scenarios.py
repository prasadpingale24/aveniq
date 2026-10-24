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
    runnable: bool = True
    status: str = "ready"  # ready | planned | draft
    subtitle: str = ""


SCENARIOS: dict[str, ScenarioDefinition] = {
    "b01": ScenarioDefinition(
        scenario_id="b01",
        benchmark_id="b01",
        title="B01-auth-jwt",
        subtitle="clock-skew drift delta",
        description="JWT validation failures after identity provider certificate rotation (fixture pack not wired yet).",
        standin_trigger_path="",
        create_investigation_body={},
        runnable=False,
        status="planned",
    ),
    "b02": ScenarioDefinition(
        scenario_id="b02",
        benchmark_id="b02",
        title="B02-kafka-lag",
        subtitle="consumer stall partition 4",
        description="Order pipeline lag from stuck consumer group on partition 4 (fixture pack not wired yet).",
        standin_trigger_path="",
        create_investigation_body={},
        runnable=False,
        status="planned",
    ),
    "b03": ScenarioDefinition(
        scenario_id="b03",
        benchmark_id="b03",
        title="B03-checkout-pool-exhaustion",
        subtitle="connection pool starvation",
        description=(
            "Simulates checkout-api deployment v2.8.1 reducing DB pool capacity, "
            "inducing HTTP 500 spikes on /v2/orders/checkout."
        ),
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
        runnable=True,
        status="ready",
    ),
    "b04": ScenarioDefinition(
        scenario_id="b04",
        benchmark_id="b04",
        title="B04-redis-oom",
        subtitle="cache stampede cluster",
        description="Redis memory pressure and cache stampede during flash sale (benchmark draft).",
        standin_trigger_path="",
        create_investigation_body={},
        runnable=False,
        status="draft",
    ),
}


def list_scenarios() -> list[ScenarioDefinition]:
    return [SCENARIOS[k] for k in sorted(SCENARIOS)]


def get_scenario(scenario_id: str) -> ScenarioDefinition | None:
    return SCENARIOS.get(scenario_id)
