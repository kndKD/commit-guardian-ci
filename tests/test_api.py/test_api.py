"""Tests for the Day 4 API additions: /api/status, /api/echo and
JSON error responses.
"""

from app.main import app


def _client():
    app.config["TESTING"] = True
    return app.test_client()


def test_status_returns_version_and_uptime():
    resp = _client().get("/api/status")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["service"] == "system-core"
    assert data["project"] == "commit-guardian-ci"
    assert data["version"] == "0.1.0"
    assert data["status"] == "ok"
    assert isinstance(data["uptime_seconds"], int)
    assert data["uptime_seconds"] >= 0
    assert "/api/echo" in data["endpoints"]


def test_echo_round_trip():
    resp = _client().post("/api/echo", json={"msg": "hi", "n": 3})
    assert resp.status_code == 200
    assert resp.get_json() == {"echo": {"msg": "hi", "n": 3}}


def test_echo_list_payload():
    resp = _client().post("/api/echo", json=[1, 2, 3])
    assert resp.status_code == 200
    assert resp.get_json() == {"echo": [1, 2, 3]}


def test_echo_empty_body_is_400():
    resp = _client().post("/api/echo")
    assert resp.status_code == 400
    assert resp.get_json()["error"] == "bad_request"


def test_echo_invalid_json_is_400():
    resp = _client().post(
        "/api/echo", data="{not json", content_type="application/json"
    )
    assert resp.status_code == 400
    assert resp.get_json()["error"] == "bad_request"


def test_unknown_route_404_is_json():
    resp = _client().get("/no-such-route")
    assert resp.status_code == 404
    data = resp.get_json()
    assert data["error"] == "not_found"
    assert "message" in data


def test_wrong_method_405_is_json():
    resp = _client().post("/api/hello", json={})
    assert resp.status_code == 405
    assert resp.get_json()["error"] == "method_not_allowed"


def test_index_project_name():
    resp = _client().get("/")
    assert resp.get_json()["project"] == "commit-guardian-ci"
