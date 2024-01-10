from flask_sqlalchemy import SQLAlchemy
from faker import Faker


db = SQLAlchemy()


    # Bank customer, can be managed by the big dawgs
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(80), nullable=False)
    saldo = db.Column(db.Float, nullable=False)




def seed_data():
    if Customer.query.count() <= 0:

        fake = Faker()

        for _ in range(3):
            city = fake.city()

            saldo = fake.random_number(digits=6)

            customer = Customer(city=city, saldo=saldo)
            db.session.add(customer)

        db.session.commit() # Must be done in the end