from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from aveniq_domain.models import InvestigationAggregate

from aveniq_api.openapi_examples import B03_CREATE_REQUEST, B03_INVESTIGATION_AFTER_RUN


class SignalRequest(BaseModel):
    kind: str = Field(
        ...,
        description="How the investigation was triggered",
        examples=["alert"],
        json_schema_extra={"enum": ["alert", "symptom", "manual"]},
    )
    fired_at: datetime | None = Field(
        default=None,
        description="When the signal was observed (ISO-8601 UTC)",
        examples=["2026-09-28T14:36:00Z"],
    )
    service: str | None = Field(
        default=None,
        description="Primary service named in the signal",
        examples=["checkout-api"],
    )
    description: str | None = Field(
        default=None,
        description="Human-readable summary of the signal",
        examples=["checkout-api error rate high"],
    )
    raw: dict[str, Any] | None = Field(
        default=None,
        description="Optional passthrough from an alert webhook",
    )


class CreateInvestigationRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [B03_CREATE_REQUEST],
        }
    )

    benchmark_id: str = Field(
        ...,
        description="Benchmark fixture package to investigate (Slice 1: b03 only)",
        examples=["b03"],
    )
    signal: SignalRequest
    org_id: str | None = Field(default=None, description="Optional tenancy (future)")
    environment_id: str | None = Field(default=None, description="Optional environment (future)")


class TimeWindowResponse(BaseModel):
    start: datetime
    end: datetime


class InvestigationHeaderResponse(BaseModel):
    id: str
    benchmark_id: str
    state: str
    created_at: datetime
    updated_at: datetime
    run_count: int
    org_id: str | None = None
    environment_id: str | None = None
    incident_window: TimeWindowResponse | None = None
    run_completed_at: datetime | None = None
    signal: SignalRequest


class EvidenceProvenanceResponse(BaseModel):
    connector: str | None = None
    fixture_path: str | None = None
    fixture_ref: str | None = None
    query: dict[str, Any] | None = None


class EvidenceResponse(BaseModel):
    id: str
    source: str
    source_type: str
    entity: str
    observation: str
    event_time: datetime
    retrieved_at: datetime
    strength: str
    provenance: EvidenceProvenanceResponse


class HypothesisResponse(BaseModel):
    id: str
    statement: str
    status: str
    supporting_evidence_ids: list[str]
    contradicting_evidence_ids: list[str]


class RcaClaimResponse(BaseModel):
    id: str
    text: str
    evidence_ids: list[str]


class RcaTimelineEntryResponse(BaseModel):
    at: datetime
    description: str


class RcaResponse(BaseModel):
    status: str
    summary: str
    root_cause: str
    contributing_factors: list[str] = Field(default_factory=list)
    causal_chain: list[str] = Field(default_factory=list)
    timeline: list[RcaTimelineEntryResponse] = Field(default_factory=list)
    affected_components: list[str] = Field(default_factory=list)
    claims: list[RcaClaimResponse] = Field(default_factory=list)
    contradicting_evidence_ids: list[str] = Field(default_factory=list)
    uncertainty: str | None = None
    evidence_gaps: list[str] = Field(default_factory=list)
    remediation: list[str] = Field(default_factory=list)
    observability_lessons: list[str] = Field(default_factory=list)


class InvestigationEventResponse(BaseModel):
    seq: int
    type: str
    occurred_at: datetime
    payload: dict[str, Any] = Field(default_factory=dict)


class InvestigationResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [B03_INVESTIGATION_AFTER_RUN],
        }
    )

    investigation: InvestigationHeaderResponse
    events: list[InvestigationEventResponse]
    evidence: list[EvidenceResponse]
    hypotheses: list[HypothesisResponse]
    rca: RcaResponse | None = None


class PlaygroundScenarioSummary(BaseModel):
    scenario_id: str
    benchmark_id: str
    title: str
    description: str


class PlaygroundScenarioListResponse(BaseModel):
    scenarios: list[PlaygroundScenarioSummary]


class PlaygroundRunResponse(BaseModel):
    scenario_id: str
    investigation_id: str
    state: str
    investigation: InvestigationResponse


class HealthResponse(BaseModel):
    status: str = Field(examples=["ok"])
    service: str = Field(examples=["aveniq-api"])
    version: str = Field(examples=["0.1.0"])


class ProblemDetail(BaseModel):
    type: str
    title: str
    status: int
    code: str
    detail: str | None = None
    instance: str | None = None
    errors: list[dict[str, str]] | None = None


def aggregate_to_response(aggregate: InvestigationAggregate) -> InvestigationResponse:
    inv = aggregate.investigation
    iw = None
    if inv.incident_window:
        iw = TimeWindowResponse(start=inv.incident_window.start, end=inv.incident_window.end)
    signal = SignalRequest(
        kind=inv.signal.kind.value,
        fired_at=inv.signal.fired_at,
        service=inv.signal.service,
        description=inv.signal.description,
        raw=inv.signal.raw,
    )
    header = InvestigationHeaderResponse(
        id=inv.id,
        benchmark_id=inv.benchmark_id,
        state=inv.state.value,
        created_at=inv.created_at,
        updated_at=inv.updated_at,
        run_count=inv.run_count,
        org_id=inv.org_id,
        environment_id=inv.environment_id,
        incident_window=iw,
        run_completed_at=inv.run_completed_at,
        signal=signal,
    )
    events = [
        InvestigationEventResponse(
            seq=e.seq,
            type=e.type,
            occurred_at=e.occurred_at,
            payload=e.payload,
        )
        for e in aggregate.events
    ]
    evidence = [
        EvidenceResponse(
            id=e.id,
            source=e.source,
            source_type=e.source_type.value,
            entity=e.entity,
            observation=e.observation,
            event_time=e.event_time,
            retrieved_at=e.retrieved_at,
            strength=e.strength.value,
            provenance=EvidenceProvenanceResponse(**e.provenance.model_dump()),
        )
        for e in aggregate.evidence
    ]
    hypotheses = [
        HypothesisResponse(
            id=h.id,
            statement=h.statement,
            status=h.status.value,
            supporting_evidence_ids=h.supporting_evidence_ids,
            contradicting_evidence_ids=h.contradicting_evidence_ids,
        )
        for h in aggregate.hypotheses
    ]
    rca = None
    if aggregate.rca:
        r = aggregate.rca
        rca = RcaResponse(
            status=r.status.value,
            summary=r.summary,
            root_cause=r.root_cause,
            contributing_factors=r.contributing_factors,
            causal_chain=r.causal_chain,
            timeline=[RcaTimelineEntryResponse(at=t.at, description=t.description) for t in r.timeline],
            affected_components=r.affected_components,
            claims=[RcaClaimResponse(id=c.id, text=c.text, evidence_ids=c.evidence_ids) for c in r.claims],
            contradicting_evidence_ids=r.contradicting_evidence_ids,
            uncertainty=r.uncertainty,
            evidence_gaps=r.evidence_gaps,
            remediation=r.remediation,
            observability_lessons=r.observability_lessons,
        )
    return InvestigationResponse(
        investigation=header,
        events=events,
        evidence=evidence,
        hypotheses=hypotheses,
        rca=rca,
    )
