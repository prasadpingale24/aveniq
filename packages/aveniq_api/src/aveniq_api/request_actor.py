from __future__ import annotations

from fastapi import Request

from aveniq_domain.models import Actor

from aveniq_application.actor import actor_from_user, resolve_request_actor
from aveniq_api.auth.session import SessionPrincipal


def resolve_api_actor(
    request: Request,
    principal: SessionPrincipal | None,
    x_actor_id: str | None,
) -> Actor:
    if principal is not None:
        return actor_from_user(principal.user_id, principal.display_name)
    return resolve_request_actor(x_actor_id)
