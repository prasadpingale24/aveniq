def test_create_investigation_201(client):
    response = client.post(
        "/api/v1/investigations",
        json={
            "benchmark_id": "b03",
            "signal": {
                "kind": "alert",
                "fired_at": "2026-09-28T14:36:00Z",
                "service": "checkout-api",
                "description": "checkout-api error rate high",
            },
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["investigation"]["benchmark_id"] == "b03"
    assert body["investigation"]["state"] == "initialized"
    assert body["events"][0]["type"] == "investigation.created"
    assert body["events"][0]["actor"]["kind"] == "anonymous"
    assert body["events"][0]["actor"]["id"] == "local"


def test_create_investigation_with_auth_user_actor(client_with_auth):
    client, _ = client_with_auth
    login = client.post(
        "/api/v1/auth/login",
        json={"username": "engineer", "password": "aveniq"},
    )
    assert login.status_code == 200
    resp = client.post(
        "/api/v1/investigations",
        json={
            "benchmark_id": "b03",
            "signal": {
                "kind": "alert",
                "fired_at": "2026-09-28T14:36:00Z",
                "service": "checkout-api",
                "description": "checkout-api error rate high",
            },
        },
    )
    assert resp.status_code == 201
    assert resp.json()["events"][0]["actor"]["kind"] == "user"
    assert resp.json()["events"][0]["actor"]["id"] == "engineer"


def test_get_investigation_404(client):
    response = client.get("/api/v1/investigations/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
    assert response.json()["code"] == "investigation_not_found"


def test_get_investigation_after_create(client):
    create = client.post(
        "/api/v1/investigations",
        json={
            "benchmark_id": "b03",
            "signal": {"kind": "alert", "service": "checkout-api"},
        },
    )
    inv_id = create.json()["investigation"]["id"]
    get = client.get(f"/api/v1/investigations/{inv_id}")
    assert get.status_code == 200
    assert get.json()["investigation"]["id"] == inv_id


def test_list_investigations_empty(client):
    resp = client.get("/api/v1/investigations")
    assert resp.status_code == 200
    assert resp.json()["investigations"] == []


def test_list_investigations_after_create_and_run(client):
    create = client.post(
        "/api/v1/investigations",
        json={
            "benchmark_id": "b03",
            "signal": {
                "kind": "alert",
                "service": "checkout-api",
                "description": "error rate high",
            },
        },
    )
    inv_id = create.json()["investigation"]["id"]
    client.post(f"/api/v1/investigations/{inv_id}/run")
    listed = client.get("/api/v1/investigations")
    assert listed.status_code == 200
    items = listed.json()["investigations"]
    assert len(items) == 1
    assert items[0]["id"] == inv_id
    assert items[0]["state"] == "rca_candidate"
    assert items[0]["service"] == "checkout-api"
    filtered = client.get("/api/v1/investigations", params={"state": "initialized"})
    assert filtered.json()["investigations"] == []


def test_run_twice_returns_409(client):
    create = client.post(
        "/api/v1/investigations",
        json={
            "benchmark_id": "b03",
            "signal": {
                "kind": "alert",
                "fired_at": "2026-09-28T14:36:00Z",
                "service": "checkout-api",
            },
        },
    )
    inv_id = create.json()["investigation"]["id"]
    first = client.post(f"/api/v1/investigations/{inv_id}/run")
    assert first.status_code == 200
    second = client.post(f"/api/v1/investigations/{inv_id}/run")
    assert second.status_code == 409
    assert second.json()["code"] == "investigation_already_run"
