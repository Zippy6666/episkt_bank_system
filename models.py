from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


    # Bank customer, can be managed by the big dawgs
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.Integer, nullable=False)
    saldo = db.Column(db.Float, nullable=False)
