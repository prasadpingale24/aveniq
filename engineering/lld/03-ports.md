# LLD 03 — Ports (application interfaces)

Python 3.12 `typing.Protocol` in `aveniq_application.ports`.

## Clock

```python
class Clock(Protocol):
    def now(self) -> datetime: ...
```

## InvestigationRepository

```python
class InvestigationRepository(Protocol):
    def create(self, investigation: Investigation) -> None: ...
    def get(self, investigation_id: str) -> Investigation | None: ...
    def update(self, investigation: Investigation) -> None: ...
```

## InvestigationEventRepository

```python
class InvestigationEventRepository(Protocol):
    def append(self, investigation_id: str, event: InvestigationEvent) -> InvestigationEvent: ...
    def list_for(self, investigation_id: str) -> list[InvestigationEvent]: ...
    def next_seq(self, investigation_id: str) -> int: ...
```

## EvidenceRepository

```python
class EvidenceRepository(Protocol):
    def add(self, evidence: Evidence) -> None: ...
    def list_for(self, investigation_id: str) -> list[Evidence]: ...
    def get(self, investigation_id: str, evidence_id: str) -> Evidence | None: ...
```

## HypothesisRepository

```python
class HypothesisRepository(Protocol):
    def upsert(self, hypothesis: Hypothesis) -> None: ...
    def list_for(self, investigation_id: str) -> list[Hypothesis]: ...
```

## RcaRepository

```python
class RcaRepository(Protocol):
    def save(self, investigation_id: str, rca: Rca) -> None: ...
    def get(self, investigation_id: str) -> Rca | None: ...
```

## AggregateReader

```python
class AggregateReader(Protocol):
    def load_aggregate(self, investigation_id: str) -> InvestigationAggregate | None: ...
```

## Investigator

```python
class Investigator(Protocol):
    def run(
        self,
        investigation: Investigation,
        uow: UnitOfWork,
        telemetry: TelemetryPort,
        changes: ChangePort,
        metadata: MetadataPort,
        clock: Clock,
    ) -> None: ...
```

## TelemetryPort

```python
@dataclass(frozen=True)
class LogQuerySpec:
    service: str
    window: TimeWindow
    level_min: str | None = None

@dataclass(frozen=True)
class MetricQuerySpec:
    service: str
    metric_name: str
    window: TimeWindow

class TelemetryPort(Protocol):
    def query_logs(self, benchmark_id: str, spec: LogQuerySpec) -> list[dict]: ...
    def query_metrics(self, benchmark_id: str, spec: MetricQuerySpec) -> list[dict]: ...
```

## ChangePort

```python
@dataclass(frozen=True)
class DeploymentQuerySpec:
    service: str
    window: TimeWindow

class ChangePort(Protocol):
    def list_deployments(self, benchmark_id: str, spec: DeploymentQuerySpec) -> list[dict]: ...
```

## MetadataPort

```python
class MetadataPort(Protocol):
    def get_services(self, benchmark_id: str) -> list[dict]: ...
    def get_alert(self, benchmark_id: str) -> dict: ...
```

## Connector errors

Raise `ConnectorError` with `code: ConnectorErrorCode`:

`fixture_not_found` | `fixture_invalid` | `query_out_of_window` | `io_error`

Mapped to HTTP 500 or investigation `blocked` per investigator policy.

## Cross-references

- Fixture impl: [05-fixture-connectors.md](05-fixture-connectors.md)
