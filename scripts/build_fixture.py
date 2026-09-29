#!/usr/bin/env python3
"""Generate fixtures/b03 from scenarios/b03/definition.yaml."""

from __future__ import annotations

import json
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
SCENARIO = REPO_ROOT / "scenarios" / "b03" / "definition.yaml"
OUT_DIR = REPO_ROOT / "fixtures" / "b03"


def main() -> None:
    data = yaml.safe_load(SCENARIO.read_text(encoding="utf-8"))
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    manifest = {
        "fixture_package_version": "1.0",
        "benchmark_id": data["benchmark_id"],
        "title": data["title"],
        "incident_window": data["incident_window"],
        "environment": data["environment"],
        "primary_service": data["primary_service"],
    }
    (OUT_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    alert = data["alert"]
    (OUT_DIR / "alert.json").write_text(json.dumps(alert, indent=2), encoding="utf-8")

    services = [
        {"name": "checkout-api", "owner": "checkout-team", "dependencies": ["postgresql-checkout"]},
        {"name": "postgresql-checkout", "type": "database"},
    ]
    (OUT_DIR / "services.json").write_text(json.dumps(services, indent=2), encoding="utf-8")

    dep = data["deployment"]
    dep_record = {
        "id": dep["id"],
        "service": dep["service"],
        "version": dep["version"],
        "started_at": dep["started_at"],
        "config_changes": dep["config_changes"],
    }
    (OUT_DIR / "deployments.json").write_text(json.dumps([dep_record], indent=2), encoding="utf-8")

    logs_dir = OUT_DIR / "logs"
    logs_dir.mkdir(exist_ok=True)
    log_lines = [
        {
            "timestamp": "2026-09-28T14:32:00Z",
            "service": "checkout-api",
            "level": "ERROR",
            "message": "Failed to acquire database connection",
            "attributes": {"error_type": "PoolExhausted"},
        },
        {
            "timestamp": "2026-09-28T14:33:00Z",
            "service": "checkout-api",
            "level": "ERROR",
            "message": "Failed to acquire database connection",
            "attributes": {"error_type": "PoolExhausted"},
        },
    ]
    (logs_dir / "checkout-api.jsonl").write_text(
        "\n".join(json.dumps(line) for line in log_lines) + "\n",
        encoding="utf-8",
    )

    metrics_dir = OUT_DIR / "metrics"
    metrics_dir.mkdir(exist_ok=True)
    metric_lines = [
        {
            "timestamp": "2026-09-28T14:30:00Z",
            "service": "checkout-api",
            "metric": "db.pool.utilization",
            "value": 0.99,
            "unit": "ratio",
        },
        {
            "timestamp": "2026-09-28T14:31:00Z",
            "service": "checkout-api",
            "metric": "db.pool.utilization",
            "value": 0.97,
            "unit": "ratio",
        },
    ]
    (metrics_dir / "db.pool.utilization.jsonl").write_text(
        "\n".join(json.dumps(line) for line in metric_lines) + "\n",
        encoding="utf-8",
    )

    gt = {
        "benchmark_id": data["benchmark_id"],
        "root_cause_summary": data["ground_truth"]["root_cause_summary"],
        "root_cause_category": "configuration_change",
        "expected_rca_status": data["ground_truth"]["expected_rca_status"],
        "expected_primary_service": data["primary_service"],
        "expected_dependency": "postgresql-checkout",
        "key_evidence_themes": [
            "deployment_config_change",
            "pool_utilization_spike",
            "connection_errors",
        ],
        "timeline_anchors": [
            {"at": dep["started_at"], "event": "deployment_started"},
            {"at": "2026-09-28T14:32:00Z", "event": "errors_begin"},
        ],
    }
    (OUT_DIR / "ground_truth.json").write_text(json.dumps(gt, indent=2), encoding="utf-8")
    print(f"Wrote fixture package to {OUT_DIR}")


if __name__ == "__main__":
    main()
