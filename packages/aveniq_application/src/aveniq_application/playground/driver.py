from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any, Callable

import httpx

from aveniq_domain.models import Signal

from aveniq_application.playground.scenarios import get_scenario
from aveniq_application.use_cases import RunInvestigationCommand, StartInvestigationCommand


@dataclass
class PlaygroundRunResult:
    scenario_id: str
    investigation_id: str
    state: str
    investigation: dict[str, Any]


def _standin_reset_and_trigger(http: httpx.Client, standin_base: str, scenario) -> None:
    reset = http.post(f"{standin_base}/playground/reset")
    reset.raise_for_status()
    trigger = http.post(f"{standin_base}{scenario.standin_trigger_path}")
    trigger.raise_for_status()


def run_scenario_inprocess(
    scenario_id: str,
    standin_base: str,
    services: Any,
    aggregate_to_payload: Callable[[Any], dict[str, Any]],
    *,
    client: httpx.Client | None = None,
) -> PlaygroundRunResult:
    """Orchestrate via use cases (API path). Stand-in still via HTTP."""
    scenario = get_scenario(scenario_id)
    if scenario is None:
        raise PlaygroundError("scenario_not_found", f"Unknown scenario: {scenario_id}")

    standin_base = standin_base.rstrip("/")
    owns_client = client is None
    http = client or httpx.Client(timeout=30.0)
    try:
        _standin_reset_and_trigger(http, standin_base, scenario)
        body = scenario.create_investigation_body
        signal = Signal.model_validate(body["signal"])
        cmd = StartInvestigationCommand(
            benchmark_id=body["benchmark_id"],
            signal=signal,
            org_id=body.get("org_id"),
            environment_id=body.get("environment_id"),
        )
        aggregate = services.start_investigation.execute(cmd)
        inv_id = aggregate.investigation.id
        aggregate = services.run_investigation.execute(RunInvestigationCommand(inv_id))
        state = aggregate.investigation.state.value
        payload = aggregate_to_payload(aggregate)
        return PlaygroundRunResult(
            scenario_id=scenario_id,
            investigation_id=inv_id,
            state=state,
            investigation=payload,
        )
    except httpx.HTTPError as exc:
        raise PlaygroundError("playground_upstream_error", str(exc)) from exc
    finally:
        if owns_client:
            http.close()


class PlaygroundError(Exception):
    def __init__(self, code: str, message: str) -> None:
        self.code = code
        super().__init__(message)


def run_scenario(
    scenario_id: str,
    api_base: str,
    standin_base: str,
    *,
    poll_timeout_sec: float = 60.0,
    poll_interval_sec: float = 0.5,
    client: httpx.Client | None = None,
) -> PlaygroundRunResult:
    scenario = get_scenario(scenario_id)
    if scenario is None:
        raise PlaygroundError("scenario_not_found", f"Unknown scenario: {scenario_id}")

    api_base = api_base.rstrip("/")
    standin_base = standin_base.rstrip("/")
    owns_client = client is None
    http = client or httpx.Client(timeout=30.0)
    try:
        _standin_reset_and_trigger(http, standin_base, scenario)

        create = http.post(
            f"{api_base}/api/v1/investigations",
            json=scenario.create_investigation_body,
        )
        create.raise_for_status()
        inv_id = create.json()["investigation"]["id"]

        run = http.post(f"{api_base}/api/v1/investigations/{inv_id}/run")
        run.raise_for_status()

        deadline = time.monotonic() + poll_timeout_sec
        payload: dict[str, Any] = run.json()
        investigation: dict[str, Any] = payload["investigation"]
        state = str(investigation.get("state", ""))
        terminal = {"rca_candidate", "inconclusive", "blocked"}
        while state not in terminal and time.monotonic() < deadline:
            time.sleep(poll_interval_sec)
            got = http.get(f"{api_base}/api/v1/investigations/{inv_id}")
            got.raise_for_status()
            payload = got.json()
            investigation = payload["investigation"]
            state = str(investigation.get("state", ""))

        if state not in terminal:
            raise PlaygroundError(
                "playground_timeout",
                f"Investigation {inv_id} did not reach terminal state within {poll_timeout_sec}s",
            )

        return PlaygroundRunResult(
            scenario_id=scenario_id,
            investigation_id=inv_id,
            state=state,
            investigation=payload,
        )
    except httpx.HTTPError as exc:
        raise PlaygroundError("playground_upstream_error", str(exc)) from exc
    finally:
        if owns_client:
            http.close()
