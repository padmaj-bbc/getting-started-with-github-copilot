import pytest
from fastapi.testclient import TestClient
import src.app as app_module

# Store the original activities data for resetting between tests
original_activities = app_module.activities.copy()

@pytest.fixture
def client():
    """FastAPI test client with reset activities database"""
    # Reset the global activities dict before each test
    app_module.activities = original_activities.copy()
    return TestClient(app_module.app)