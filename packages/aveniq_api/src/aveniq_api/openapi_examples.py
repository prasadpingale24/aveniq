"""Examples embedded in served OpenAPI (/docs). Keep aligned with engineering/api/openapi.yaml."""

B03_CREATE_REQUEST = {
    "benchmark_id": "b03",
    "signal": {
        "kind": "alert",
        "fired_at": "2026-09-28T14:36:00Z",
        "service": "checkout-api",
        "description": "checkout-api error rate high",
    },
}

# Illustrative id for path-param hints in Swagger (actual ids are generated at create time).
EXAMPLE_INVESTIGATION_ID = "01J9Y2K5Q8Z7X6W5V4U3T2S1R0"

B03_INVESTIGATION_AFTER_RUN = {
    "investigation": {
        "id": EXAMPLE_INVESTIGATION_ID,
        "benchmark_id": "b03",
        "state": "rca_candidate",
        "created_at": "2026-09-28T15:00:00Z",
        "updated_at": "2026-09-28T15:00:05Z",
        "run_count": 1,
        "org_id": None,
        "environment_id": None,
        "incident_window": {
            "start": "2026-09-28T14:28:00Z",
            "end": "2026-09-28T14:45:00Z",
        },
        "run_completed_at": "2026-09-28T15:00:05Z",
        "signal": B03_CREATE_REQUEST["signal"],
    },
    "events": [
        {
            "seq": 1,
            "type": "investigation.created",
            "occurred_at": "2026-09-28T15:00:00Z",
            "payload": {"benchmark_id": "b03"},
        },
        {
            "seq": 2,
            "type": "rca.published",
            "occurred_at": "2026-09-28T15:00:05Z",
            "payload": {"rca_status": "probable"},
        },
    ],
    "evidence": [
        {
            "id": "ev_b03_alert_001",
            "source": "fixture",
            "source_type": "alert",
            "entity": "checkout-api",
            "observation": "Alert checkout-api error rate high fired at 2026-09-28T14:36:00Z",
            "event_time": "2026-09-28T14:36:00Z",
            "retrieved_at": "2026-09-28T15:00:01Z",
            "strength": "direct",
            "provenance": {
                "connector": "fixture_metadata",
                "fixture_path": "fixtures/b03/alert.json",
                "fixture_ref": "alert.json",
            },
        },
        {
            "id": "ev_b03_metric_pool_util_001",
            "source": "fixture",
            "source_type": "telemetry_metric",
            "entity": "checkout-api",
            "observation": "db.pool.utilization reached 0.99 during incident window",
            "event_time": "2026-09-28T14:30:00Z",
            "retrieved_at": "2026-09-28T15:00:02Z",
            "strength": "derived",
            "provenance": {
                "connector": "fixture_telemetry",
                "fixture_path": "fixtures/b03/metrics/db.pool.utilization.jsonl",
                "fixture_ref": "metrics/db.pool.utilization.jsonl#1",
            },
        },
    ],
    "hypotheses": [
        {
            "id": "hyp_b03_h1",
            "statement": (
                "Recent deployment reduced database connection pool capacity, "
                "leading to connection exhaustion and checkout-api errors."
            ),
            "status": "supported",
            "supporting_evidence_ids": [
                "ev_b03_alert_001",
                "ev_b03_log_errors_001",
                "ev_b03_metric_pool_util_001",
                "ev_b03_deploy_001",
            ],
            "contradicting_evidence_ids": [],
        }
    ],
    "rca": {
        "status": "probable",
        "summary": "Deployment reduced DB pool size; connection exhaustion caused checkout-api errors.",
        "root_cause": (
            "A production deployment (v2.8.1) reduced the database connection pool max size, "
            "causing connection pool exhaustion."
        ),
        "contributing_factors": [],
        "causal_chain": [
            "Configuration change (pool max 50→5)",
            "Connection pool exhaustion",
            "DB acquisition failures",
            "checkout-api HTTP errors",
        ],
        "timeline": [
            {
                "at": "2026-09-28T14:29:00Z",
                "description": "checkout-api v2.8.1 deployment started",
            },
            {
                "at": "2026-09-28T14:32:00Z",
                "description": "Database connection errors observed",
            },
        ],
        "affected_components": ["checkout-api", "postgresql-checkout"],
        "claims": [
            {
                "id": "claim_b03_2",
                "text": "Connection pool utilization peaked at 99%",
                "evidence_ids": ["ev_b03_metric_pool_util_001"],
            }
        ],
        "contradicting_evidence_ids": [],
        "uncertainty": "Distributed tracing not used; request-level impact not verified.",
        "evidence_gaps": [],
        "remediation": ["Roll back or increase database.pool.max_size"],
        "observability_lessons": ["Alert on db.pool.utilization before error rate spikes"],
    },
}
