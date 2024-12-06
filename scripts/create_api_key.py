import sys
import uuid
from peewee import SqliteDatabase
from app.models import APIKeyModel


def create_api_key(client_name, permissions):
    """
    Create a new API key with the given client name and permissions.
    """
    api_key = uuid.uuid4().hex + uuid.uuid4().hex  # 64 characters
    return {"api_key": api_key, "client_name": client_name, "permissions": permissions}


def main():
    if len(sys.argv) != 4:
        print(
            "Usage: python create_api_key.py <api_key> <client_name> <perm1,perm2,perm3>"
        )
        sys.exit(1)

    api_key = sys.argv[1]
    client_name = sys.argv[2]
    permissions = sys.argv[3]

    db = SqliteDatabase("alerts.db")
    db.connect()

    APIKeyModel.create(
        key=api_key, client_name=client_name, is_active=True, permissions=permissions
    )

    db.close()

    print("API Key created successfully!")


if __name__ == "__main__":
    main()
