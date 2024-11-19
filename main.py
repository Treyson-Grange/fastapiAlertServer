#!/usr/bin/env python

from datetime import datetime, timedelta, timezone


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from peewee import *

db = SqliteDatabase('alerts.db')
db.connect()

# db.create_tables([AlertModel], safe=True)# uncomment this line to create table.

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
    
    class Meta:
        database = db
    

class Alert(BaseModel):
    message: str
    criticality: int
    autoClear: bool
    timestamp: datetime
    clearAfter: int
    
    
def verify_alert(alert: Alert):
    crits = [0,1,2]
    if alert.criticality not in crits:
        return False
    
    if alert.clearAfter < 0:
        return False
    
    return True
    
@app.get("/")
def get_alerts():
    alerts = AlertModel.select().order_by(AlertModel.criticality.asc(), AlertModel.timestamp.desc())
    return [
        { 
            "id": alert.id,
            "message": alert.message,
            "criticality": alert.criticality,
            "autoClear": alert.autoClear,
            "timestamp": alert.timestamp,
            "clearAfter": alert.clearAfter,
        }
        for alert in alerts
    ]
    
# Realistically, we will have this scheduled, with cron or whatever.
@app.get("/run-clean")
def run_clean():
    alerts = AlertModel.select().where(AlertModel.autoClear == True)
    for alert in alerts:
        timestamp = datetime.strptime(alert.timestamp, '%Y-%m-%d %H:%M:%S%z')
        print(timestamp + timedelta(minutes=alert.clearAfter))
        print(datetime.now(timezone.utc))
        if timestamp + timedelta(minutes=alert.clearAfter) < datetime.now(timezone.utc):
            alert.delete_instance()

    
@app.post("/create")
def create_alert(alert: Alert):
    if not verify_alert(alert):
        return {
            "error": "Invalid alert"
        }
    try:        
        alert = AlertModel.create(
            message=alert.message,
            criticality=alert.criticality,
            autoClear=alert.autoClear,
            timestamp=alert.timestamp,
            clearAfter=alert.clearAfter,
        )
        return {
            "id": alert.id,
            "message": alert.message,
            "criticality": alert.criticality,
            "autoClear": alert.autoClear,
            "timestamp": alert.timestamp,
            "clearAfter": alert.clearAfter,
        }
    except Exception as e:
        return {
            "error": str(e)
        }
    
@app.get("/delete/{alert_id}")
def delete_alert(alert_id: int):
    try:
        alert = AlertModel.get(AlertModel.id == alert_id)
        alert.delete_instance()
        return {
            "message": "Alert " + str(alert_id) + " deleted"
        }
    except AlertModel.DoesNotExist: 
        return {
            "error": "Alert not found"
        }
    except Exception as e:
        return {
            "error": str(e)
        }