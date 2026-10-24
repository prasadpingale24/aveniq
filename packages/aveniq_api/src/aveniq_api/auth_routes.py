from __future__ import annotations

from fastapi import APIRouter, Depends, Request, Response

from aveniq_adapters.settings import Settings

from aveniq_api.auth.deps import enforce_auth, get_optional_principal
from aveniq_api.auth.session import DevUser, SessionPrincipal, parse_dev_users
from aveniq_api.schemas import AuthConfigResponse, AuthLoginRequest, AuthUserResponse

router = APIRouter()


@router.get("/api/v1/auth/config", response_model=AuthConfigResponse)
def auth_config(request: Request) -> AuthConfigResponse:
    settings: Settings = request.app.state.settings
    return AuthConfigResponse(
        enabled=settings.auth_enabled,
        dev_login=settings.auth_enabled,
    )


@router.get("/api/v1/auth/me", response_model=AuthUserResponse)
def auth_me(
    request: Request,
    principal: SessionPrincipal | None = Depends(get_optional_principal),
) -> AuthUserResponse:
    settings: Settings = request.app.state.settings
    if not settings.auth_enabled:
        return AuthUserResponse(
            authenticated=False,
            user_id=None,
            display_name=None,
        )
    if principal is None:
        return AuthUserResponse(
            authenticated=False,
            user_id=None,
            display_name=None,
        )
    return AuthUserResponse(
        authenticated=True,
        user_id=principal.user_id,
        display_name=principal.display_name,
    )


@router.post("/api/v1/auth/login", response_model=AuthUserResponse)
def auth_login(
    request: Request,
    response: Response,
    body: AuthLoginRequest,
) -> AuthUserResponse:
    settings: Settings = request.app.state.settings
    if not settings.auth_enabled:
        return AuthUserResponse(
            authenticated=False,
            user_id=None,
            display_name=None,
        )

    users = parse_dev_users(settings.auth_dev_users)
    password = users.get(body.username)
    if password is None or password != body.password:
        from fastapi import HTTPException

        raise HTTPException(status_code=401, detail="Invalid username or password")

    store = request.app.state.session_store
    token = store.create(
        DevUser(user_id=body.username, display_name=body.username),
    )
    response.set_cookie(
        key=settings.auth_cookie_name,
        value=token,
        httponly=True,
        samesite="lax",
        max_age=settings.auth_cookie_max_age_sec,
        path="/",
    )
    return AuthUserResponse(
        authenticated=True,
        user_id=body.username,
        display_name=body.username,
    )


@router.post("/api/v1/auth/logout", status_code=204)
def auth_logout(request: Request, response: Response) -> Response:
    settings: Settings = request.app.state.settings
    if settings.auth_enabled:
        enforce_auth(request)
    token = request.cookies.get(settings.auth_cookie_name)
    request.app.state.session_store.delete(token)
    response.delete_cookie(key=settings.auth_cookie_name, path="/")
    return Response(status_code=204)
