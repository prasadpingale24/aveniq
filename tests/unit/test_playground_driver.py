from unittest.mock import MagicMock, patch

import httpx

from aveniq_application.playground.driver import PlaygroundError, run_scenario
from aveniq_application.playground.scenarios import get_scenario


def test_run_scenario_unknown():
    try:
        run_scenario("nope", "http://api", "http://standin")
        assert False, "expected error"
    except PlaygroundError as exc:
        assert exc.code == "scenario_not_found"


def test_run_scenario_b03_happy_path():
    scenario = get_scenario("b03")
    assert scenario is not None

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/playground/reset"):
            return httpx.Response(200, json={"status": "reset"})
        if request.url.path.endswith("/trigger"):
            return httpx.Response(200, json={"status": "triggered"})
        if request.url.path == "/api/v1/investigations" and request.method == "POST":
            return httpx.Response(
                201,
                json={"investigation": {"id": "01J9Y2K5Q8Z7X6W5V4U3T2S1R0", "state": "initialized"}},
            )
        if request.url.path.endswith("/run"):
            return httpx.Response(
                200,
                json={
                    "investigation": {"id": "01J9Y2K5Q8Z7X6W5V4U3T2S1R0", "state": "rca_candidate"},
                    "evidence": [],
                    "hypotheses": [],
                    "events": [],
                },
            )
        if request.method == "GET":
            return httpx.Response(
                200,
                json={
                    "investigation": {"id": "01J9Y2K5Q8Z7X6W5V4U3T2S1R0", "state": "rca_candidate"},
                    "evidence": [],
                    "hypotheses": [],
                    "events": [],
                },
            )
        return httpx.Response(404)

    transport = httpx.MockTransport(handler)
    client = httpx.Client(transport=transport)
    result = run_scenario("b03", "http://api.test", "http://standin.test", client=client)
    assert result.scenario_id == "b03"
    assert result.state == "rca_candidate"
    client.close()
