from __future__ import annotations

import logging
import uuid

from fastapi import APIRouter, Body, Header, Path, Request, Response

from aveniq_domain.exceptions import InvestigationNotFoundError
from aveniq_domain.models import Signal
from aveniq_domain.enums import SignalKind

from aveniq_application.use_cases import RunInvestigationCommand, StartInvestigationCommand

from aveniq_adapters.factory import AppServices
from aveniq_adapters.observability.otel import get_tracer

from aveniq_api import __version__
from aveniq_api.openapi_examples import B03_CREATE_REQUEST, EXAMPLE_INVESTIGATION_ID
from aveniq_api.schemas import (
    CreateInvestigationRequest,
    HealthResponse,
    InvestigationResponse,
    aggregate_to_response,
)

logger = logging.getLogger("aveniq.api")

router = APIRouter()


def _request_id(header: str | None) -> str:
    return header or str(uuid.uuid4())


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", service="aveniq-api", version=__version__)


@router.post(
    "/api/v1/investigations",
    response_model=InvestigationResponse,
    status_code=201,
    summary="Start investigation (benchmark b03: DB connection exhaustion)",
)
def create_investigation(
    request: Request,
    response: Response,
    body: CreateInvestigationRequest = Body(
        ...,
        openapi_examples={
            "b03_alert": {
                "summary": "B03 — checkout-api alert",
                "description": (
                    "Starts an investigation against fixture package b03. "
                    "Call POST .../run next to execute the deterministic playbook."
                ),
                "value": B03_CREATE_REQUEST,
            },
        },
    ),
    x_request_id: str | None = Header(default=None, alias="X-Request-Id"),
) -> InvestigationResponse:
    rid = _request_id(x_request_id)
    response.headers["X-Request-Id"] = rid
    services: AppServices = request.app.state.services
    tracer = get_tracer()
    with tracer.start_as_current_span("aveniq.investigation.start") as span:
        span.set_attribute("request_id", rid)
        signal = Signal(
            kind=SignalKind(body.signal.kind),
            fired_at=body.signal.fired_at,
            service=body.signal.service,
            description=body.signal.description,
            raw=body.signal.raw,
        )
        cmd = StartInvestigationCommand(
            benchmark_id=body.benchmark_id,
            signal=signal,
            org_id=body.org_id,
            environment_id=body.environment_id,
        )
        aggregate = services.start_investigation.execute(cmd)
        span.set_attribute("investigation_id", aggregate.investigation.id)
        logger.info(
            "investigation created",
            extra={
                "request_id": rid,
                "investigation_id": aggregate.investigation.id,
                "benchmark_id": body.benchmark_id,
            },
        )
        return aggregate_to_response(aggregate)


@router.get("/api/v1/investigations/{investigation_id}", response_model=InvestigationResponse)
def get_investigation(
    request: Request,
    response: Response,
    investigation_id: str = Path(
        ...,
        description="Investigation id returned from POST /api/v1/investigations",
        examples=[EXAMPLE_INVESTIGATION_ID],
    ),
    x_request_id: str | None = Header(default=None, alias="X-Request-Id"),
) -> InvestigationResponse:
    rid = _request_id(x_request_id)
    response.headers["X-Request-Id"] = rid
    services: AppServices = request.app.state.services
    aggregate = services.aggregate_reader.load_aggregate(investigation_id)
    if aggregate is None:
        raise InvestigationNotFoundError(investigation_id)
    return aggregate_to_response(aggregate)


@router.post(
    "/api/v1/investigations/{investigation_id}/run",
    response_model=InvestigationResponse,
    summary="Run B03 investigation playbook",
)
def run_investigation(
    request: Request,
    response: Response,
    investigation_id: str = Path(
        ...,
        description="Investigation id in state initialized",
        examples=[EXAMPLE_INVESTIGATION_ID],
    ),
    x_request_id: str | None = Header(default=None, alias="X-Request-Id"),
) -> InvestigationResponse:
    rid = _request_id(x_request_id)
    response.headers["X-Request-Id"] = rid
    services: AppServices = request.app.state.services
    tracer = get_tracer()
    with tracer.start_as_current_span("aveniq.investigation.run") as span:
        span.set_attribute("request_id", rid)
        span.set_attribute("investigation_id", investigation_id)
        aggregate = services.run_investigation.execute(RunInvestigationCommand(investigation_id))
        logger.info(
            "investigation run completed",
            extra={
                "request_id": rid,
                "investigation_id": investigation_id,
                "state": aggregate.investigation.state.value,
            },
        )
        return aggregate_to_response(aggregate)
