from fastapi.testclient import TestClient

from src.app import app, activities


def test_get_activities_returns_activity_list():
    with TestClient(app) as client:
        response = client.get("/activities")

    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "Chess Club" in response.json()


def test_signup_for_activity_adds_participant():
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    original_participants = list(activities[activity_name]["participants"])

    try:
        with TestClient(app) as client:
            response = client.post(
                f"/activities/{activity_name}/signup",
                params={"email": email},
            )

        assert response.status_code == 200
        assert email in activities[activity_name]["participants"]
    finally:
        activities[activity_name]["participants"] = original_participants


def test_remove_participant_from_activity():
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
