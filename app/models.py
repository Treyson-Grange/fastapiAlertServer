from peewee import Model, CharField, IntegerField, BooleanField, DateTimeField
from app.database import db


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


class GroupModel(Model):
    name = CharField()
    description = CharField()

    class Meta:
        database = db


class APIKeyModel(Model):
    key = CharField(unique=True)
    client_name = CharField()
    is_active = BooleanField()
    permissions = (
        CharField()
    )  # Comma separated list of permissions E.g. "read,write,delete"
    # service to service api key, won't expire.

    class Meta:
        database = db
