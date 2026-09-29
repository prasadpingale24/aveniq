from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from aveniq_domain.exceptions import (
    DomainError,
    InvestigationAlreadyRunError,
    InvestigationNotFoundError,
    RunNotImplementedError,
    UnsupportedBenchmarkError,
)

from aveniq_api.schemas import ProblemDetail

PROBLEM_BASE = "https://aveniq.dev/problems"


def problem(
    code: str,
    title: str,
    status: int,
    detail: str | None = None,
    instance: str | None = None,
    errors: list[dict[str, str]] | None = None,
) -> ProblemDetail:
    return ProblemDetail(
        type=f"{PROBLEM_BASE}/{code}",
        title=title,
        status=status,
        code=code,
        detail=detail,
        instance=instance,
        errors=errors,
    )


def problem_response(p: ProblemDetail) -> JSONResponse:
    return JSONResponse(
        status_code=p.status,
        content=p.model_dump(exclude_none=True),
        media_type="application/problem+json",
    )


def register_exception_handlers(app) -> None:
    @app.exception_handler(RequestValidationError)
    async def validation_handler(request: Request, exc: RequestValidationError):
        errors = []
        for err in exc.errors():
            loc = ".".join(str(x) for x in err.get("loc", []))
            errors.append({"field": loc, "message": err.get("msg", "invalid")})
        return problem_response(
            problem(
                "validation_error",
                "Validation Error",
                422,
                detail="Request validation failed",
                instance=str(request.url.path),
                errors=errors,
            )
        )

    @app.exception_handler(ValidationError)
    async def pydantic_validation_handler(request: Request, exc: ValidationError):
        return problem_response(
            problem(
                "validation_error",
                "Validation Error",
                422,
                detail=str(exc),
                instance=str(request.url.path),
            )
        )

    @app.exception_handler(InvestigationNotFoundError)
    async def not_found_handler(request: Request, exc: InvestigationNotFoundError):
        return problem_response(
            problem(
                "investigation_not_found",
                "Not Found",
                404,
                detail=str(exc),
                instance=str(request.url.path),
            )
        )

    @app.exception_handler(InvestigationAlreadyRunError)
    async def already_run_handler(request: Request, exc: InvestigationAlreadyRunError):
        return problem_response(
            problem(
                "investigation_already_run",
                "Conflict",
                409,
                detail=str(exc),
                instance=str(request.url.path),
            )
        )

    @app.exception_handler(UnsupportedBenchmarkError)
    async def unsupported_benchmark_handler(request: Request, exc: UnsupportedBenchmarkError):
        return problem_response(
            problem(
                "unsupported_benchmark",
                "Unprocessable Entity",
                422,
                detail=str(exc),
                instance=str(request.url.path),
            )
        )

    @app.exception_handler(RunNotImplementedError)
    async def not_implemented_handler(request: Request, exc: RunNotImplementedError):
        return problem_response(
            problem(
                "investigation_run_not_implemented",
                "Not Implemented",
                501,
                detail="Investigation run is not available",
                instance=str(request.url.path),
            )
        )

    @app.exception_handler(DomainError)
    async def domain_handler(request: Request, exc: DomainError):
        return problem_response(
            problem(
                "internal_error",
                "Internal Server Error",
                500,
                detail=str(exc),
                instance=str(request.url.path),
            )
        )

    @app.exception_handler(Exception)
    async def unhandled_handler(request: Request, exc: Exception):
        return problem_response(
            problem(
                "internal_error",
                "Internal Server Error",
                500,
                detail="An unexpected error occurred",
                instance=str(request.url.path),
            )
        )
