def test_root_redirects_to_static_index(client):
    """Test that GET / redirects to /static/index.html"""
    response = client.get("/", follow_redirects=False)  # Don't follow redirect

    assert response.status_code == 307  # Temporary redirect
    assert response.headers["location"] == "/static/index.html"