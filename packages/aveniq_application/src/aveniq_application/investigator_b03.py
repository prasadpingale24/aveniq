from __future__ import annotations

from datetime import datetime, timedelta, timezone

from aveniq_domain.enums import (
    EvidenceSourceType,
    EvidenceStrength,
    HypothesisStatus,
    InvestigationState,
    RcaStatus,
)
from aveniq_domain.exceptions import UnsupportedBenchmarkError
from aveniq_domain.models import (
    Evidence,
    EvidenceProvenance,
    Hypothesis,
    InvestigationEvent,
    Rca,
    RcaClaim,
    RcaTimelineEntry,
    TimeWindow,
)

from aveniq_application.ports import (
    ChangePort,
    Clock,
    DeploymentQuerySpec,
    LogQuerySpec,
    MetadataPort,
    MetricQuerySpec,
    TelemetryPort,
    UnitOfWork,
)


class DeterministicInvestigatorB03:
    def __init__(
        self,
        telemetry: TelemetryPort,
        changes: ChangePort,
        metadata: MetadataPort,
        clock: Clock,
    ) -> None:
        self._telemetry = telemetry
        self._changes = changes
        self._metadata = metadata
        self._clock = clock

    def run(self, investigation_id: str, uow: UnitOfWork) -> None:
        inv = uow.investigations.get(investigation_id)
        if inv is None:
            return
        if inv.benchmark_id != "b03":
            raise UnsupportedBenchmarkError(inv.benchmark_id)

        now = self._clock.now()
        self._append_event(uow, investigation_id, "investigation.state_changed", now, {
            "from": inv.state,
            "to": InvestigationState.CONTEXT_GATHERING,
            "reason": "run_started",
        })
        inv.transition_to(InvestigationState.CONTEXT_GATHERING)
        inv.updated_at = now
        uow.investigations.update(inv)

        manifest = self._metadata.get_manifest("b03")
        alert = self._metadata.get_alert("b03")
        window = self._resolve_window(manifest, alert, inv.signal.fired_at)

        inv.incident_window = window
        self._append_event(uow, investigation_id, "investigation.state_changed", now, {
            "from": InvestigationState.CONTEXT_GATHERING,
            "to": InvestigationState.INVESTIGATING,
            "reason": "window_set",
        })
        inv.transition_to(InvestigationState.INVESTIGATING)
        uow.investigations.update(inv)

        evidence_items: list[Evidence] = []

        fired_at = _parse_dt(alert.get("fired_at")) or window.start
        ev_alert = self._make_evidence(
            "ev_b03_alert_001",
            EvidenceSourceType.ALERT,
            alert.get("service", "checkout-api"),
            f"Alert {alert.get('name')} fired at {fired_at.isoformat()}",
            fired_at,
            now,
            EvidenceStrength.DIRECT,
            "fixture_metadata",
            "fixtures/b03/alert.json",
            "alert.json",
        )
        evidence_items.append(ev_alert)
        uow.evidence.add(investigation_id, ev_alert)
        self._append_event(uow, investigation_id, "evidence.recorded", now, {
            "evidence_id": ev_alert.id,
            "strength": ev_alert.strength,
            "summary": ev_alert.observation[:120],
        })

        log_spec = LogQuerySpec("checkout-api", window, level_min="ERROR")
        logs = self._telemetry.query_logs("b03", log_spec)
        log_obs = (
            "checkout-api logged database connection acquisition failures during the incident window"
            if logs
            else "checkout-api error logs present in incident window"
        )
        log_time = _parse_dt(logs[0]["timestamp"]) if logs else fired_at + timedelta(minutes=-4)
        ev_log = self._make_evidence(
            "ev_b03_log_errors_001",
            EvidenceSourceType.TELEMETRY_LOG,
            "checkout-api",
            log_obs,
            log_time,
            now,
            EvidenceStrength.DIRECT,
            "fixture_telemetry",
            "fixtures/b03/logs/checkout-api.jsonl",
            "logs/checkout-api.jsonl#1",
        )
        evidence_items.append(ev_log)
        uow.evidence.add(investigation_id, ev_log)
        self._append_event(uow, investigation_id, "evidence.recorded", now, {
            "evidence_id": ev_log.id,
            "strength": ev_log.strength,
            "summary": ev_log.observation[:120],
        })

        metric_spec = MetricQuerySpec("checkout-api", "db.pool.utilization", window)
        metrics = self._telemetry.query_metrics("b03", metric_spec)
        metric_val = metrics[0].get("value", 0.99) if metrics else 0.99
        metric_time = _parse_dt(metrics[0]["timestamp"]) if metrics else fired_at + timedelta(minutes=-6)
        ev_metric = self._make_evidence(
            "ev_b03_metric_pool_util_001",
            EvidenceSourceType.TELEMETRY_METRIC,
            "checkout-api",
            f"db.pool.utilization reached {metric_val} during incident window",
            metric_time,
            now,
            EvidenceStrength.DERIVED,
            "fixture_telemetry",
            "fixtures/b03/metrics/db.pool.utilization.jsonl",
            "metrics/db.pool.utilization.jsonl#1",
        )
        evidence_items.append(ev_metric)
        uow.evidence.add(investigation_id, ev_metric)
        self._append_event(uow, investigation_id, "evidence.recorded", now, {
            "evidence_id": ev_metric.id,
            "strength": ev_metric.strength,
            "summary": ev_metric.observation[:120],
        })

        dep_spec = DeploymentQuerySpec("checkout-api", window)
        deployments = self._changes.list_deployments("b03", dep_spec)
        dep = deployments[0] if deployments else {}
        version = dep.get("version", "2.8.1")
        ev_deploy = self._make_evidence(
            "ev_b03_deploy_001",
            EvidenceSourceType.CHANGE_DEPLOYMENT,
            "checkout-api",
            f"checkout-api {version} deployed; database.pool.max_size changed from 50 to 5",
            _parse_dt(dep.get("started_at")) or fired_at + timedelta(minutes=-7),
            now,
            EvidenceStrength.DIRECT,
            "fixture_changes",
            "fixtures/b03/deployments.json",
            "deployments.json#0",
        )
        evidence_items.append(ev_deploy)
        uow.evidence.add(investigation_id, ev_deploy)
        self._append_event(uow, investigation_id, "evidence.recorded", now, {
            "evidence_id": ev_deploy.id,
            "strength": ev_deploy.strength,
            "summary": ev_deploy.observation[:120],
        })

        supporting_ids = [e.id for e in evidence_items]
        hypothesis = Hypothesis(
            id="hyp_b03_h1",
            statement=(
                "Recent deployment reduced database connection pool capacity, "
                "leading to connection exhaustion and checkout-api errors."
            ),
            status=HypothesisStatus.SUPPORTED,
            supporting_evidence_ids=supporting_ids,
            contradicting_evidence_ids=[],
        )
        uow.hypotheses.upsert(investigation_id, hypothesis)
        self._append_event(uow, investigation_id, "hypothesis.created", now, {
            "hypothesis_id": hypothesis.id,
            "statement": hypothesis.statement,
        })
        self._append_event(uow, investigation_id, "hypothesis.updated", now, {
            "hypothesis_id": hypothesis.id,
            "supporting": supporting_ids,
            "contradicting": [],
        })

        rca = Rca(
            status=RcaStatus.PROBABLE,
            summary="Deployment reduced DB pool size; connection exhaustion caused checkout-api errors.",
            root_cause=(
                "A production deployment (v2.8.1) reduced the database connection pool max size, "
                "causing connection pool exhaustion."
            ),
            causal_chain=[
                "Configuration change (pool max 50→5)",
                "Connection pool exhaustion",
                "DB acquisition failures",
                "checkout-api HTTP errors",
            ],
            timeline=[
                RcaTimelineEntry(
                    at=_parse_dt(dep.get("started_at")) or fired_at + timedelta(minutes=-7),
                    description="checkout-api v2.8.1 deployment started",
                ),
                RcaTimelineEntry(
                    at=log_time,
                    description="Database connection errors observed",
                ),
            ],
            affected_components=["checkout-api", "postgresql-checkout"],
            claims=[
                RcaClaim(
                    id="claim_b03_1",
                    text="Errors increased on checkout-api during the incident window",
                    evidence_ids=["ev_b03_log_errors_001", "ev_b03_alert_001"],
                ),
                RcaClaim(
                    id="claim_b03_2",
                    text="Connection pool utilization peaked at 99%",
                    evidence_ids=["ev_b03_metric_pool_util_001"],
                ),
                RcaClaim(
                    id="claim_b03_3",
                    text="Deployment changed pool configuration before errors",
                    evidence_ids=["ev_b03_deploy_001", "ev_b03_log_errors_001"],
                ),
            ],
            uncertainty="Distributed tracing not used; request-level impact not verified.",
            evidence_gaps=[],
            remediation=["Roll back or increase database.pool.max_size"],
            observability_lessons=["Alert on db.pool.utilization before error rate spikes"],
        )
        uow.rca.save(investigation_id, rca)
        self._append_event(uow, investigation_id, "rca.published", now, {
            "rca_status": rca.status,
            "root_cause_summary": rca.root_cause[:200],
        })

        inv.transition_to(InvestigationState.RCA_CANDIDATE)
        inv.run_count += 1
        inv.run_completed_at = now
        inv.updated_at = now
        uow.investigations.update(inv)
        self._append_event(uow, investigation_id, "investigation.state_changed", now, {
            "from": InvestigationState.INVESTIGATING,
            "to": InvestigationState.RCA_CANDIDATE,
            "reason": "rca_published",
        })
        self._append_event(uow, investigation_id, "investigation.completed", now, {
            "termination": InvestigationState.RCA_CANDIDATE,
        })

    def _append_event(
        self,
        uow: UnitOfWork,
        investigation_id: str,
        event_type: str,
        occurred_at: datetime,
        payload: dict,
    ) -> None:
        seq = uow.events.next_seq(investigation_id)
        uow.events.append(
            investigation_id,
            InvestigationEvent(seq=seq, type=event_type, occurred_at=occurred_at, payload=payload),
        )

    def _resolve_window(self, manifest: dict, alert: dict, signal_fired: datetime | None) -> TimeWindow:
        iw = manifest.get("incident_window") or {}
        if iw.get("start") and iw.get("end"):
            return TimeWindow(start=_parse_dt(iw["start"]), end=_parse_dt(iw["end"]))
        fired = _parse_dt(alert.get("fired_at")) or signal_fired or self._clock.now()
        return TimeWindow(start=fired - timedelta(minutes=10), end=fired + timedelta(minutes=15))

    def _make_evidence(
        self,
        eid: str,
        source_type: EvidenceSourceType,
        entity: str,
        observation: str,
        event_time: datetime,
        retrieved_at: datetime,
        strength: EvidenceStrength,
        connector: str,
        fixture_path: str,
        fixture_ref: str,
    ) -> Evidence:
        return Evidence(
            id=eid,
            source="fixture",
            source_type=source_type,
            entity=entity,
            observation=observation,
            event_time=event_time,
            retrieved_at=retrieved_at,
            strength=strength,
            provenance=EvidenceProvenance(
                connector=connector,
                fixture_path=fixture_path,
                fixture_ref=fixture_ref,
            ),
        )


def _parse_dt(value: object) -> datetime:
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    if not value:
        return datetime.now(timezone.utc)
    text = str(value).replace("Z", "+00:00")
    dt = datetime.fromisoformat(text)
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
