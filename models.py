# =====================================================================
# imports
# =====================================================================


from flask_sqlalchemy import SQLAlchemy
from faker import Faker


# =====================================================================
# models
# =====================================================================


# if shit hits the fan, do db.create_all()


db = SQLAlchemy()


    # Bank customer, can be managed by the big dawgs
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(80), nullable=False)
    ssn = db.Column(db.Integer, nullable=False, unique=True)

    # relationship
    accounts = db.relationship("Account", backref="customer", lazy=True)


    # Bank account for a customer
class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    saldo = db.Column(db.Float, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)


    # Transaction for a account
# class Transaction(db.Model):
#     pass



# =====================================================================
# seed
# =====================================================================


    # Fake data
def seed_data():
    
    fake = Faker()


    if Customer.query.count() <= 0:

        for i in range(1, 301):

            # customer
            city = fake.city()
            ssn = fake.random_number(digits=9)
            customer = Customer(id=i, city=city, ssn=ssn)
            
            # account for customer
            saldo = fake.random_number(digits=6)
            account = Account(id=i, customer_id=customer.id, saldo=saldo)

            
            db.session.add(customer)
            db.session.add(account)


        db.session.commit()  # Must be done in the end