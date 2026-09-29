# ADR-013 — Fixture package format v1

| | |
|---|---|
| **Status** | Accepted |
| **Date** | 2026-09-28 |

## Context

Product ADR-010 requires synthetic benchmarks before real integrations. B03 is the implementation spine.

## Decision

- On-disk layout `fixtures/{benchmark_id}/` version **1.0** per [01-fixture-package-spec-v1.md](../01-fixture-package-spec-v1.md)
- Scenarios authored in `scenarios/` and built by `scripts/build_fixture.py`
- `ground_truth.json` is **eval-only**; runtime connectors use a filename whitelist

## Alternatives considered

| Option | Rejected because |
|--------|------------------|
| Hand-only fixtures | Hard to reproduce B09/B10 variants |
| Embed ground truth in manifest | Risk of leaking into investigator context |

## Consequences

- Connectors mirror future query specs (time window, service)
- Version bumps require ADR-013 supersede or `fixture_package_version` migration

## References

- [hld/04-data-flows.md](../hld/04-data-flows.md)
- [docs/21-benchmark-incidents.md](../../docs/21-benchmark-incidents.md)
