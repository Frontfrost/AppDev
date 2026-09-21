from fastapi.testclient import TestClient

try:
    from app.main import app
except ImportError:
    from main import app


client = TestClient(app)


def test_basic_division():
    r = client.post("/calculate", json={"expr": "30/4"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 7.5) < 1e-9


def test_percent_subtraction():
    r = client.post("/calculate", json={"expr": "100 - 6%"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 94.0) < 1e-9


def test_standalone_percent():
    r = client.post("/calculate", json={"expr": "6%"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 0.06) < 1e-9


def test_invalid_expr_returns_ok_false():
    r = client.post("/calculate", json={"expr": "2**(3"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is False
    assert "error" in data and data["error"] != ""


def test_history_logging():
    client.delete("/history")
    client.post("/calculate", json={"expr": "10 + 20"})

    r = client.get("/history")
    assert r.status_code == 200
    history = r.json()
    assert len(history) == 1
    assert history[0]["expr"] == "10 + 20"
    assert history[0]["result"] == 30
    assert "timestamp" in history[0]


def test_multiplication():
    for expr in ["7 * 9", "7 × 9", "7x9"]:
        r = client.post("/calculate", json={"expr": expr})
        assert r.status_code == 200
        data = r.json()
        assert data["ok"] is True
        assert data["result"] == 63