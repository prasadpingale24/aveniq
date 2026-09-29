from datetime import datetime, timezone

from aveniq_domain.enums import InvestigationState, SignalKind
from aveniq_domain.models import Investigation, InvestigationEvent, Signal

from aveniq_adapters.persistence.sqlite import SqliteUnitOfWork, connect, migrate


def test_sqlite_repository_roundtrip(tmp_path):
    db_path = tmp_path / "aveniq.db"
    migrate(db_path)
    conn = connect(db_path)
    uow = SqliteUnitOfWork(conn)
    now = datetime(2026, 9, 28, 15, 0, 0, tzinfo=timezone.utc)
    inv = Investigation(
        id="test-inv-1",
        benchmark_id="b03",
        state=InvestigationState.INITIALIZED,
        created_at=now,
        updated_at=now,
        signal=Signal(kind=SignalKind.ALERT, service="checkout-api"),
    )
    uow.investigations.create(inv)
    uow.events.append(
        "test-inv-1",
        InvestigationEvent(seq=1, type="investigation.created", occurred_at=now, payload={}),
    )
    uow.commit()

    loaded = uow.investigations.get("test-inv-1")
    assert loaded is not None
    assert loaded.benchmark_id == "b03"
    events = uow.events.list_for("test-inv-1")
    assert len(events) == 1
    conn.close()
