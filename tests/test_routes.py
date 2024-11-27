from fastapi.testclient import TestClient
from main import app
from app.models import AlertModel, ManualAlertModel, GroupModel

client = TestClient(app)


def test_create_auto_success():
    """
    Test the creation of an auto alert.

    This test will pass if the response status code is 200.
    """
    test_alert = {
        "message": "test",
        "criticality": "1",
        "autoClear": "True",
        "timestamp": "2024-11-24T00:00:02.784Z",
        "clearAfter": "100",
        "group": "usuIT",
    }

    response = client.post("/create", json=test_alert)

    assert response.status_code == 200


def test_create_auto_fail():
    """
    Test the invalid creation of an auto alert.
    Make sure it handles the error correctly.

    This test will pass if the response status code is 400.
    """
    test_alert = {
        "message": "test",
        "criticality": "1",
        "autoClear": "True",
        "timestamp": "2024-11-24T00:00:02.784Z",
        "clearAfter": "100",
        "group": "usuITs",
    }

    response = client.post("/create", json=test_alert)

    assert response.status_code == 400
