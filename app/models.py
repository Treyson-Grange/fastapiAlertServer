from peewee import Model, CharField, IntegerField, BooleanField, DateTimeField
from app.database import db
import datetime


class AlertModel(Model):
    # Descriptive message to be displayed in clients UI
    message = CharField()

    # Criticality of the alert
    criticality = IntegerField()

    # Whether or not the alert should be auto-cleared
    autoClear = BooleanField()

    # Initial timestamp of the alert
    timestamp = DateTimeField(default=datetime.datetime.now)

    # Time in minutes after which the alert should be auto-cleared
    clearAfter = IntegerField()

    # Group to which the alert belongs (TODO: This should be a foreign key to a group)+
    group = CharField()

    class Meta:
        database = db


class ManualAlertModel(Model):
    # Due date of the alert
    dueDate = DateTimeField()

    # Number of days before the due date that the alert should be displayed
    daysNotice = IntegerField()

    # Descriptive message to be displayed in clients UI
    message = CharField()

    # Group to which the alert belongs (TODO: This should be a foreign key to a group)
    group = CharField()

    class Meta:
        database = db


class GroupModel(Model):
    # Name of the group
    name = CharField()

    # Description of the group (unused)
    description = CharField()

    class Meta:
        database = db


class APIKeyModel(Model):
    # Unique key for the API client (64 characters)
    key = CharField(unique=True)

    # Name of the client
    client_name = CharField()

    # Whether or not the key is active
    is_active = BooleanField()

    # Comma separated list of permissions E.g. "read,write,delete"
    permissions = CharField()

    class Meta:
        database = db
