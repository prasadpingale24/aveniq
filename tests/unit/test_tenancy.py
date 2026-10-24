from aveniq_application.tenancy import (
    DEFAULT_ENVIRONMENT_ID,
    DEFAULT_ORG_ID,
    resolve_investigation_scope,
)


def test_resolve_investigation_scope_applies_defaults() -> None:
    org, env = resolve_investigation_scope(None, None)
    assert org == DEFAULT_ORG_ID
    assert env == DEFAULT_ENVIRONMENT_ID


def test_resolve_investigation_scope_preserves_explicit() -> None:
    org, env = resolve_investigation_scope("acme", "production")
    assert org == "acme"
    assert env == "production"
