# =====================================================================
# imports
# =====================================================================


from flask_sqlalchemy import SQLAlchemy


# =====================================================================
# models
# =====================================================================


db = SQLAlchemy()


    # Bank customer, can be managed by the big dawgs
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kundnummer = db.Column(db.String(12), nullable=False, unique=True)
    personnummer = db.Column(db.String(10), nullable=False, unique=True)
    name = db.Column(db.String(80), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    accounts = db.relationship("Account", backref="customer", lazy=True)


    # Bank account for a customer
class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    saldo = db.Column(db.Float, nullable=False)
    kontonummer = db.Column(db.String(12), nullable=False, unique=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    transactions = db.relationship("Transaction", backref="transaction", lazy=True)


    # Transaction for a account
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    belopp = db.Column(db.Float, nullable=False)
    typ = db.Column(db.String(6), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=False)