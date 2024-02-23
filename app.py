# =====================================================================
# Imports
# =====================================================================


import webbrowser, os, threading
from flask import Flask, render_template, request, redirect, url_for
from flask_migrate import Migrate, upgrade
from flask_login import login_required, LoginManager, login_user
from models import db, Customer, Account, SuperUser, Transaction
from hashlib import sha256
from sqlalchemy import or_
from typing import Optional
from datetime import datetime


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
# Services
# =====================================================================


def get_customer(id: int) -> Customer:
    """Aquire customer from database by ID."""
    return Customer.query.filter(Customer.id == id).first()


def get_account(id: int) -> Account:
    """Aquire account from database by ID."""
    return Account.query.filter(Account.id == id).first()


@login_manager.user_loader
def load_user(user_id: int) -> SuperUser:
    """Login manager load user"""
    return SuperUser.query.filter(SuperUser.id == user_id).first()


def get_user(email: str) -> SuperUser:
    """Gets user by email"""
    return SuperUser.query.filter(SuperUser.email == email).first()


def check_password(input_password: str, stored_hash: str) -> bool:
    input_hash = sha256(input_password.encode()).hexdigest()
    return input_hash == stored_hash


def customer_search(
    search_str: str, sort_by: str = "id", sort_direction: str = "asc", page: int = 1
):
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

    return query.paginate(page=page, per_page=50), query.count()


def transaction(amt: float, from_: int, to_: Optional[int] = None) -> str:
    """Do a transaction for an account"""
    account_from = get_account(from_)
    b_uttag = amt < 0

    if not account_from:
        return "Transaction failed: Unknown error."

    if b_uttag and -amt > account_from.saldo:
        return "Transaction failed: Account does not have enough funds to complete the transaction!"

    try:
        # Saldo change
        account_from.saldo += amt

        # Register "from" transaction
        transaction_ = Transaction(
            account_id=from_,
            timestamp=datetime.now(),
            type=b_uttag and "UTTAG" or "INSÄTT",
            belopp=amt,
        )
        db.session.add(transaction_)

        db.session.commit()
    except Exception as e:
        print(f"Error during transaction: {e}")
        db.session.rollback()  # Rollback the transaction in case of an error
        return "Transaction failed: Unknown error."

    return f"Transaction success: Successfully completed the transaction!"


# =====================================================================
# Login
# =====================================================================


# login page
@app.route("/login", methods=["GET", "POST"])
def login() -> str:
    errormsg = ""

    # login post
    if request.method == "POST":
        email = request.form["email"]
        user = get_user(email)

        # user email registered in database
        if not user is None:
            password = request.form["password"]
            authorized = check_password(password, user.password)

            if authorized:
                login_user(user)  # login
                return redirect(url_for("index"))  # to homepage
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
    """First page, needs login"""

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
        customer = get_customer(id)

        data["input_kundid"] = id

        if customer is None:
            data["info_kundid"] = "Kund #" + id + " finns ej registrerad."
        else:
            data["info_kundid"] = "Kund #" + id + ": " + customer.name
            data["info_personnummer"] = "Personnummer: " + customer.personnummer
            data["info_city"] = "Stad: " + customer.city
            data["info_accounts"] = customer.accounts

            if len(customer.accounts) > 0:
                totsaldo = sum(
                    a.saldo for a in Account.query.all() if a.customer_id == int(id)
                )
                totsaldo = f"{totsaldo:,}"
                data["info_totsaldo"] = f"Totalt saldo: {totsaldo} SEK"

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
            "search-bar" in request.form and request.form["search-bar"]
        ) or request.args.get("searchword")
        data["searchbarval"] = search_str

        results, results_count = customer_search(
            search_str, sort_by or "id", sort_direction, page or 1
        )

        if sort_direction == "asc":
            data["new_direction"] = "desc"
        else:
            data["new_direction"] = "asc"

        data["search_h1"] = str(results_count) + " sökresultat för '" + search_str + "'"
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
    konto_id = request.args.get("id")

    # New transaction
    transaction_msg = None
    if request.method == "POST":
        belopp = float(request.form.get("belopp"))
        transaction_type = request.form.get("transaction_type")

        if transaction_type == "uttag" or transaction_type == "överför":
            belopp = -belopp

        transaction_msg = transaction(belopp, konto_id)

    account = get_account(konto_id)

    data = dict(
        konto_id=konto_id,
        info_kontonummer=account.kontonummer,
        info_saldo=f"{account.saldo:,}",
        info_transactions=account.transactions,
        transaction_msg=transaction_msg or "",
    )

    return render_template("kontobild.html", **data)


# =====================================================================
# TOS/Privacy
# =====================================================================


@app.route("/terms-of-service")
def tos() -> str:
    return render_template("tos.html")


@app.route("/privacy-policy")
def privacy_policy() -> str:
    return render_template("privacy-policy.html")


# =====================================================================
# Main
# =====================================================================


def main() -> None:
    # flask db migrate -m "Your migration message"
    # flask db upgrade

    with app.app_context():
        upgrade()

    if threading.current_thread() == threading.main_thread():
        webbrowser.open("http://127.0.0.1:5000/")

    app.run("127.0.0.1", port=5000, debug=True)


if __name__ == "__main__":
    main()
