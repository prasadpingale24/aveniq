from __future__ import annotations

import secrets
from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class DevUser:
    user_id: str
    display_name: str


@dataclass(frozen=True)
class SessionPrincipal:
    user_id: str
    display_name: str


def parse_dev_users(raw: str) -> dict[str, str]:
    """Parse `user:pass,user2:pass2` into username -> password."""
    users: dict[str, str] = {}
    for part in raw.split(","):
        part = part.strip()
        if not part or ":" not in part:
            continue
        username, password = part.split(":", 1)
        username = username.strip()
        if username:
            users[username] = password
    return users


class InMemorySessionStore:
    def __init__(self) -> None:
        self._sessions: Dict[str, SessionPrincipal] = {}

    def create(self, user: DevUser) -> str:
        token = secrets.token_urlsafe(32)
        self._sessions[token] = SessionPrincipal(
            user_id=user.user_id,
            display_name=user.display_name,
        )
        return token

    def get(self, token: str | None) -> SessionPrincipal | None:
        if not token:
            return None
        return self._sessions.get(token)

    def delete(self, token: str | None) -> None:
        if token:
            self._sessions.pop(token, None)
