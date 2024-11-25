# Just run this when you need to create the database.

from peewee import (
    SqliteDatabase,
)
from main import AlertModel, ManualAlertModel

db = SqliteDatabase("alerts.db")

db.connect()

db.create_tables([AlertModel, ManualAlertModel], safe=True)
