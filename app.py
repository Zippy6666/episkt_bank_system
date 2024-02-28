# =====================================================================
# Imports
# =====================================================================


from flask import Flask, render_template, request, redirect, url_for
from flask_migrate import Migrate, upgrade
from flask_login import login_required, LoginManager, login_user
from models import db, Customer, Account, SuperUser, Transaction
from hashlib import sha256
from sqlalchemy import or_
from datetime import datetime
from enum import Enum
from seeddata import seed_data
from decimal import Decimal
import os


# =====================================================================
# Essentials
# =====================================================================


app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "mysql+mysqlconnector://root:my-secret-pw@localhost:3306/bnk"
app.config["SECRET_KEY"] = os.environ.get("LoginSecretKey")

login_manager = LoginManager(app)
login_manager.login_view = "login"

db.app = app
db.init_app(app)

migrate = Migrate(app, db)


# =====================================================================
# Enums
# =====================================================================


class TransactionResultMessage(Enum):
    NOT_FOUND = "Transaction failed: Account not found"
    INSUFFICIENT_FUNDS = "Transaction failed: Account does not have enough funds to complete the transaction!"
    UNKNOWN = "Transaction failed: Unknown error."
    SUCCESS = "Transaction success: Successfully completed the transaction!"
    FORBIDDEN = "Transaction error: Forbidden transfer!"
    LESS_THAN_ZERO = "Transaction error: Input must be more than 0!"
    DB_ERROR = "Transaction error: Database commit error."


# =====================================================================
# Services
# =====================================================================


def get_customer(id: int) -> Customer:
    """Aquire customer from database by ID."""
    return Customer.query.filter(Customer.id == id).first()


def get_account(id: int) -> Account:
    """Aquire account from database by ID."""
    return Account.query.filter(Account.id == id).first()


def get_account_by_nr(nr: str) -> Account:
    """Aquire account from database by account number."""
    return Account.query.filter(Account.kontonummer == nr).first()


@login_manager.user_loader
def load_user(user_id: int) -> SuperUser:
    """Login manager load user"""
    return SuperUser.query.filter(SuperUser.id == user_id).first()


def get_user(email: str) -> SuperUser:
    """Gets user by email"""
    return SuperUser.query.filter(SuperUser.email == email).first()


def check_password(input_password: str, stored_hash: str) -> bool:
    """Password check"""
    input_hash = sha256(input_password.encode()).hexdigest()
    return input_hash == stored_hash


def customer_search(
    search_str: str, sort_by: str = "id", sort_direction: str = "asc", page: int = 1
):
    """Searches for a customer by string, and also handles sorting and paginating the search."""
    str_in_name = Customer.name.ilike(f"%{search_str}%")
    str_in_city = Customer.city.ilike(f"%{search_str}%")

    query = Customer.query.filter(or_(str_in_name, str_in_city))

    match sort_by:
        case "id":
            column = Customer.id
        case "name":
            column = Customer.name
        case "personnummer":
            column = Customer.personnummer
        case "city":
            column = Customer.city
        case "adress":
            column = Customer.adress

    if sort_direction == "desc":
        query = query.order_by(column.desc())
    else:
        query = query.order_by(column.asc())

    return query.paginate(page=page, per_page=49), query.count()


def transaction(
    amt: float, account: Account, is_transfer: bool = False
) -> tuple[str, bool]:
    """Do a transaction for an account. Returns a response message, and a bool letting us know if the transaction succeded."""

    b_uttag = amt < 0  # amt < 0 = It's a withrawal

    # Account not found
    if not account:
        return TransactionResultMessage.NOT_FOUND.value, False

    # Trying to withdraw/transfer too much
    if b_uttag and -amt > account.saldo:
        return (
            TransactionResultMessage.INSUFFICIENT_FUNDS.value,
            False,
        )

    try:
        # Saldo change
        account.saldo += amt

        # Add new transaction to session
        transaction_ = Transaction(
            account_id=account.id,
            timestamp=datetime.now(),
            type=(is_transfer and "ÖVER") or (b_uttag and "UTTAG") or "INSÄTT",
            belopp=amt,
        )
        db.session.add(transaction_)
    except Exception as e:
        print(f"Error during transaction: {e}")
        return TransactionResultMessage.UNKNOWN.value, False

    return TransactionResultMessage.SUCCESS.value, True


def commit_transaction() -> bool:
    """Tries to commit to database, rolls back on fail. Was intended to be used during a transaction"""
    try:
        db.session.commit()
        return True
    except Exception:
        db.session.rollback()
        return False


# =====================================================================
# Login
# =====================================================================


# login page
@app.route("/login", methods=["GET", "POST"])
def login() -> str:
    """User login page"""
    errormsg = ""

    # Login post
    if request.method == "POST":
        email = request.form["email"]
        user = get_user(email)

        # User email registered in database
        if not user is None:
            password = request.form["password"]
            authorized = check_password(password, user.password)

            if authorized:
                login_user(user)  # Login
                return redirect(url_for("index"))  # Redirect to homepage
            else:
                errormsg = "The password is incorrect."

        else:
            errormsg = "This email is not registered in our database."

    return render_template("login.html", errormsg=errormsg)


# =====================================================================
# Index
# =====================================================================


@app.route("/")
@login_required
def index() -> str:
    """Homepage, shows statistics"""

    cquery = Customer.query  # customer query
    aquery = Account.query  # account query

    saldosum = sum(a.saldo for a in aquery.all())

    return render_template(
        "index.html",
        customercount=cquery.count(),
        accountcount=aquery.count(),
        saldosum=f"{saldosum:,}",
    )


# =====================================================================
# Kundbild
# =====================================================================


