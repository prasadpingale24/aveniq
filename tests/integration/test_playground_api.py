from unittest.mock import patch

from fastapi.testclient import TestClient

from aveniq_application.playground.driver import PlaygroundRunResult


def test_list_playground_scenarios(client: TestClient):
    resp = client.get("/api/v1/playground/scenarios")
    assert resp.status_code == 200
    data = resp.json()
    assert any(s["scenario_id"] == "b03" for s in data["scenarios"])


def test_playground_run_unknown_scenario(client: TestClient):
    resp = client.post("/api/v1/playground/scenarios/unknown/runs")
    assert resp.status_code == 404
    assert resp.json()["code"] == "scenario_not_found"


@patch("aveniq_api.playground_routes.run_scenario_inprocess")
def test_playground_run_b03(mock_run, client: TestClient):
    mock_run.return_value = PlaygroundRunResult(
        scenario_id="b03",
        investigation_id="01J9Y2K5Q8Z7X6W5V4U3T2S1R0",
        state="rca_candidate",
        investigation={
            "investigation": {
                "id": "01J9Y2K5Q8Z7X6W5V4U3T2S1R0",
                "benchmark_id": "b03",
                "state": "rca_candidate",
                "created_at": "2026-09-28T15:00:00Z",
                "updated_at": "2026-09-28T15:01:00Z",
                "run_count": 1,
                "signal": {
                    "kind": "alert",
                    "fired_at": "2026-09-28T14:36:00Z",
                    "service": "checkout-api",
                    "description": "checkout-api error rate high",
                },
            },
            "events": [],
            "evidence": [],
            "hypotheses": [],
            "rca": None,
        },
    )
    resp = client.post("/api/v1/playground/scenarios/b03/runs")
    assert resp.status_code == 201
    body = resp.json()
    assert body["scenario_id"] == "b03"
    assert body["investigation_id"] == "01J9Y2K5Q8Z7X6W5V4U3T2S1R0"
