from peewee import SqliteDatabase

db = SqliteDatabase("alerts.db")
db.connect()
