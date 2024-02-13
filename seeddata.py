from faker import Faker
from models import Customer, Account, db
from app import app


# =====================================================================
# seed
# =====================================================================


    # Fake data
def seed_data():
    fake = Faker()

    try:
        # Delete old data
        db.session.query(Account).delete()
        db.session.query(Customer).delete()
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

        db.session.commit()  # Commit the remaining records

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