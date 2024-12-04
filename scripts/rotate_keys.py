import secrets
from peewee import SqliteDatabase
from app.models import APIKeyModel
import subprocess


def get_new_key():
    """
    Return a new key.
    """
    return secrets.token_urlsafe(64)


def update_bitwarden_key(item_id, new_key):
    """
    Ideally, all clients will store their API keys in the bitwarden.
    Ideally, all named identically, alert_box_api_key.
    """
    NAME = "alert_box_api_key"

    # ansible will need to do this, so  will use ansible stuff. See networkingweb-ansible
    # for ideas on how to do this.
    pass


def run_cli_command(command):
    """
    Run a command in the terminal via subprocess
    """
    result = subprocess.run(command, shell=True, capture_output=True)
    if result.returncode != 0:
        raise Exception(f"Error running command {command}: {result.stderr}")
    return result.stdout


def main():
    """
    Rotate all keys in the database.

    Rotating keys is the easy part, but you'll need to update the clients with the new keys.
    """
    db = SqliteDatabase("alerts.db")
    db.connect()

    keys = APIKeyModel.select()

    for key in keys:
        new_key = get_new_key()
        key.key = new_key
        key.save()
        print(f"Key {key.client_name}'s API key is now {key.key}")

    db.close()


if __name__ == "__main__":
    main()
