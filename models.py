from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


    # Bank customer, can be managed by the big dawgs
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    saldo = db.Column(db.Float, nullable=False)
