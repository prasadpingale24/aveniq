CREATE TABLE IF NOT EXISTS schema_migrations (
  version INTEGER PRIMARY KEY,
  applied_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS investigations (
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

CREATE INDEX IF NOT EXISTS idx_investigations_benchmark ON investigations(benchmark_id);
CREATE INDEX IF NOT EXISTS idx_investigations_created ON investigations(created_at);

CREATE TABLE IF NOT EXISTS investigation_events (
  investigation_id TEXT NOT NULL,
  seq INTEGER NOT NULL,
  type TEXT NOT NULL,
  occurred_at TEXT NOT NULL,
  payload_json TEXT NOT NULL,
  PRIMARY KEY (investigation_id, seq),
  FOREIGN KEY (investigation_id) REFERENCES investigations(id)
);

CREATE TABLE IF NOT EXISTS evidence (
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

CREATE INDEX IF NOT EXISTS idx_evidence_investigation ON evidence(investigation_id);

CREATE TABLE IF NOT EXISTS hypotheses (
  id TEXT NOT NULL,
  investigation_id TEXT NOT NULL,
  statement TEXT NOT NULL,
  status TEXT NOT NULL,
  supporting_json TEXT NOT NULL,
  contradicting_json TEXT NOT NULL,
  PRIMARY KEY (id, investigation_id),
  FOREIGN KEY (investigation_id) REFERENCES investigations(id)
);

CREATE TABLE IF NOT EXISTS rca (
  investigation_id TEXT PRIMARY KEY,
  document_json TEXT NOT NULL,
  FOREIGN KEY (investigation_id) REFERENCES investigations(id)
);
