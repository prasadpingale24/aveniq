from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from typing import Iterator

from aveniq_application.investigator_b03 import DeterministicInvestigatorB03
from aveniq_application.ports import Investigator
from aveniq_application.use_cases import RunInvestigation, StartInvestigation

from aveniq_adapters.clock import SystemClock
from aveniq_adapters.connectors.fixture import (
    FixtureChangePort,
    FixtureMetadataPort,
    FixtureStore,
    FixtureTelemetryPort,
)
from aveniq_adapters.persistence.sqlite import (
    SqliteAggregateReader,
    SqliteUnitOfWork,
    connect,
    migrate,
)
from aveniq_adapters.settings import Settings


class AppServices:
    def __init__(self, settings: Settings, conn: sqlite3.Connection) -> None:
        self.settings = settings
        self.conn = conn
        self.clock = SystemClock()
        self.uow = SqliteUnitOfWork(conn)
        self.aggregate_reader = SqliteAggregateReader(self.uow)
        store = FixtureStore(settings.fixture_root.resolve())
        telemetry = FixtureTelemetryPort(store)
        changes = FixtureChangePort(store)
        metadata = FixtureMetadataPort(store)
        investigator: Investigator | None = None
        if settings.investigation_run_enabled:
            investigator = DeterministicInvestigatorB03(telemetry, changes, metadata, self.clock)
        self.start_investigation = StartInvestigation(self.uow, self.clock)
        self.run_investigation = RunInvestigation(
            self.uow,
            investigator,
            self.clock,
            run_enabled=settings.investigation_run_enabled,
        )


@contextmanager
def session(settings: Settings) -> Iterator[AppServices]:
    migrate(settings.aveniq_sqlite_path)
    conn = connect(settings.aveniq_sqlite_path)
    try:
        yield AppServices(settings, conn)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
