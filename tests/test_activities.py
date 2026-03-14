def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all activities with correct structure"""
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()

    # Should have all 9 activities
    expected_activities = [
        "Chess Club", "Programming Class", "Gym Class",
        "Soccer Team", "Basketball Club", "Art Club",
        "Drama Society", "Math Olympiad", "Debate Club"
    ]

    assert len(data) == 9
    for activity in expected_activities:
        assert activity in data

    # Check structure of one activity
    chess_club = data["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    assert isinstance(chess_club["participants"], list)