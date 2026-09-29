from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from aveniq_adapters.settings import Settings
from aveniq_api.app import create_app

REPO_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def settings(tmp_path: Path) -> Settings:
    return Settings(
        aveniq_env="ci",
        aveniq_sqlite_path=tmp_path / "test.db",
        fixture_root=REPO_ROOT / "fixtures",
        investigation_run_enabled=True,
    )


@pytest.fixture
def client(settings: Settings) -> TestClient:
    app = create_app(settings)
    with TestClient(app) as test_client:
        yield test_client
