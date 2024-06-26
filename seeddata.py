from faker import Faker
from models import Customer, Account, SuperUser, Transaction, db
from hashlib import sha256
import random


# =====================================================================
# Seed
# =====================================================================


def till_personnummer(num: int) -> str:
    num = str(num)
    personnummer = f"{num[0:8]}-{num[8:12]}"
    return personnummer


def till_kontonummer(num: int) -> str:
    num = str(num)
    kontonummer = f"{num[0:4]} {num[4:8]} {num[8:12]} {num[12:16]}"
    return kontonummer


def create_user(email: str, password: str, rolename: str) -> None:
    pass_encoded = password.encode()
    passhash = sha256(pass_encoded).hexdigest()
    user = SuperUser(email=email, password=passhash, rolename=rolename)
    db.session.add(user)


def seed_data():
    fake = Faker()

    try:
        # Delete old data
        db.session.query(Transaction).delete()
        db.session.query(Account).delete()
        db.session.query(Customer).delete()
        db.session.query(SuperUser).delete()
        db.session.commit()

        for _ in range(1, 1001):
            # Customer
            city = fake.city()
            personnummer = till_personnummer(
                fake.random_number(digits=12, fix_len=True)
            )
            name = fake.name()
            adress = fake.street_address()
            customer = Customer(
                city=city, personnummer=personnummer, name=name, adress=adress
            )

            # Account for customer
            for _ in range(random.randint(0, 3)):
                saldo = fake.random_number(digits=6)
                kontonummer = till_kontonummer(
                    fake.random_number(digits=16, fix_len=True)
                )
                account = Account(
                    customer=customer, saldo=saldo, kontonummer=kontonummer
                )

                db.session.add(account)

            db.session.add(customer)

        # Seed users
        create_user("bruh420@garbagemail.net", "123123123", "Admin")
        create_user("stefan.holmberg@systementor.se", "Hejsan123#", "Admin")
        create_user("stefan.holmberg@nackademin.se", "Hejsan123#", "Cashier")

        # Commit
        db.session.commit()

    except Exception as e:
        print(f"Error during data seed: {e}")
        db.session.rollback()

    else:
        print("Data seeded sucessfully!")


# =====================================================================
# Main
# =====================================================================


if __name__ == "__main__":
    from app import app

    with app.app_context():
        seed_data()
