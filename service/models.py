# models.py
from peewee import Model, SmallIntegerField, IntegerField, DateField, FloatField

from .db import db


class Records(Model):
    iid = SmallIntegerField()
    order_id = IntegerField()
    cost_us = FloatField()
    cost_rus = FloatField()
    date = DateField()

    class Meta:
        database = db


if db.table_exists('records') is False:
    db.create_tables([Records])