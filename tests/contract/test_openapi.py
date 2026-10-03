from pathlib import Path

import yaml
from fastapi.testclient import TestClient
from openapi_spec_validator import validate
from openapi_spec_validator.readers import read_from_filename

REPO_ROOT = Path(__file__).resolve().parents[2]
OPENAPI_PATH = REPO_ROOT / "engineering" / "api" / "openapi.yaml"


def test_openapi_file_is_valid():
    spec, _ = read_from_filename(str(OPENAPI_PATH))
    validate(spec)


def test_app_exposes_core_paths(client: TestClient):
    openapi = client.get("/openapi.json").json()
    paths = openapi.get("paths", {})
    assert "/health" in paths
    assert "/api/v1/investigations" in paths
    assert "/api/v1/investigations/{investigation_id}" in paths
    assert "/api/v1/investigations/{investigation_id}/run" in paths
    assert "/api/v1/playground/scenarios" in paths
    assert "/api/v1/playground/scenarios/{scenario_id}/runs" in paths


def test_create_investigation_has_b03_openapi_example(client: TestClient):
    openapi = client.get("/openapi.json").json()
    post = openapi["paths"]["/api/v1/investigations"]["post"]
    content = post["requestBody"]["content"]["application/json"]
    examples = content.get("examples") or {}
    assert "b03_alert" in examples
    assert examples["b03_alert"]["value"]["benchmark_id"] == "b03"
    assert examples["b03_alert"]["value"]["signal"]["service"] == "checkout-api"


def test_openapi_yaml_loads():
    data = yaml.safe_load(OPENAPI_PATH.read_text(encoding="utf-8"))
    assert data["openapi"].startswith("3.")
    assert data["info"]["title"] == "AVENIQ Investigation API"
