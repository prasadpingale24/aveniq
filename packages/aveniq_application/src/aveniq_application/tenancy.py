"""Investigation isolation defaults (ADR-017)."""

from __future__ import annotations

DEFAULT_ORG_ID = "local"
DEFAULT_ENVIRONMENT_ID = "playground"


def resolve_investigation_scope(
    org_id: str | None,
    environment_id: str | None,
) -> tuple[str, str | None]:
    """Apply server defaults when callers omit scope (Playground / local-dev)."""
    resolved_org = org_id if org_id is not None else DEFAULT_ORG_ID
    resolved_env = environment_id if environment_id is not None else DEFAULT_ENVIRONMENT_ID
    return resolved_org, resolved_env
