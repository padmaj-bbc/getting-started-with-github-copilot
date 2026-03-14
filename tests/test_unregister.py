def test_unregister_successful(client):
    """Test successful unregister from an activity"""
    email = "unregister@example.com"

    # First signup
    client.post("/activities/Chess%20Club/signup?email=" + email)

    # Then unregister
    response = client.delete("/activities/Chess%20Club/unregister?email=" + email)

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Unregistered unregister@example.com from Chess Club"

    # Verify participant was removed
    activities = client.get("/activities").json()
    assert email not in activities["Chess Club"]["participants"]


def test_unregister_not_enrolled(client):
    """Test unregistering student not signed up returns 400"""
    response = client.delete("/activities/Chess%20Club/unregister?email=notenrolled@example.com")

    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Student not signed up for this activity"


def test_unregister_invalid_activity(client):
    """Test unregister from non-existent activity returns 404"""
    response = client.delete("/activities/NonExistent/unregister?email=test@example.com")

    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Activity not found"


def test_unregister_from_one_activity_keeps_others(client):
    """Test unregistering from one activity keeps enrollment in others"""
    email = "multi@example.com"

    # Signup for two activities
    client.post("/activities/Chess%20Club/signup?email=" + email)
    client.post("/activities/Soccer%20Team/signup?email=" + email)

    # Unregister from one
    client.delete("/activities/Chess%20Club/unregister?email=" + email)

    # Verify removed from Chess Club but still in Soccer Team
    activities = client.get("/activities").json()
    assert email not in activities["Chess Club"]["participants"]
    assert email in activities["Soccer Team"]["participants"]