from fastapi.testclient import TestClient
from main import app
from app.models import AlertModel
from app.utils import (
    verify_alert,
    verify_manual_alert,
    calc_criticality,
    verify_group_exist,
)

client = TestClient(app)


def test_verify_alert():
    """
    Test the verify_alert function.
    """
    alert = AlertModel(
        message="test",
        criticality=1,
        autoClear=True,
        timestamp="2024-11-24T00:00:02.784Z",
        clearAfter=100,
        group="usuIT",
    )

    assert verify_alert(alert) == True

    alert = AlertModel(
        message="test",
        criticality=1,
        autoClear=True,
        timestamp="2024-11-24T00:00:02.784Z",
        clearAfter=-100,
        group="usuIT",
    )

    assert verify_alert(alert) == False

    alert = AlertModel(
        message="test",
        criticality=3,
        autoClear=True,
        timestamp="2024-11-24T00:00:02.784Z",
        clearAfter=100,
        group="usuIT",
    )

    assert verify_alert(alert) == False

    alert = AlertModel(
        message="test",
        criticality=1,
        autoClear=True,
        timestamp="2024-11-24T00:00:02.784Z",
        clearAfter=100,
        group="usuITs",
    )

    assert verify_alert(alert) == False


def test_verify_manual_alert():
    """
    Test the verify_manual_alert function.
    """
    alert = AlertModel(
        message="test",
        daysNotice=1,
        group="usuIT",
    )

    assert verify_manual_alert(alert) == True

    alert = AlertModel(
        message="",
        daysNotice=1,
        group="usuIT",
    )

    assert verify_manual_alert(alert) == False

    alert = AlertModel(
        message="test",
        daysNotice=-1,
        group="usuIT",
    )

    assert verify_manual_alert(alert) == False

    alert = AlertModel(
        message="test",
        daysNotice=1,
        group="usuITs",
    )

    assert verify_manual_alert(alert) == False


def test_verify_group_exist():
    """
    Test the verify_group_exist function.
    """
    assert verify_group_exist("usuIT") == True
    assert verify_group_exist("usuITs") == False
    
