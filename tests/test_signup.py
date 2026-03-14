def test_signup_successful(client):
    """Test successful signup for an activity"""
    response = client.post("/activities/Chess%20Club/signup?email=test@example.com")

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Signed up test@example.com for Chess Club"

    # Verify participant was added
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert "test@example.com" in activities["Chess Club"]["participants"]


def test_signup_duplicate_email(client):
    """Test that signing up twice returns 400 error"""
    # First signup
    client.post("/activities/Chess%20Club/signup?email=duplicate@example.com")

    # Second signup should fail
    response = client.post("/activities/Chess%20Club/signup?email=duplicate@example.com")

    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Student already signed up"


def test_signup_invalid_activity(client):
    """Test signup for non-existent activity returns 404"""
    response = client.post("/activities/NonExistent/signup?email=test@example.com")

    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Activity not found"


def test_signup_different_activities(client):
    """Test that same email can signup for different activities"""
    email = "multi@example.com"

    # Signup for two different activities
    response1 = client.post("/activities/Chess%20Club/signup?email=" + email)
    response2 = client.post("/activities/Soccer%20Team/signup?email=" + email)

    assert response1.status_code == 200
    assert response2.status_code == 200

    # Verify in both
    activities = client.get("/activities").json()
    assert email in activities["Chess Club"]["participants"]
    assert email in activities["Soccer Team"]["participants"]