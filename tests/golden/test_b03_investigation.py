import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
GROUND_TRUTH = REPO_ROOT / "fixtures" / "b03" / "ground_truth.json"


def test_b03_full_investigation(client):
    assert GROUND_TRUTH.is_file(), "Run: uv run python scripts/build_fixture.py"

    create = client.post(
        "/api/v1/investigations",
        json={
            "benchmark_id": "b03",
            "signal": {
                "kind": "alert",
                "fired_at": "2026-09-28T14:36:00Z",
                "service": "checkout-api",
                "description": "checkout-api error rate high",
            },
        },
    )
    assert create.status_code == 201
    inv_id = create.json()["investigation"]["id"]

    run = client.post(f"/api/v1/investigations/{inv_id}/run")
    assert run.status_code == 200
    body = run.json()

    assert body["investigation"]["state"] == "rca_candidate"
    assert body["rca"] is not None
    assert body["rca"]["status"] == "probable"
    assert "connection pool" in body["rca"]["root_cause"].lower()
    assert len(body["evidence"]) >= 4
    evidence_ids = {e["id"] for e in body["evidence"]}
    assert "ev_b03_alert_001" in evidence_ids
    assert "ev_b03_metric_pool_util_001" in evidence_ids
    assert body["hypotheses"]
    assert "deployment" in body["hypotheses"][0]["statement"].lower()

    for claim in body["rca"]["claims"]:
        for eid in claim["evidence_ids"]:
            assert eid in evidence_ids

    event_types = {e["type"] for e in body["events"]}
    assert "rca.published" in event_types
    assert "evidence.recorded" in event_types


def test_ground_truth_not_required_for_api(client):
    """Eval file exists for harness; API outcome aligns with expected status."""
    gt = json.loads(GROUND_TRUTH.read_text(encoding="utf-8"))
    create = client.post(
        "/api/v1/investigations",
        json={"benchmark_id": "b03", "signal": {"kind": "alert", "service": "checkout-api"}},
    )
    inv_id = create.json()["investigation"]["id"]
    run = client.post(f"/api/v1/investigations/{inv_id}/run")
    assert run.json()["rca"]["status"] == gt["expected_rca_status"]
