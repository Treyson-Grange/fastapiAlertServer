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


def test_calc_criticality():
    """
    Test suite for calc_criticality function.
    """
    test_cases = [
        {"day_diff": 0, "days_notice": 10, "expected": 0},
        {"day_diff": 2, "days_notice": 10, "expected": 0},
        {"day_diff": 3, "days_notice": 10, "expected": 1},
        {"day_diff": 5, "days_notice": 10, "expected": 1},
        {"day_diff": 8, "days_notice": 10, "expected": 2},
        {"day_diff": 10, "days_notice": 10, "expected": 2},
    ]

    for case in test_cases:
        result = calc_criticality(case["day_diff"], case["days_notice"])
        assert (
            result == case["expected"]
        ), f"Expected {case['expected']} but got {result}"
