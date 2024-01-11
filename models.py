from flask_sqlalchemy import SQLAlchemy
# from faker import Faker


db = SQLAlchemy()


# if shit hits the fan, do db.create_all()



# Bank customer, can be managed by the big dawgs
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # id = kundnummer
    city = db.Column(db.String(80), nullable=False)
    ssn = db.Column(db.Integer, nullable=False, unique=True)
    accounts = db.relationship("accounts", backref="account", lazy=True)



    # Bank account for a customer
class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True) # id = kontonummer
    saldo = db.Column(db.Float, nullable=False)
    customer = db.Column(db.Integer, db.ForeignKey("customer.id"))






"""
    # Fake data
def seed_data():
    if Customer.query.count() <= 0:
        fake = Faker()

        for _ in range(1000):
            city = fake.city()

            saldo = fake.random_number(digits=6)

            customer = Customer(city=city, saldo=saldo)
            db.session.add(customer)

        db.session.commit()  # Must be done in the end
"""