# LLD 04 — Persistence (SQLite)

**ADR:** [adrs/012-sqlite-persistence.md](../adrs/012-sqlite-persistence.md)

## Connection

- Driver: `sqlite3` stdlib or `aiosqlite` if async API later (Phase 0b: **sync**).
- Path: `AVENIQ_SQLITE_PATH`
- PRAGMAs on connect: `journal_mode=WAL`, `foreign_keys=ON`

## Schema version

Table `schema_migrations`:

| version | applied_at |
|---------|------------|
| 1 | ISO datetime |

Migration file: `aveniq_adapters/persistence/migrations/001_initial.sql`

## DDL v1

```sql
CREATE TABLE investigations (
  id TEXT PRIMARY KEY,
  benchmark_id TEXT NOT NULL,
  state TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  org_id TEXT,
  environment_id TEXT,
  incident_window_start TEXT,
  incident_window_end TEXT,
  run_completed_at TEXT,
  run_count INTEGER NOT NULL DEFAULT 0,
  signal_json TEXT NOT NULL
);

CREATE INDEX idx_investigations_benchmark ON investigations(benchmark_id);
CREATE INDEX idx_investigations_created ON investigations(created_at);

CREATE TABLE investigation_events (
  investigation_id TEXT NOT NULL,
  seq INTEGER NOT NULL,
  type TEXT NOT NULL,
  occurred_at TEXT NOT NULL,
  payload_json TEXT NOT NULL,
  PRIMARY KEY (investigation_id, seq),
  FOREIGN KEY (investigation_id) REFERENCES investigations(id)
);

CREATE TABLE evidence (
  id TEXT NOT NULL,
  investigation_id TEXT NOT NULL,
  source TEXT NOT NULL,
  source_type TEXT NOT NULL,
  entity TEXT NOT NULL,
  observation TEXT NOT NULL,
  event_time TEXT NOT NULL,
  retrieved_at TEXT NOT NULL,
  strength TEXT NOT NULL,
  provenance_json TEXT NOT NULL,
  PRIMARY KEY (id, investigation_id),
  FOREIGN KEY (investigation_id) REFERENCES investigations(id)
);

CREATE INDEX idx_evidence_investigation ON evidence(investigation_id);

CREATE TABLE hypotheses (
  id TEXT NOT NULL,
  investigation_id TEXT NOT NULL,
  statement TEXT NOT NULL,
  status TEXT NOT NULL,
  supporting_json TEXT NOT NULL,
  contradicting_json TEXT NOT NULL,
  PRIMARY KEY (id, investigation_id),
  FOREIGN KEY (investigation_id) REFERENCES investigations(id)
);

CREATE TABLE rca (
  investigation_id TEXT PRIMARY KEY,
  document_json TEXT NOT NULL,
  FOREIGN KEY (investigation_id) REFERENCES investigations(id)
);
```

`document_json` stores serialized `Rca` model (JSON).

## Repository methods → SQL

| Method | SQL pattern |
|--------|-------------|
| `create` | INSERT investigations |
| `append event` | SELECT MAX(seq)+1; INSERT investigation_events |
| `add evidence` | INSERT evidence |
| `upsert hypothesis` | INSERT OR REPLACE hypotheses |
| `save rca` | INSERT OR REPLACE rca |
| `load_aggregate` | JOIN queries or multiple SELECTs in one transaction |

## Aggregate load order

1. investigations row  
2. investigation_events ORDER BY seq  
3. evidence  
4. hypotheses  
5. rca (optional)

## Backup (VPS)

Document for operators: copy SQLite file while process stopped or use SQLite backup API (future).

## Cross-references

- Domain: [01-domain-model.md](01-domain-model.md)
- Environments: [../05-local-vs-staging.md](../05-local-vs-staging.md)
