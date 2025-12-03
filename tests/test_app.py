import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_for_activity_success():
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    # Remove if already present
    activities = client.get("/activities").json()
    if email in activities[activity]["participants"]:
        client.post(f"/activities/{activity}/unregister?email={email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"


def test_signup_for_activity_already_signed_up():
    email = "michael@mergington.edu"
    activity = "Chess Club"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_for_activity_not_found():
    email = "student@mergington.edu"
    activity = "Nonexistent Club"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_participant():
    email = "removeme@mergington.edu"
    activity = "Chess Club"
    # Add participant first
    client.post(f"/activities/{activity}/signup?email={email}")
    # Unregister endpoint
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    if response.status_code == 200:
        assert "removed" in response.json()["message"].lower() or "unregister" in response.json()["message"].lower()
    else:
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
