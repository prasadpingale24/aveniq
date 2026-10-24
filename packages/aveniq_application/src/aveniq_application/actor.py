"""Actor attribution defaults (ADR-018)."""

from __future__ import annotations

from aveniq_domain.enums import ActorKind
from aveniq_domain.models import Actor

ACTOR_ANONYMOUS_LOCAL = Actor(kind=ActorKind.ANONYMOUS, id="local")
ACTOR_SERVICE_PLAYGROUND_RUNNER = Actor(kind=ActorKind.SERVICE, id="playground-runner")
ACTOR_SERVICE_INVESTIGATOR_B03 = Actor(kind=ActorKind.SERVICE, id="investigator-b03")
ACTOR_SYSTEM_PLAYGROUND = Actor(kind=ActorKind.SYSTEM, id="playground")


def resolve_request_actor(x_actor_id: str | None) -> Actor:
    """HTTP request actor until auth middleware supplies a user principal."""
    if x_actor_id and x_actor_id.strip():
        return Actor(kind=ActorKind.ANONYMOUS, id=x_actor_id.strip())
    return ACTOR_ANONYMOUS_LOCAL


def actor_from_user(user_id: str, display_name: str | None = None) -> Actor:
    return Actor(
        kind=ActorKind.USER,
        id=user_id,
        display=display_name or user_id,
    )
