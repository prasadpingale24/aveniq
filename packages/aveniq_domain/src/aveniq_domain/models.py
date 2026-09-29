from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from aveniq_domain.enums import (
    EvidenceSourceType,
    EvidenceStrength,
    HypothesisStatus,
    InvestigationState,
    RcaStatus,
    SignalKind,
    TERMINAL_STATES,
)
from aveniq_domain.exceptions import InvalidStateTransitionError


class TimeWindow(BaseModel):
    start: datetime
    end: datetime


class Signal(BaseModel):
    kind: SignalKind
    fired_at: datetime | None = None
    service: str | None = None
    description: str | None = None
    raw: dict[str, Any] | None = None


class Investigation(BaseModel):
    id: str
    benchmark_id: str
    state: InvestigationState = InvestigationState.INITIALIZED
    created_at: datetime
    updated_at: datetime
    org_id: str | None = None
    environment_id: str | None = None
    incident_window: TimeWindow | None = None
    run_completed_at: datetime | None = None
    run_count: int = 0
    signal: Signal

    def transition_to(self, new_state: InvestigationState) -> None:
        allowed = _ALLOWED_TRANSITIONS.get(self.state, frozenset())
        if new_state not in allowed and new_state != self.state:
            raise InvalidStateTransitionError(self.state, new_state)
        self.state = new_state

    @property
    def is_terminal(self) -> bool:
        return self.state in TERMINAL_STATES


_ALLOWED_TRANSITIONS: dict[InvestigationState, frozenset[InvestigationState]] = {
    InvestigationState.INITIALIZED: frozenset(
        {InvestigationState.CONTEXT_GATHERING, InvestigationState.INVESTIGATING}
    ),
    InvestigationState.CONTEXT_GATHERING: frozenset({InvestigationState.INVESTIGATING}),
    InvestigationState.INVESTIGATING: frozenset(
        {
            InvestigationState.RCA_CANDIDATE,
            InvestigationState.INCONCLUSIVE,
            InvestigationState.BLOCKED,
        }
    ),
    InvestigationState.RCA_CANDIDATE: frozenset(),
    InvestigationState.INCONCLUSIVE: frozenset(),
    InvestigationState.BLOCKED: frozenset(),
}


class EvidenceProvenance(BaseModel):
    connector: str | None = None
    fixture_path: str | None = None
    fixture_ref: str | None = None
    query: dict[str, Any] | None = None


class Evidence(BaseModel):
    id: str
    source: str
    source_type: EvidenceSourceType
    entity: str
    observation: str
    event_time: datetime
    retrieved_at: datetime
    strength: EvidenceStrength
    provenance: EvidenceProvenance


class Hypothesis(BaseModel):
    id: str
    statement: str
    status: HypothesisStatus
    supporting_evidence_ids: list[str] = Field(default_factory=list)
    contradicting_evidence_ids: list[str] = Field(default_factory=list)


class RcaClaim(BaseModel):
    id: str
    text: str
    evidence_ids: list[str]


class RcaTimelineEntry(BaseModel):
    at: datetime
    description: str


class Rca(BaseModel):
    status: RcaStatus
    summary: str
    root_cause: str
    contributing_factors: list[str] = Field(default_factory=list)
    causal_chain: list[str] = Field(default_factory=list)
    timeline: list[RcaTimelineEntry] = Field(default_factory=list)
    affected_components: list[str] = Field(default_factory=list)
    claims: list[RcaClaim] = Field(default_factory=list)
    contradicting_evidence_ids: list[str] = Field(default_factory=list)
    uncertainty: str | None = None
    evidence_gaps: list[str] = Field(default_factory=list)
    remediation: list[str] = Field(default_factory=list)
    observability_lessons: list[str] = Field(default_factory=list)


class InvestigationEvent(BaseModel):
    seq: int
    type: str
    occurred_at: datetime
    payload: dict[str, Any] = Field(default_factory=dict)


class InvestigationAggregate(BaseModel):
    investigation: Investigation
    events: list[InvestigationEvent] = Field(default_factory=list)
    evidence: list[Evidence] = Field(default_factory=list)
    hypotheses: list[Hypothesis] = Field(default_factory=list)
    rca: Rca | None = None
