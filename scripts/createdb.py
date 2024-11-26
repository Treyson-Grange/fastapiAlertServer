from peewee import SqliteDatabase
import os
from app.models import AlertModel, ManualAlertModel, GroupModel


def create_db():
    db = SqliteDatabase(os.getenv("DB_PATH"))
    db.connect()

    db.create_tables([AlertModel, ManualAlertModel, GroupModel], safe=True)

    GroupModel.create(name="usuNetworking", description="USU IT Networking Team")
    GroupModel.create(name="usuIT", description="USU IT Department")

    db.close()


if __name__ == "__main__":
    create_db()
