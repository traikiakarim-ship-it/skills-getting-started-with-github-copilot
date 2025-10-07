import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_for_activity():
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Remove if already present
    client.delete(f"/activities/{activity}/unregister?email={email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert response.json()["message"].startswith("Signed up")
    # Duplicate signup should fail
    response_dup = client.post(f"/activities/{activity}/signup?email={email}")
    assert response_dup.status_code == 400


def test_unregister_participant():
    email = "testuser2@mergington.edu"
    activity = "Programming Class"
    # Add first
    client.post(f"/activities/{activity}/signup?email={email}")
    # Remove
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    assert "désinscrit" in response.json()["message"]
    # Remove again should fail
    response_fail = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response_fail.status_code == 400


def test_signup_invalid_activity():
    response = client.post("/activities/UnknownActivity/signup?email=foo@bar.com")
    assert response.status_code == 404


def test_unregister_invalid_activity():
    response = client.delete("/activities/UnknownActivity/unregister?email=foo@bar.com")
    assert response.status_code == 404
