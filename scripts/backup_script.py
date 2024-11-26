#!/usr/bin/env python3

import shutil
from pathlib import Path


def backup_database():
    """
    Copies alerts.db to alerts.db.bak in the same directory.
    """
    db_file = Path("alerts.db")
    backup_file = Path("alerts.db.bak")

    if db_file.exists():
        try:
            shutil.copy2(db_file, backup_file)
            print(f"Backup created: {backup_file}")
        except Exception as e:
            print(f"Error during backup: {e}")
    else:
        print(f"{db_file} does not exist. Backup not performed.")


if __name__ == "__main__":
    backup_database()
