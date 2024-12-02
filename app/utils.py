from app.models import GroupModel
from fastapi import HTTPException, Header
import os

API_KEYS = os.getenv("ACCEPTED_KEYS").split(",")


def verify_api_key(api_key: str = Header(...)):
    """
    Verify that the API key is valid.

    Parameters:
        api_key (str): The API key.

    Returns:
        bool: True if the API key is valid, Exception if it is not.
    """
    if api_key not in API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return True


def verify_auto_alert(alert):
    """
    Verify before creation that an auto alert is valid.

    Checks for the following:
        - The alert criticality is valid.
        - The alert clearAfter is valid.
    """
    criticalities = [0, 1, 2]
    if alert.criticality not in criticalities:
        return False

    if alert.clearAfter < 0:
        return False

    if alert.group:
        return verify_group_exist(alert.group)

    return True


def verify_manual_alert(alert):
    """
    Verify before creation that a manual alert is valid.

    Checks for the following:
        - The alert daysNotice is valid.
    """
    if alert.daysNotice < 0:
        return False

    if alert.message == "":
        return False

    if alert.group:
        return verify_group_exist(alert.group)

    return True


def calc_criticality(day_diff, days_notice):
    """
    Calculate the criticality of an alert based on the days until the alert is due.

    Parameters:
        day_diff (int): The number of days until the alert is due.
        days_notice (int): The number of days the alert will be shown before it is due.

    Returns:
        int: The criticality of the alert. (0: Critical, 1: Warning, or 2: Info)
    """
    CRITICALITIES = {0.2: 0, 0.5: 1, 1: 2}

    percentage = day_diff / days_notice

    for key in CRITICALITIES:
        if percentage <= key:
            return CRITICALITIES[key]

    return 0


def verify_group_exist(groupName):
    """
    Verify that a group exists.

    Parameters:
        groupName (str): The name of the group.

    Returns:
        bool: True if the group exists, False if it does not.
    """
    group = GroupModel.get_or_none(GroupModel.name == groupName)
    if not group:
        return False
    return True
