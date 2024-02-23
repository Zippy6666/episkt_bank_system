# =====================================================================
# Imports
# =====================================================================


from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


# =====================================================================
# Models
# =====================================================================


db = SQLAlchemy()


# Bank customer, can be managed by the big dawgs
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    personnummer = db.Column(db.String(13), nullable=False, unique=True)
    name = db.Column(db.String(80), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    adress = db.Column(db.String(80), nullable=False)
    accounts = db.relationship("Account", backref="customer", lazy=True)


# Bank account for a customer
class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    saldo = db.Column(db.Numeric(10, 2), nullable=False)
    kontonummer = db.Column(db.String(20), nullable=False, unique=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    transactions = db.relationship("Transaction", backref="transaction", lazy=True)


# Transaction for a account
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    belopp = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(6), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=False)


# User, such as admin or cashier
class SuperUser(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(64), nullable=False)
    rolename = db.Column(db.String(80), nullable=False)
