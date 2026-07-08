from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_route_returns_ok():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "mode": "simulation", "tenant_connected": False}


def test_static_ui_contains_demo_controls():
    response = client.get("/")

    assert response.status_code == 200
    assert "Example prompts" in response.text
    assert "Planned Actions" in response.text
    assert "Evidence" in response.text
    assert "Safety Notes" in response.text


def test_chat_endpoint_returns_structured_planned_actions():
    response = client.post(
        "/chat",
        json={
            "scenario": "access_troubleshooting",
            "message": "Maria cannot access Teams.",
        },
    )

    payload = response.json()

    assert response.status_code == 200
    assert payload["scenario"] == "access_troubleshooting"
    assert payload["planned_actions"]
    assert payload["evidence"]
    assert all(action["operation"] == "plan" for action in payload["planned_actions"])
