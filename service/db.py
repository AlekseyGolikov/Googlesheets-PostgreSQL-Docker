# db.py
from peewee import PostgresqlDatabase

from . import settings

db = PostgresqlDatabase(
    settings.DATABASE['NAME'],
    user=settings.DATABASE['USER'],
    password=settings.DATABASE['PASSWORD'],
    host=settings.DATABASE['HOST'],
    port=settings.DATABASE['PORT']
)