# Just run this when you need to create the database.

from peewee import (
    SqliteDatabase,
)
import os
from models import AlertModel, ManualAlertModel, GroupModel

db = SqliteDatabase(os.getenv("DB_PATH"))

db.connect()

db.create_tables([AlertModel, ManualAlertModel, GroupModel], safe=True)


# Seed the database
GroupModel.create(name="usuNetworking", description="USU IT Networking Team")
GroupModel.create(name="usuIT", description="USU IT Department")

db.close()
