# ADR-014 — Deterministic investigator v1 (B03)

| | |
|---|---|
| **Status** | Accepted |
| **Date** | 2026-09-28 |

## Context

Product ADR-004 treats agentic investigation as experimental. Phase 0b–1 must be testable without LLM flake.

## Decision

- Implement `Investigator` port with `DeterministicInvestigatorB03` fixed playbook
- Stable evidence ids `ev_b03_*` for golden tests
- LLM investigator is a future adapter behind the same port

## Alternatives considered

| Option | When |
|--------|------|
| LLM from day one | Rejected for Slice 1 — breaks determinism and eval baselines |
| Rules engine DSL | Deferred — Python playbook sufficient for one benchmark |

## Consequences

- Experiment 02 (agentic vs deterministic) can compare later by swapping investigator
- Additional benchmarks add playbooks or a planner in Phase 2

## References

- [lld/06-deterministic-investigator-b03.md](../lld/06-deterministic-investigator-b03.md)
- [docs/22-experiments.md](../../docs/22-experiments.md)
