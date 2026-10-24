from __future__ import annotations

import logging
import uuid

from fastapi import APIRouter, Depends, Header, Path, Request, Response

from aveniq_application.playground import list_scenarios, run_scenario_inprocess
from aveniq_api.auth.deps import enforce_auth
from aveniq_api.auth.session import SessionPrincipal
from aveniq_api.request_actor import resolve_api_actor
from aveniq_application.playground.driver import PlaygroundError

from aveniq_api.errors import problem, problem_response
from aveniq_api.schemas import (
    InvestigationResponse,
    PlaygroundRunResponse,
    PlaygroundScenarioListResponse,
    PlaygroundScenarioSummary,
    aggregate_to_response,
)

logger = logging.getLogger("aveniq.api.playground")

router = APIRouter()


def _request_id(header: str | None) -> str:
    return header or str(uuid.uuid4())


@router.get(
    "/api/v1/playground/scenarios",
    response_model=PlaygroundScenarioListResponse,
    summary="List Playground scenarios",
)
def list_playground_scenarios(
    request: Request,
    _principal: SessionPrincipal | None = Depends(enforce_auth),
) -> PlaygroundScenarioListResponse:
    scenarios = [
        PlaygroundScenarioSummary(
            scenario_id=s.scenario_id,
            benchmark_id=s.benchmark_id,
            title=s.title,
            description=s.description,
            subtitle=s.subtitle,
            runnable=s.runnable,
            status=s.status,
        )
        for s in list_scenarios()
    ]
    return PlaygroundScenarioListResponse(scenarios=scenarios)


@router.post(
    "/api/v1/playground/scenarios/{scenario_id}/runs",
    response_model=PlaygroundRunResponse,
    status_code=201,
    summary="Run Playground scenario end-to-end",
)
def run_playground_scenario(
    request: Request,
    response: Response,
    scenario_id: str = Path(..., examples=["b03"]),
    x_request_id: str | None = Header(default=None, alias="X-Request-Id"),
    principal: SessionPrincipal | None = Depends(enforce_auth),
) -> PlaygroundRunResponse | Response:
    rid = _request_id(x_request_id)
    response.headers["X-Request-Id"] = rid
    settings = request.app.state.settings
    services = request.app.state.services
    run_actor = resolve_api_actor(request, principal, None)

    def _payload(aggregate):
        return aggregate_to_response(aggregate).model_dump(mode="json")

    try:
        result = run_scenario_inprocess(
            scenario_id,
            settings.checkout_standin_url,
            services,
            _payload,
            run_actor=run_actor,
        )
    except PlaygroundError as exc:
        if exc.code == "scenario_not_found":
            return problem_response(
                problem(
                    "scenario_not_found",
                    "Not Found",
                    404,
                    detail=str(exc),
                    instance=str(request.url.path),
                )
            )
        if exc.code == "scenario_not_runnable":
            return problem_response(
                problem(
                    "scenario_not_runnable",
                    "Conflict",
                    409,
                    detail=str(exc),
                    instance=str(request.url.path),
                )
            )
        if exc.code == "playground_timeout":
            return problem_response(
                problem(
                    "playground_timeout",
                    "Gateway Timeout",
                    504,
                    detail=str(exc),
                    instance=str(request.url.path),
                )
            )
        return problem_response(
            problem(
                "playground_upstream_error",
                "Bad Gateway",
                502,
                detail=str(exc),
                instance=str(request.url.path),
            )
        )

    inv_body = InvestigationResponse.model_validate(result.investigation)
    logger.info(
        "playground run completed",
        extra={
            "request_id": rid,
            "scenario_id": scenario_id,
            "investigation_id": result.investigation_id,
            "state": result.state,
        },
    )
    return PlaygroundRunResponse(
        scenario_id=result.scenario_id,
        investigation_id=result.investigation_id,
        state=result.state,
        investigation=inv_body,
    )
