import pytest

from aveniq_domain.enums import InvestigationState
from aveniq_domain.exceptions import InvalidStateTransitionError
from aveniq_domain.models import Investigation
from aveniq_domain.enums import SignalKind
from aveniq_domain.models import Signal
from datetime import datetime, timezone


def _inv() -> Investigation:
    now = datetime.now(timezone.utc)
    return Investigation(
        id="x",
        benchmark_id="b03",
        state=InvestigationState.INITIALIZED,
        created_at=now,
        updated_at=now,
        signal=Signal(kind=SignalKind.ALERT),
    )


def test_valid_transition_to_rca_candidate():
    inv = _inv()
    inv.transition_to(InvestigationState.CONTEXT_GATHERING)
    inv.transition_to(InvestigationState.INVESTIGATING)
    inv.transition_to(InvestigationState.RCA_CANDIDATE)
    assert inv.state == InvestigationState.RCA_CANDIDATE


def test_invalid_transition_from_terminal():
    inv = _inv()
    inv.state = InvestigationState.RCA_CANDIDATE
    with pytest.raises(InvalidStateTransitionError):
        inv.transition_to(InvestigationState.INVESTIGATING)
