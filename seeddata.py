from faker import Faker
from models import Customer, Account, SuperUser, db
from app import app
from werkzeug.security import generate_password_hash


# =====================================================================
# seed
# =====================================================================


def fake_user( email, password, rolename ):
    user = SuperUser(email=email, password=generate_password_hash(password, method="sha256"), rolename=rolename)
    db.session.add(user)


def seed_data():
    fake = Faker()

    try:
        # Delete old data
        db.session.query(Account).delete()
        db.session.query(Customer).delete()
        db.session.query(SuperUser).delete()
        db.session.commit()

        for _ in range(1, 301):
            # customer
            city = fake.city()
            personnummer = str( fake.random_number(digits=10, fix_len=True) )
            kundnummer = str( fake.random_number(digits=12, fix_len=True) )
            name = fake.name()
            customer = Customer(city=city, personnummer=personnummer, kundnummer=kundnummer, name=name)

            # account for customer
            saldo = fake.random_number(digits=6)
            kontonummer = str( fake.random_number(digits=12, fix_len=True) )
            account = Account(customer=customer, saldo=saldo, kontonummer=kontonummer)

            db.session.add(customer)
            db.session.add(account)
        
        # seed users
        fake_user( "bruh420@garbagemail.net", "123123123", "Admin" )
        fake_user( "stefan.holmberg@systementor.se", "Hejsan123#", "Admin" )
        fake_user( "stefan.holmberg@nackademin.se", "Hejsan123#", "Cashier" )

        # commit
        db.session.commit()

    except Exception as e:

        print(f"Error during data seed: {str(e)}")
        db.session.rollback()  # Rollback the transaction in case of an error

    else:

        print("Data seeded sucessfully!")



# =====================================================================
# main
# =====================================================================


if __name__ == "__main__":
    with app.app_context():
        seed_data()