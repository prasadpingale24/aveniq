from __future__ import annotations

from dataclasses import dataclass

from aveniq_domain.enums import InvestigationState
from aveniq_domain.exceptions import (
    InvestigationAlreadyRunError,
    InvestigationNotFoundError,
    RunNotImplementedError,
    UnsupportedBenchmarkError,
)
from aveniq_domain.models import Actor, Investigation, InvestigationAggregate, InvestigationEvent, Signal

from aveniq_application.actor import ACTOR_ANONYMOUS_LOCAL
from aveniq_application.ids import new_ulid
from aveniq_application.ports import Clock, Investigator, UnitOfWork
from aveniq_application.tenancy import resolve_investigation_scope


@dataclass
class ListInvestigationsQuery:
    org_id: str | None = None
    environment_id: str | None = None
    limit: int = 50
    offset: int = 0
    state: str | None = None


@dataclass
class StartInvestigationCommand:
    benchmark_id: str
    signal: Signal
    org_id: str | None = None
    environment_id: str | None = None
    actor: Actor | None = None


class StartInvestigation:
    def __init__(self, uow: UnitOfWork, clock: Clock) -> None:
        self._uow = uow
        self._clock = clock

    def execute(self, command: StartInvestigationCommand) -> InvestigationAggregate:
        if command.benchmark_id not in ("b03",):
            raise UnsupportedBenchmarkError(command.benchmark_id)

        now = self._clock.now()
        inv_id = new_ulid()
        org_id, environment_id = resolve_investigation_scope(
            command.org_id, command.environment_id
        )
        investigation = Investigation(
            id=inv_id,
            benchmark_id=command.benchmark_id,
            state=InvestigationState.INITIALIZED,
            created_at=now,
            updated_at=now,
            org_id=org_id,
            environment_id=environment_id,
            signal=command.signal,
        )
        self._uow.investigations.create(investigation)
        seq = self._uow.events.next_seq(inv_id)
        request_actor = command.actor or ACTOR_ANONYMOUS_LOCAL
        event = InvestigationEvent(
            seq=seq,
            type="investigation.created",
            occurred_at=now,
            payload={
                "benchmark_id": command.benchmark_id,
                "signal": command.signal.model_dump(mode="json"),
            },
            actor=request_actor,
        )
        self._uow.events.append(inv_id, event)
        self._uow.commit()
        return InvestigationAggregate(investigation=investigation, events=[event])


@dataclass
class RunInvestigationCommand:
    investigation_id: str


class RunInvestigation:
    def __init__(
        self,
        uow: UnitOfWork,
        investigator: Investigator | None,
        clock: Clock,
        run_enabled: bool = True,
    ) -> None:
        self._uow = uow
        self._investigator = investigator
        self._clock = clock
        self._run_enabled = run_enabled

    def execute(self, command: RunInvestigationCommand) -> InvestigationAggregate:
        inv = self._uow.investigations.get(command.investigation_id)
        if inv is None:
            raise InvestigationNotFoundError(command.investigation_id)
        if inv.is_terminal:
            raise InvestigationAlreadyRunError(command.investigation_id)
        if not self._run_enabled or self._investigator is None:
            raise RunNotImplementedError()

        self._investigator.run(command.investigation_id, self._uow)
        self._uow.commit()
        aggregate = self._load_aggregate(command.investigation_id)
        if aggregate is None:
            raise InvestigationNotFoundError(command.investigation_id)
        return aggregate

    def _load_aggregate(self, investigation_id: str) -> InvestigationAggregate | None:
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


class ListInvestigations:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    def execute(self, query: ListInvestigationsQuery) -> list[Investigation]:
        org_id, environment_id = resolve_investigation_scope(query.org_id, query.environment_id)
        limit = min(max(query.limit, 1), 100)
        offset = max(query.offset, 0)
        return self._uow.investigations.list_for_scope(
            org_id,
            environment_id,
            limit=limit,
            offset=offset,
            state=query.state,
        )
