from datetime import datetime, timezone

from aveniq_adapters.persistence.event_storage import event_from_storage_row, event_to_storage_json
from aveniq_domain.enums import ActorKind
from aveniq_domain.models import Actor, InvestigationEvent


def test_event_round_trip_with_actor() -> None:
    now = datetime(2026, 1, 1, tzinfo=timezone.utc)
    event = InvestigationEvent(
        seq=1,
        type="investigation.created",
        occurred_at=now,
        payload={"benchmark_id": "b03"},
        actor=Actor(kind=ActorKind.ANONYMOUS, id="local"),
    )
    raw = event_to_storage_json(event)
    restored = event_from_storage_row(1, event.type, now.isoformat(), raw, lambda s: now)
    assert restored.payload == event.payload
    assert restored.actor is not None
    assert restored.actor.id == "local"


def test_event_legacy_flat_payload() -> None:
    now = datetime(2026, 1, 1, tzinfo=timezone.utc)
    raw = '{"benchmark_id": "b03"}'
    restored = event_from_storage_row(1, "investigation.created", now.isoformat(), raw, lambda s: now)
    assert restored.payload["benchmark_id"] == "b03"
    assert restored.actor is None
