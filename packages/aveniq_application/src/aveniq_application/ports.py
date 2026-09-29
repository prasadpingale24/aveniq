from __future__ import annotations

from datetime import datetime
from typing import Protocol

from aveniq_domain.models import (
    Evidence,
    Hypothesis,
    Investigation,
    InvestigationAggregate,
    InvestigationEvent,
    Rca,
    TimeWindow,
)


class Clock(Protocol):
    def now(self) -> datetime: ...


class InvestigationEventRepository(Protocol):
    def append(self, investigation_id: str, event: InvestigationEvent) -> InvestigationEvent: ...
    def list_for(self, investigation_id: str) -> list[InvestigationEvent]: ...
    def next_seq(self, investigation_id: str) -> int: ...


class InvestigationRepository(Protocol):
    def create(self, investigation: Investigation) -> None: ...
    def get(self, investigation_id: str) -> Investigation | None: ...
    def update(self, investigation: Investigation) -> None: ...


class EvidenceRepository(Protocol):
    def add(self, investigation_id: str, evidence: Evidence) -> None: ...
    def list_for(self, investigation_id: str) -> list[Evidence]: ...


class HypothesisRepository(Protocol):
    def upsert(self, investigation_id: str, hypothesis: Hypothesis) -> None: ...
    def list_for(self, investigation_id: str) -> list[Hypothesis]: ...


class RcaRepository(Protocol):
    def save(self, investigation_id: str, rca: Rca) -> None: ...
    def get(self, investigation_id: str) -> Rca | None: ...


class AggregateReader(Protocol):
    def load_aggregate(self, investigation_id: str) -> InvestigationAggregate | None: ...


class UnitOfWork(Protocol):
    investigations: InvestigationRepository
    events: InvestigationEventRepository
    evidence: EvidenceRepository
    hypotheses: HypothesisRepository
    rca: RcaRepository

    def commit(self) -> None: ...
    def rollback(self) -> None: ...


class LogQuerySpec:
    def __init__(
        self,
        service: str,
        window: TimeWindow,
        level_min: str | None = None,
    ) -> None:
        self.service = service
        self.window = window
        self.level_min = level_min


class MetricQuerySpec:
    def __init__(self, service: str, metric_name: str, window: TimeWindow) -> None:
        self.service = service
        self.metric_name = metric_name
        self.window = window


class DeploymentQuerySpec:
    def __init__(self, service: str, window: TimeWindow) -> None:
        self.service = service
        self.window = window


class TelemetryPort(Protocol):
    def query_logs(self, benchmark_id: str, spec: LogQuerySpec) -> list[dict]: ...
    def query_metrics(self, benchmark_id: str, spec: MetricQuerySpec) -> list[dict]: ...


class ChangePort(Protocol):
    def list_deployments(self, benchmark_id: str, spec: DeploymentQuerySpec) -> list[dict]: ...


class MetadataPort(Protocol):
    def get_alert(self, benchmark_id: str) -> dict: ...
    def get_manifest(self, benchmark_id: str) -> dict: ...
    def get_services(self, benchmark_id: str) -> list[dict]: ...


class Investigator(Protocol):
    def run(self, investigation_id: str, uow: UnitOfWork) -> None: ...
