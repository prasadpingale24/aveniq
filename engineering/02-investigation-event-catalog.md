# 02 — Investigation event catalog

Append-only events stored in `investigation_events` (see [lld/04-persistence.md](lld/04-persistence.md)).  
`seq` is monotonic per investigation starting at 1.

## Event envelope (stored payload)

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Catalog id below |
| `occurred_at` | ISO-8601 UTC | Event time (usually clock.now at write) |
| `payload` | object | Type-specific body |
| `correlation` | object? | Optional: `step_id`, `question_id` |

Wire format for events inside `InvestigationResponse` mirrors this (OpenAPI `InvestigationEvent`).

## Catalog

| type | Emitted when | Payload keys |
|------|----------------|--------------|
| `investigation.created` | Investigation persisted | `benchmark_id`, `signal` |
| `investigation.state_changed` | State transition | `from`, `to`, `reason` |
| `investigation.question_raised` | Investigator articulates question | `question_id`, `text`, `category` |
| `investigation.action_selected` | Tool/query chosen | `action_id`, `tool`, `query_summary` |
| `connector.query_started` | Before external read | `connector`, `query_spec` |
| `connector.query_completed` | After external read | `connector`, `record_count`, `duration_ms` |
| `connector.query_failed` | Connector error | `connector`, `error_code`, `message` |
| `evidence.recorded` | Evidence entity persisted | `evidence_id`, `strength`, `summary` |
| `observation.recorded` | Derived observation text | `observation`, `evidence_ids` |
| `hypothesis.created` | New hypothesis | `hypothesis_id`, `statement` |
| `hypothesis.updated` | Support/contradict links | `hypothesis_id`, `supporting`, `contradicting` |
| `rca.published` | RCA written | `rca_status`, `root_cause_summary` |
| `investigation.completed` | Terminal run success | `termination` (`rca_candidate` \| `inconclusive` \| `blocked`) |
| `investigation.run_rejected` | Run refused (e.g. already run) | `reason` |

## B03 playbook mapping

| Playbook step | Events (minimum) |
|---------------|------------------|
| Initialize window from alert | `investigation.question_raised`, `investigation.action_selected` |
| Query logs | `connector.query_*`, `evidence.recorded` |
| Query metrics | `connector.query_*`, `evidence.recorded` |
| Query deployments | `connector.query_*`, `evidence.recorded` |
| Form H1 | `hypothesis.created`, `hypothesis.updated` |
| Publish RCA | `rca.published`, `investigation.state_changed`, `investigation.completed` |

Full step list: [lld/06-deterministic-investigator-b03.md](lld/06-deterministic-investigator-b03.md).

## Cross-references

- Product investigation record: [docs/09-investigation-model.md](../docs/09-investigation-model.md) §13
- OpenAPI: [api/openapi.yaml](api/openapi.yaml) `InvestigationEvent`
