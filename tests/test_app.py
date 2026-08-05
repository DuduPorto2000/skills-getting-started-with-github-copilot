from fastapi.testclient import TestClient

from src.app import app, activities


def test_prevents_duplicate_signup_for_same_activity():
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    original_participants = list(activities[activity_name]["participants"])

    with TestClient(app) as client:
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email},
        )

    assert response.status_code == 400
    assert activities[activity_name]["participants"] == original_participants
