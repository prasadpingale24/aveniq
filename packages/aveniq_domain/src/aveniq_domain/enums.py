from enum import StrEnum


class InvestigationState(StrEnum):
    INITIALIZED = "initialized"
    CONTEXT_GATHERING = "context_gathering"
    INVESTIGATING = "investigating"
    RCA_CANDIDATE = "rca_candidate"
    INCONCLUSIVE = "inconclusive"
    BLOCKED = "blocked"


class EvidenceStrength(StrEnum):
    DIRECT = "direct"
    DERIVED = "derived"
    CORRELATED = "correlated"
    INFERRED = "inferred"
    HUMAN_PROVIDED = "human_provided"


class EvidenceSourceType(StrEnum):
    TELEMETRY_LOG = "telemetry_log"
    TELEMETRY_METRIC = "telemetry_metric"
    TELEMETRY_TRACE = "telemetry_trace"
    CHANGE_DEPLOYMENT = "change_deployment"
    CONTEXT_SERVICE = "context_service"
    ALERT = "alert"
    HUMAN = "human"


class HypothesisStatus(StrEnum):
    PROPOSED = "proposed"
    SUPPORTED = "supported"
    WEAKENED = "weakened"
    REJECTED = "rejected"


class RcaStatus(StrEnum):
    CONFIRMED = "confirmed"
    PROBABLE = "probable"
    POSSIBLE = "possible"
    INCONCLUSIVE = "inconclusive"


class SignalKind(StrEnum):
    ALERT = "alert"
    SYMPTOM = "symptom"
    MANUAL = "manual"


TERMINAL_STATES = frozenset(
    {
        InvestigationState.RCA_CANDIDATE,
        InvestigationState.INCONCLUSIVE,
        InvestigationState.BLOCKED,
    }
)
