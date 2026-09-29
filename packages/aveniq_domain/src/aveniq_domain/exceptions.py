class DomainError(Exception):
    """Base domain error."""


class InvalidStateTransitionError(DomainError):
    def __init__(self, from_state: str, to_state: str) -> None:
        self.from_state = from_state
        self.to_state = to_state
        super().__init__(f"Invalid transition {from_state} -> {to_state}")


class InvestigationNotFoundError(DomainError):
    def __init__(self, investigation_id: str) -> None:
        self.investigation_id = investigation_id
        super().__init__(f"Investigation {investigation_id} not found")


class InvestigationAlreadyRunError(DomainError):
    def __init__(self, investigation_id: str) -> None:
        self.investigation_id = investigation_id
        super().__init__(f"Investigation {investigation_id} already completed")


class UnsupportedBenchmarkError(DomainError):
    def __init__(self, benchmark_id: str) -> None:
        self.benchmark_id = benchmark_id
        super().__init__(f"Benchmark {benchmark_id} is not supported")


class RunNotImplementedError(DomainError):
    """Slice 0 stub when run is disabled."""
