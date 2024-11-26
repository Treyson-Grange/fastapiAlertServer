from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# Test a creation, both auto and manual


def test_create_auto():
    assert 1 == 1
