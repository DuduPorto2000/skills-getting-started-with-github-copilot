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


def test_removes_participant_from_activity():
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    original_participants = list(activities[activity_name]["participants"])

    try:
        with TestClient(app) as client:
            response = client.delete(
                f"/activities/{activity_name}/participants/{email}",
            )

        assert response.status_code == 200
        assert email not in activities[activity_name]["participants"]
    finally:
        activities[activity_name]["participants"] = original_participants
