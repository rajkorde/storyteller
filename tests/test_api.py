from fastapi.testclient import TestClient

from src.api import app


def test_create_story(monkeypatch):
    def dummy_fill_in_details(story):
        story.story_text = "dummy text"

    monkeypatch.setattr("src.api.fill_in_details", dummy_fill_in_details)

    client = TestClient(app)
    payload = {
        "age": 8,
        "interests": "reading",
        "situation": "needs encouragement",
        "guidance": "use bright colors",
    }
    response = client.post("/story", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["student"]["age"] == 8
    assert data["story_text"] == "dummy text"
    assert data["scenario_id"]
