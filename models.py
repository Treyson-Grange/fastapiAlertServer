from peewee import Model, CharField, IntegerField, BooleanField, DateTimeField
from database import db

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
