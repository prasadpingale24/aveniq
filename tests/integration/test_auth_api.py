from pathlib import Path

from fastapi.testclient import TestClient

from aveniq_adapters.settings import Settings
from aveniq_api.app import create_app

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_playground_requires_auth_when_enabled(tmp_path):
    settings = Settings(
        aveniq_env="local",
        aveniq_sqlite_path=tmp_path / "auth.db",
        fixture_root=REPO_ROOT / "fixtures",
        auth_enabled=True,
        auth_dev_users="engineer:aveniq",
    )
    with TestClient(create_app(settings)) as client:
        resp = client.get("/api/v1/playground/scenarios")
        assert resp.status_code == 401


def test_login_sets_session_and_allows_playground(tmp_path):
    settings = Settings(
        aveniq_env="local",
        aveniq_sqlite_path=tmp_path / "auth.db",
        fixture_root=REPO_ROOT / "fixtures",
        auth_enabled=True,
        auth_dev_users="engineer:aveniq",
    )
    with TestClient(create_app(settings)) as client:
        login = client.post(
            "/api/v1/auth/login",
            json={"username": "engineer", "password": "aveniq"},
        )
        assert login.status_code == 200
        assert login.json()["authenticated"] is True

        scenarios = client.get("/api/v1/playground/scenarios")
        assert scenarios.status_code == 200
