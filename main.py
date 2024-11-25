#!/usr/bin/env python

from datetime import datetime, timedelta, timezone

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import logging

from peewee import *

db = SqliteDatabase("alerts.db")
db.connect()

logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.DEBUG)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AlertModel(Model):
    message = CharField()
    criticality = IntegerField()
    autoClear = BooleanField()
    timestamp = DateTimeField()
    clearAfter = IntegerField()
    group = CharField()

    class Meta:
        database = db


class ManualAlertModel(Model):
    dueDate = DateTimeField()
    daysNotice = IntegerField()
    message = CharField()
    group = CharField()

    class Meta:
        database = db


class Alert(BaseModel):
    message: str
    criticality: int
    autoClear: bool
    timestamp: datetime
    clearAfter: int
    group: str


class ManualAlert(BaseModel):
    dueDate: datetime
    daysNotice: int
    message: str
    group: str


class ApiAlerts(BaseModel):
    id: int = None
    type: str = "auto"
    message: str
    criticality: int
    timestamp: datetime
    days: int = None


def verify_alert(alert: Alert):
    criticalities = [0, 1, 2]
    if alert.criticality not in criticalities:
        return False

    if alert.clearAfter < 0:
        return False

    return True


@app.get("/alerts")
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


def calc_criticality(day_diff, days_notice):
    percentage = day_diff / days_notice

    CRITICALITIES = {0: 2, 0.5: 1, 0.8: 0}

    for key in CRITICALITIES:
        if percentage <= key:
            return CRITICALITIES[key]

    return 0


# Realistically, we will have this scheduled, with cron or whatever.
@app.get("/run-clean")
def run_clean():
    alerts = AlertModel.select().where(AlertModel.autoClear == True)
    for alert in alerts:
        timestamp = datetime.strptime(alert.timestamp, "%Y-%m-%d %H:%M:%S%z")
        if timestamp + timedelta(minutes=alert.clearAfter) < datetime.now(timezone.utc):
            alert.delete_instance()


@app.post("/create")
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


@app.post("/create-manual")
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


@app.get("/delete/{alert_id}")  # Should be a post, but for testing, we use get.
def delete_alert(alert_id: int):
    try:
        alert = AlertModel.get(AlertModel.id == alert_id)
        alert.delete_instance()
        return {"message": "Alert " + str(alert_id) + " deleted"}
    except AlertModel.DoesNotExist:
        return {"error": "Alert not found"}
    except Exception as e:
        return {"error": str(e)}


@app.get("/delete-manual/{alert_id}")
def delete_manual_alert(alert_id: int):
    try:
        alert = ManualAlertModel.get(ManualAlertModel.id == alert_id)
        alert.delete_instance()
        return {"message": "Alert " + str(alert_id) + " deleted"}
    except ManualAlertModel.DoesNotExist:
        return {"error": "Alert not found"}
    except Exception as e:
        return {"error": str(e)}


# Heres my idea. We want both of these alerts to be GETTED, so we we need a way to send them to the frontend in the same object.
# Needed on frontend: message, criticality, timestamp. The rest is not going to be passed along, they dont need to know about it.
# We will also need to calculate the criticality of the manual alerts, so we will do that in the get.
