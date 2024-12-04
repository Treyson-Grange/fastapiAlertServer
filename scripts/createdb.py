from peewee import SqliteDatabase
from app.models import AlertModel, ManualAlertModel, GroupModel, APIKeyModel
from dotenv import load_dotenv
import os

load_dotenv()

ADMIN = "read,write,delete"
USER = "read"


def create_db():
    db = SqliteDatabase(os.getenv("DB_PATH"))
    db.connect()

    db.create_tables([AlertModel, ManualAlertModel, GroupModel, APIKeyModel], safe=True)

    GroupModel.create(name="usuNetworking", description="USU IT Networking Team")
    GroupModel.create(name="usuIT", description="USU IT Department")

    keys = os.getenv("ACCEPTED_KEYS").split(",")

    APIKeyModel.create(
        key=keys[0], client_name="NOC", is_active=True, permissions=ADMIN
    )
    APIKeyModel.create(
        key=keys[1], client_name="test", is_active=True, permissions=USER
    )

    db.close()


if __name__ == "__main__":
    create_db()
