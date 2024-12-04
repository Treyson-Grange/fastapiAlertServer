from peewee import SqliteDatabase
from dotenv import load_dotenv

import os

load_dotenv()

db = SqliteDatabase(os.getenv("DB_PATH", "alerts.db"))
db.connect()
