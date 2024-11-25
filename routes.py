from fastapi import APIRouter
from datetime import datetime, timedelta, timezone
from models import AlertModel, ManualAlertModel
from schemas import Alert, ManualAlert, ApiAlerts
from utils import verify_alert, calc_criticality
import logging

logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.DEBUG)

alert_router = APIRouter()

@alert_router.get("/alerts")
def get_all_alerts(group: str = None):
    all_alerts = []
    # Auto alerts
    if group:
        alerts = (
            AlertModel.select()
            .where(AlertModel.group == group)
            .order_by(AlertModel.criticality.asc(), AlertModel.timestamp.desc())
        )
        for alert in alerts:
            a = ApiAlerts(
                id=alert.id,
                message=alert.message,
                criticality=alert.criticality,
                timestamp=alert.timestamp,
            )
            all_alerts.append(a)
    else:
        return []

    # Manual alerts
    today = datetime.now()

    manual_alerts = (
        ManualAlertModel.select()
        .where(ManualAlertModel.group == group if group else True)
        .order_by(ManualAlertModel.dueDate.asc())
    )

    for manual_alert in manual_alerts:
        due_date = datetime.fromisoformat(manual_alert.dueDate.replace("Z", "+00:00"))

        if due_date.tzinfo is None:
            due_date = due_date.replace(tzinfo=timezone.utc)

        today = datetime.now(timezone.utc)

        if due_date - timedelta(days=manual_alert.daysNotice) < today:
            total_days_diff = (due_date - today).days
            logger.debug(f"Total days diff: {total_days_diff}")
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

    # Then sort all alerts by timestamp
    all_alerts.sort(key=lambda x: x.timestamp, reverse=True)

    return all_alerts


@alert_router.get("/run-clean")
def run_clean():
    alerts = AlertModel.select().where(AlertModel.autoClear == True)
    for alert in alerts:
        timestamp = datetime.strptime(alert.timestamp, "%Y-%m-%d %H:%M:%S%z")
        if timestamp + timedelta(minutes=alert.clearAfter) < datetime.now(timezone.utc):
            alert.delete_instance()



@alert_router.post("/create")
def create_alert(alert: Alert):
    if not verify_alert(alert):
        return {"error": "Invalid alert"}
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
        return {"error": str(e)}



@alert_router.post("/create-manual")
def create_manual_alert(manual_alert: ManualAlert):
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




@alert_router.post("/delete/{alert_id}")
def delete_alert(alert_id: int):
    try:
        alert = AlertModel.get(AlertModel.id == alert_id)
        alert.delete_instance()
        return {"message": "Alert " + str(alert_id) + " deleted"}
    except AlertModel.DoesNotExist:
        return {"error": "Alert not found"}
    except Exception as e:
        return {"error": str(e)}


@alert_router.post("/delete-manual/{alert_id}")
def delete_manual_alert(alert_id: int):
    try:
        alert = ManualAlertModel.get(ManualAlertModel.id == alert_id)
        alert.delete_instance()
        return {"message": "Alert " + str(alert_id) + " deleted"}
    except ManualAlertModel.DoesNotExist:
        return {"error": "Alert not found"}
    except Exception as e:
        return {"error": str(e)}