@app.route("/kundbild", methods=["GET", "POST"])
@login_required
def kundbild() -> str:
    """Kundbild"""

    force_id = request.args.get("id")
    data = dict(
        info_kundid="Ingen kund vald",
        account_fetch_status="Ingen registrerad kund vald",
        allow_input=force_id is None,
    )

    if request.method == "POST" or force_id:
        id = force_id or request.form["kundid"]

        if isinstance(id, str) and id.isnumeric():  # Input validation
            customer = get_customer(id)
            data["input_kundid"] = id

            if customer is None:
                # Let us know that the customer isn't registered in the database
                data["info_kundid"] = "Kund #" + id + " finns ej registrerad."
            else:
                # General info
                data["info_kundid"] = "Kund #" + id + ": " + customer.name
                data["info_personnummer"] = "Personnummer: " + customer.personnummer
                data["info_city"] = "Stad: " + customer.city
                data["info_accounts"] = customer.accounts

                # Calculate total saldo
                if len(customer.accounts) > 0:
                    totsaldo = sum(
                        a.saldo for a in Account.query.all() if a.customer_id == int(id)
                    )
                    totsaldo = f"{totsaldo:,}"
                    data["info_totsaldo"] = f"Totalt saldo: {totsaldo} SEK"

                # Let us know wheter or not the customer has any accounts
                data["account_fetch_status"] = (
                    len(customer.accounts) > 0
                    and ("Konton hittade för kund #" + id)
                    or "Kunden har inga konton"
                )

    return render_template("kundbild.html", **data)


# =====================================================================
# Kundsökning
# =====================================================================


@app.route("/kundsokning", methods=["GET", "POST"])
@login_required
def kundsokning() -> str:
    """Customer search."""
    data = dict(
        search_h1="Sökningsresultat för kundsökningen visas här.",
        results_count=0,
    )

    sort_by = request.args.get("sort_by")
    sort_direction = request.args.get("sort_direction", "asc")
    page = request.args.get("page")

    if isinstance(page, str):
        page = int(page)

    # Show table of customers if we should
    if request.method == "POST" or sort_by or page:
        search_str = (
            ("search-bar" in request.form and request.form["search-bar"])
            or request.args.get("searchword")
            or ""
        )
        data["searchbarval"] = search_str

        if len(search_str) > 0:
            results, results_count = customer_search(
                search_str, sort_by or "id", sort_direction, page or 1
            )

            if sort_direction == "asc":
                data["new_direction"] = "desc"
            else:
                data["new_direction"] = "asc"

            data["search_h1"] = (
                str(results_count) + " sökresultat för '" + search_str + "'"
            )
            data["results"] = results
            data["results_count"] = results_count
            data["page"] = page or 1

    return render_template("kundsearch.html", **data)


# =====================================================================
# Kontobild
# =====================================================================


@app.route("/kontobild", methods=["GET", "POST"])
@login_required
def kontobild() -> str:
    """Kontobild"""
    konto_id = request.args.get("id")
    account = get_account(konto_id)

    # New transaction
    transaction_msg = None
    if request.method == "POST":
        try:
            str_belopp = request.form.get("belopp")
            belopp = Decimal(str_belopp)
        except Exception as e:
            print(f"Error during input: {e}")
            transaction_msg = "Transaction error: Invalid input."
        else:
            if belopp > 0:
                transaction_type = request.form.get("transaction_type")
                transfer_accountnr = request.form.get("transfer_accountnr")

                # Set 'belopp' to a negative value if the transaction type is a withdrawal or transfer
                if transaction_type == "uttag" or transaction_type == "överför":
                    belopp = -belopp

                # Do transaction for this account
                transaction_msg, success = transaction(
                    belopp, account, transaction_type == "överför"
                )

                # Transfer, do a transaction for the recieving account as well
                if success and transaction_type == "överför":
                    receiving_account = get_account_by_nr(transfer_accountnr)

                    if account != receiving_account:
                        transfer_to_msg, success = transaction(
                            -belopp, receiving_account, True
                        )
                        transaction_msg = (
                            success
                            and transaction_msg
                            or "(RECEIVING END) " + transfer_to_msg
                        )
                    else:
                        # Cannot transfer to itself
                        transaction_msg = TransactionResultMessage.FORBIDDEN.value
                        success = False

                # Commit or rollback
                if success:
                    commit_success = commit_transaction()
                    if not commit_success:
                        transaction_msg = TransactionResultMessage.DB_ERROR.value
                else:
                    db.session.rollback()
            else:
                transaction_msg = TransactionResultMessage.LESS_THAN_ZERO.value

    data = dict(
        konto_id=konto_id,
        info_kontonummer=account.kontonummer,
        info_saldo=f"{account.saldo:,}",
        info_transactions=account.transactions,
        transaction_msg=transaction_msg or "",
        transaction_msg_type=(
            transaction_msg == TransactionResultMessage.SUCCESS.value and "sucesstext"
        )
        or "errortext",
    )

    return render_template("kontobild.html", **data)


# =====================================================================
# TOS/Privacy
# =====================================================================


@app.route("/terms-of-service")
def tos() -> str:
    """Terms of service"""
    return render_template("tos.html")


@app.route("/privacy-policy")
def privacy_policy() -> str:
    """Privacy policy"""
    return render_template("privacy-policy.html")


# =====================================================================
# Main
# =====================================================================


def main() -> None:
    with app.app_context():
        # UNCOMMENT TO CREATE TABLES
        # db.create_all()

        # Upgrade
        upgrade()

        # Seed
        if db.session.query(Customer).count() == 0:
            seed_data()

    app.run("127.0.0.1", port=5000, debug=True)


if __name__ == "__main__":
    main()
