# Just run this when you need to create the database.

from peewee import (
    SqliteDatabase,
)
import os
from main import AlertModel, ManualAlertModel

db = SqliteDatabase(os.getenv('DB_PATH'))

db.connect()

db.create_tables([AlertModel, ManualAlertModel], safe=True)
