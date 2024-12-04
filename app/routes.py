from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, timedelta, timezone
from app.models import AlertModel, ManualAlertModel, GroupModel, APIKeyModel
from app.schemas import Alert, ManualAlert, ApiAlerts
from app.utils import (
    verify_auto_alert,
    calc_criticality,
    verify_manual_alert,
    verify_group_exist,
    verify_api_key,
    
)
import logging, os

logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.DEBUG)

alert_router = APIRouter()


@alert_router.get("/alerts", dependencies=[Depends(verify_api_key("read"))])
def get_all_alerts(group: str = None):
    """
    Given a group, return all alerts for that group.

    Returns:
        List of auto and manual alerts for the group.
    """
    if group is None:
        group = os.getenv("DEFAULT_GROUP")

    if not verify_group_exist(group):  # Check if group exists
        raise HTTPException(status_code=400, detail="Group does not exist")

    today = datetime.now(timezone.utc)
    all_alerts = []
    alerts = (
        AlertModel.select()
        .where(AlertModel.group == group)
        .order_by(AlertModel.criticality.asc(), AlertModel.timestamp.desc())
    )
    for alert in alerts:
        if alert.autoClear:
            timestamp = datetime.strptime(alert.timestamp, "%Y-%m-%d %H:%M:%S.%f%z")
            if timestamp + timedelta(minutes=alert.clearAfter) < today:
                alert.delete_instance()
                continue
        a = ApiAlerts(
            id=alert.id,
            message=alert.message,
            criticality=alert.criticality,
            timestamp=alert.timestamp,
        )
        all_alerts.append(a)

    manual_alerts = (
        ManualAlertModel.select()
        .where(ManualAlertModel.group == group if group else True)
        .order_by(ManualAlertModel.dueDate.asc())
    )

    for manual_alert in manual_alerts:
        due_date = datetime.fromisoformat(manual_alert.dueDate.replace("Z", "+00:00"))

        if due_date.tzinfo is None:
            due_date = due_date.replace(tzinfo=timezone.utc)

        if due_date - timedelta(days=manual_alert.daysNotice) < today:
            total_days_diff = (due_date - today).days
            if due_date > today:
                to_add = ApiAlerts(
                    id=manual_alert.id,
                    type="manual",
                    message=manual_alert.message,
                    criticality=calc_criticality(
                        total_days_diff, manual_alert.daysNotice
                    ),
                    timestamp=manual_alert.dueDate,
                    days=total_days_diff,
                )
                all_alerts.append(to_add)
            else:
                manual_alert.delete_instance()

    all_alerts.sort(key=lambda x: (x.criticality, x.timestamp))

    return all_alerts


@alert_router.post("/create", dependencies=[Depends(verify_api_key("write"))])
def create_alert(alert: Alert):
    """
    Create an auto alert, given an alert object.

    Parameters:
        alert: Alert object.

    Returns:
        Alert object when successful, error message when not.

    """
    if not verify_auto_alert(alert):
        raise HTTPException(status_code=400, detail="Invalid alert")

    if not verify_group_exist(alert.group):
        raise HTTPException(status_code=400, detail="Group does not exist")

    try:
        alert = AlertModel.create(
            message=alert.message,
            criticality=alert.criticality,
            autoClear=alert.autoClear,
            timestamp=alert.timestamp,
            clearAfter=alert.clearAfter,
            group=alert.group,
        )
        return {
            "id": alert.id,
            "message": alert.message,
            "criticality": alert.criticality,
            "autoClear": alert.autoClear,
            "timestamp": alert.timestamp,
            "clearAfter": alert.clearAfter,
            "group": alert.group,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@alert_router.post("/create-manual", dependencies=[Depends(verify_api_key("write"))])
def create_manual_alert(manual_alert: ManualAlert):
    """
    Create a manual alert, given a manual alert object.

    Parameters:
        manual_alert: ManualAlert object.

    Returns:
        ManualAlert object when successful, error message when not.
    """
    if not verify_manual_alert(manual_alert):
        raise HTTPException(status_code=400, detail="Invalid alert")

    if not verify_group_exist(manual_alert.group):
        raise HTTPException(status_code=400, detail="Group does not exist")

    try:
        manual_alert = ManualAlertModel.create(
            dueDate=manual_alert.dueDate,
            daysNotice=manual_alert.daysNotice,
            message=manual_alert.message,
            group=manual_alert.group,
        )
        return {
            "id": manual_alert.id,
            "dueDate": manual_alert.dueDate,
            "daysNotice": manual_alert.daysNotice,
            "message": manual_alert.message,
            "group": manual_alert.group,
        }
    except Exception as e:
        return {"error": str(e)}


@alert_router.post("/delete/{alert_id}", dependencies=[Depends(verify_api_key("delete"))])
def delete_alert(alert_id: int):
    """
    Delete an auto alert, given an alert ID.

    Parameters:
        alert_id: int

    Returns:
        Message when successful, error message when not.
    """
    try:
        alert = AlertModel.get(AlertModel.id == alert_id)
        alert.delete_instance()
        return {"message": "Alert " + str(alert_id) + " deleted"}
    except AlertModel.DoesNotExist:
        return {"error": "Alert not found"}
    except Exception as e:
        return {"error": str(e)}


@alert_router.post("/delete-manual/{alert_id}", dependencies=[Depends(verify_api_key("delete"))])
def delete_manual_alert(alert_id: int):
    """
    Delete a manual alert, given a manual alert ID.

    Parameters:
        alert_id: int

    Returns:
        Message when successful, error message when not.
    """
    try:
        alert = ManualAlertModel.get(ManualAlertModel.id == alert_id)
        alert.delete_instance()
        return {"message": "Alert " + str(alert_id) + " deleted"}
    except ManualAlertModel.DoesNotExist:
        return {"error": "Alert not found"}
    except Exception as e:
        return {"error": str(e)}


# Endpoints for testing purposes only


@alert_router.get("/all")
def get_all_alerts():
    """
    Get all alerts, regardless of group.
    """
    all_alerts = []
    alerts = AlertModel.select()
    for alert in alerts:
        a = ApiAlerts(
            id=alert.id,
            message=alert.message,
            criticality=alert.criticality,
            timestamp=alert.timestamp,
        )
        all_alerts.append(a)

    manual_alerts = ManualAlertModel.select()

    for manual_alert in manual_alerts:
        to_add = ApiAlerts(
            id=manual_alert.id,
            type="manual",
            message=manual_alert.message,
            criticality=0,
            timestamp=manual_alert.dueDate,
        )
        all_alerts.append(to_add)

    all_alerts.sort(key=lambda x: (x.criticality, x.timestamp))

    return all_alerts


@alert_router.get("/groups")
def get_all_groups():
    """
    Retrieve a list of all groups.
    """
    groups = GroupModel.select()
    all_groups = []
    for group in groups:
        all_groups.append({"name": group.name, "description": group.description})
    return all_groups


@alert_router.get("/keys")
def get_all_keys():
    """
    Retrieve a list of all API keys
    """
    keys = APIKeyModel.select()
    all_keys = []
    for key in keys:
        all_keys.append(
            {
                "key": key.key,
                "client_name": key.client_name,
                "is_active": key.is_active,
                "permissions": key.permissions,
            }
        )
    return all_keys