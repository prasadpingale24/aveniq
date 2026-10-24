"""Serialize investigation event envelope for payload_json (ADR-018)."""

from __future__ import annotations

import json
from typing import Any

from aveniq_domain.enums import ActorKind
from aveniq_domain.models import Actor, InvestigationEvent


def event_to_storage_json(event: InvestigationEvent) -> str:
    body: dict[str, Any] = {"payload": event.payload}
    if event.actor is not None:
        body["actor"] = event.actor.model_dump(mode="json")
    return json.dumps(body)


def event_from_storage_row(
    seq: int,
    type: str,
    occurred_at_str: str,
    payload_json: str,
    str_to_dt,
) -> InvestigationEvent:
    raw = json.loads(payload_json)
    if isinstance(raw.get("payload"), dict):
        payload = raw["payload"]
        actor_data = raw.get("actor")
    else:
        payload = raw
        actor_data = None

    actor: Actor | None = None
    if isinstance(actor_data, dict) and actor_data.get("kind") and actor_data.get("id"):
        actor = Actor(
            kind=ActorKind(actor_data["kind"]),
            id=str(actor_data["id"]),
            display=actor_data.get("display"),
        )

    return InvestigationEvent(
        seq=seq,
        type=type,
        occurred_at=str_to_dt(occurred_at_str),
        payload=payload,
        actor=actor,
    )
