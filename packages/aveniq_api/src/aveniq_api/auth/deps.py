from __future__ import annotations

from fastapi import HTTPException, Request

from aveniq_adapters.settings import Settings
from aveniq_api.auth.session import SessionPrincipal


def _session_token(request: Request) -> str | None:
    settings: Settings = request.app.state.settings
    token = request.cookies.get(settings.auth_cookie_name)
    if token:
        return token
    auth = request.headers.get("Authorization")
    if auth and auth.lower().startswith("bearer "):
        return auth[7:].strip() or None
    return None


def get_optional_principal(request: Request) -> SessionPrincipal | None:
    settings: Settings = request.app.state.settings
    if not settings.auth_enabled:
        return None
    store = request.app.state.session_store
    return store.get(_session_token(request))


def enforce_auth(request: Request) -> SessionPrincipal | None:
    """When auth is enabled, require a valid session; otherwise return None."""
    settings: Settings = request.app.state.settings
    if not settings.auth_enabled:
        return None
    principal = get_optional_principal(request)
    if principal is None:
        raise HTTPException(status_code=401, detail="Authentication required")
    return principal
