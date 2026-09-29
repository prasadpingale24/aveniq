from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from aveniq_domain.enums import (
    EvidenceSourceType,
    EvidenceStrength,
    HypothesisStatus,
    InvestigationState,
    RcaStatus,
    SignalKind,
)
from aveniq_domain.models import (
    Evidence,
    EvidenceProvenance,
    Hypothesis,
    Investigation,
    InvestigationAggregate,
    InvestigationEvent,
    Rca,
    RcaClaim,
    RcaTimelineEntry,
    Signal,
    TimeWindow,
)

from aveniq_application.ports import UnitOfWork


def _dt_to_str(dt: datetime) -> str:
    return dt.isoformat()


def _str_to_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value)


class SqliteUnitOfWork(UnitOfWork):
    def __init__(self, conn: sqlite3.Connection) -> None:
        self._conn = conn
        self.investigations = SqliteInvestigationRepository(conn)
        self.events = SqliteEventRepository(conn)
        self.evidence = SqliteEvidenceRepository(conn)
        self.hypotheses = SqliteHypothesisRepository(conn)
        self.rca = SqliteRcaRepository(conn)

    def commit(self) -> None:
        self._conn.commit()

    def rollback(self) -> None:
        self._conn.rollback()


def migrate(db_path: Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    migration_file = Path(__file__).parent / "migrations" / "001_initial.sql"
    sql = migration_file.read_text(encoding="utf-8")
    conn = sqlite3.connect(db_path)
    try:
        conn.executescript(sql)
        row = conn.execute("SELECT version FROM schema_migrations WHERE version = 1").fetchone()
        if row is None:
            conn.execute(
                "INSERT INTO schema_migrations (version, applied_at) VALUES (1, ?)",
                (_dt_to_str(datetime.now(timezone.utc)),),
            )
            conn.commit()
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        conn.commit()
    finally:
        conn.close()


def connect(db_path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


class SqliteInvestigationRepository:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self._conn = conn

    def create(self, investigation: Investigation) -> None:
        iw = investigation.incident_window
        self._conn.execute(
            """
            INSERT INTO investigations (
              id, benchmark_id, state, created_at, updated_at, org_id, environment_id,
              incident_window_start, incident_window_end, run_completed_at, run_count, signal_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                investigation.id,
                investigation.benchmark_id,
                investigation.state,
                _dt_to_str(investigation.created_at),
                _dt_to_str(investigation.updated_at),
                investigation.org_id,
                investigation.environment_id,
                _dt_to_str(iw.start) if iw else None,
                _dt_to_str(iw.end) if iw else None,
                _dt_to_str(investigation.run_completed_at) if investigation.run_completed_at else None,
                investigation.run_count,
                json.dumps(investigation.signal.model_dump(mode="json")),
            ),
        )

    def get(self, investigation_id: str) -> Investigation | None:
        row = self._conn.execute(
            "SELECT * FROM investigations WHERE id = ?", (investigation_id,)
        ).fetchone()
        if row is None:
            return None
        signal_data = json.loads(row["signal_json"])
        signal = Signal(
            kind=SignalKind(signal_data["kind"]),
            fired_at=_str_to_dt(signal_data.get("fired_at")),
            service=signal_data.get("service"),
            description=signal_data.get("description"),
            raw=signal_data.get("raw"),
        )
        iw = None
        if row["incident_window_start"] and row["incident_window_end"]:
            iw = TimeWindow(
                start=_str_to_dt(row["incident_window_start"]),
                end=_str_to_dt(row["incident_window_end"]),
            )
        return Investigation(
            id=row["id"],
            benchmark_id=row["benchmark_id"],
            state=InvestigationState(row["state"]),
            created_at=_str_to_dt(row["created_at"]),
            updated_at=_str_to_dt(row["updated_at"]),
            org_id=row["org_id"],
            environment_id=row["environment_id"],
            incident_window=iw,
            run_completed_at=_str_to_dt(row["run_completed_at"]),
            run_count=row["run_count"],
            signal=signal,
        )

    def update(self, investigation: Investigation) -> None:
        iw = investigation.incident_window
        self._conn.execute(
            """
            UPDATE investigations SET
              state = ?, updated_at = ?, incident_window_start = ?, incident_window_end = ?,
              run_completed_at = ?, run_count = ?
            WHERE id = ?
            """,
            (
                investigation.state,
                _dt_to_str(investigation.updated_at),
                _dt_to_str(iw.start) if iw else None,
                _dt_to_str(iw.end) if iw else None,
                _dt_to_str(investigation.run_completed_at) if investigation.run_completed_at else None,
                investigation.run_count,
                investigation.id,
            ),
        )


class SqliteEventRepository:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self._conn = conn

    def next_seq(self, investigation_id: str) -> int:
        row = self._conn.execute(
            "SELECT COALESCE(MAX(seq), 0) + 1 AS n FROM investigation_events WHERE investigation_id = ?",
            (investigation_id,),
        ).fetchone()
        return int(row["n"])

    def append(self, investigation_id: str, event: InvestigationEvent) -> InvestigationEvent:
        seq = event.seq if event.seq else self.next_seq(investigation_id)
        stored = InvestigationEvent(
            seq=seq,
            type=event.type,
            occurred_at=event.occurred_at,
            payload=event.payload,
        )
        self._conn.execute(
            """
            INSERT INTO investigation_events (investigation_id, seq, type, occurred_at, payload_json)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                investigation_id,
                stored.seq,
                stored.type,
                _dt_to_str(stored.occurred_at),
                json.dumps(stored.payload),
            ),
        )
        return stored

    def list_for(self, investigation_id: str) -> list[InvestigationEvent]:
        rows = self._conn.execute(
            "SELECT * FROM investigation_events WHERE investigation_id = ? ORDER BY seq",
            (investigation_id,),
        ).fetchall()
        return [
            InvestigationEvent(
                seq=row["seq"],
                type=row["type"],
                occurred_at=_str_to_dt(row["occurred_at"]),
                payload=json.loads(row["payload_json"]),
            )
            for row in rows
        ]


class SqliteEvidenceRepository:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self._conn = conn

    def add(self, investigation_id: str, evidence: Evidence) -> None:
        self._conn.execute(
            """
            INSERT INTO evidence (
              id, investigation_id, source, source_type, entity, observation,
              event_time, retrieved_at, strength, provenance_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                evidence.id,
                investigation_id,
                evidence.source,
                evidence.source_type,
                evidence.entity,
                evidence.observation,
                _dt_to_str(evidence.event_time),
                _dt_to_str(evidence.retrieved_at),
                evidence.strength,
                json.dumps(evidence.provenance.model_dump(mode="json")),
            ),
        )

    def list_for(self, investigation_id: str) -> list[Evidence]:
        rows = self._conn.execute(
            "SELECT * FROM evidence WHERE investigation_id = ? ORDER BY event_time",
            (investigation_id,),
        ).fetchall()
        result: list[Evidence] = []
        for row in rows:
            prov = json.loads(row["provenance_json"])
            result.append(
                Evidence(
                    id=row["id"],
                    source=row["source"],
                    source_type=EvidenceSourceType(row["source_type"]),
                    entity=row["entity"],
                    observation=row["observation"],
                    event_time=_str_to_dt(row["event_time"]),
                    retrieved_at=_str_to_dt(row["retrieved_at"]),
                    strength=EvidenceStrength(row["strength"]),
                    provenance=EvidenceProvenance(**prov),
                )
            )
        return result


class SqliteHypothesisRepository:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self._conn = conn

    def upsert(self, investigation_id: str, hypothesis: Hypothesis) -> None:
        self._conn.execute(
            """
            INSERT OR REPLACE INTO hypotheses (
              id, investigation_id, statement, status, supporting_json, contradicting_json
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                hypothesis.id,
                investigation_id,
                hypothesis.statement,
                hypothesis.status,
                json.dumps(hypothesis.supporting_evidence_ids),
                json.dumps(hypothesis.contradicting_evidence_ids),
            ),
        )

    def list_for(self, investigation_id: str) -> list[Hypothesis]:
        rows = self._conn.execute(
            "SELECT * FROM hypotheses WHERE investigation_id = ?", (investigation_id,)
        ).fetchall()
        return [
            Hypothesis(
                id=row["id"],
                statement=row["statement"],
                status=HypothesisStatus(row["status"]),
                supporting_evidence_ids=json.loads(row["supporting_json"]),
                contradicting_evidence_ids=json.loads(row["contradicting_json"]),
            )
            for row in rows
        ]


class SqliteRcaRepository:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self._conn = conn

    def save(self, investigation_id: str, rca: Rca) -> None:
        self._conn.execute(
            """
            INSERT OR REPLACE INTO rca (investigation_id, document_json) VALUES (?, ?)
            """,
            (investigation_id, json.dumps(rca.model_dump(mode="json"))),
        )

    def get(self, investigation_id: str) -> Rca | None:
        row = self._conn.execute(
            "SELECT document_json FROM rca WHERE investigation_id = ?", (investigation_id,)
        ).fetchone()
        if row is None:
            return None
        data = json.loads(row["document_json"])
        return Rca(
            status=RcaStatus(data["status"]),
            summary=data["summary"],
            root_cause=data["root_cause"],
            contributing_factors=data.get("contributing_factors", []),
            causal_chain=data.get("causal_chain", []),
            timeline=[RcaTimelineEntry(**t) for t in data.get("timeline", [])],
            affected_components=data.get("affected_components", []),
            claims=[RcaClaim(**c) for c in data.get("claims", [])],
            contradicting_evidence_ids=data.get("contradicting_evidence_ids", []),
            uncertainty=data.get("uncertainty"),
            evidence_gaps=data.get("evidence_gaps", []),
            remediation=data.get("remediation", []),
            observability_lessons=data.get("observability_lessons", []),
        )


class SqliteAggregateReader:
    def __init__(self, uow: SqliteUnitOfWork) -> None:
        self._uow = uow

    def load_aggregate(self, investigation_id: str) -> InvestigationAggregate | None:
        inv = self._uow.investigations.get(investigation_id)
        if inv is None:
            return None
        return InvestigationAggregate(
            investigation=inv,
            events=self._uow.events.list_for(investigation_id),
            evidence=self._uow.evidence.list_for(investigation_id),
            hypotheses=self._uow.hypotheses.list_for(investigation_id),
            rca=self._uow.rca.get(investigation_id),
        )
