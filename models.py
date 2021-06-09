from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

i = 0


def mydefault():
    global i
    i += 1
    return i


class BookModel(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer())
    currency = db.Column(db.String(80))
    description = db.Column(db.Text)
    shop_order_id = db.Column(db.Integer, unique=True)
    created_at = db.Column(db.DateTime(), default=datetime.now())

    def __init__(self, amount, currency, description):
        self.amount = amount
        self.currency = currency
        self.description = description
        self.shop_order_id = mydefault()

    def json(self):
        return {"amount": self.amount,
                "currency": self.currency,
                "description": self.description,
                "shop_order_id": self.shop_order_id,
                "created_at": self.created_at}
