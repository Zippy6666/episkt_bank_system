# =====================================================================
# Imports
# =====================================================================


import webbrowser, os
from flask import Flask, render_template, request, redirect, url_for
from models import db, Customer, Account, SuperUser
from flask_migrate import Migrate, upgrade
from flask_login import login_required, LoginManager, login_user
from hashlib import sha256
from sqlalchemy import func


# =====================================================================
# Essentials
# =====================================================================


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:my-secret-pw@localhost:3306/bnk"
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

@login_manager.user_loader
def load_user(user_id: int) -> SuperUser:
    """Login manager load user"""
    return SuperUser.query.filter(SuperUser.id == user_id).first()


def get_user(email: str) -> SuperUser:
    """Gets user by email"""
    return SuperUser.query.filter(SuperUser.email == email).first()


def check_password(input_password, stored_hash):
    input_hash = sha256(input_password.encode()).hexdigest()
    return input_hash == stored_hash


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

    data = dict(
        info_kundid="Ingen kund vald",
        account_fetch_status="Ingen registrerad kund vald"
    )

    if request.method == "POST":
        id = request.form["kundid"]
        customer = get_customer(id)

        data["input_kundid"] = id  # keeps the id in the input field

        if customer is None:
            data["info_kundid"] = "Kund #" + id + " finns ej registrerad."
        else:
            data["info_kundid"] = "Kund #" + id + ": "+customer.name
            data["info_personnummer"] = "Personnummer: "+customer.personnummer
            data["info_city"] = "Stad: "+customer.city
            data["info_accounts"] = customer.accounts

            if len(customer.accounts) > 0:
                totsaldo = sum(a.saldo for a in Account.query.all())
                totsaldo = f"{totsaldo:,}"
                data["info_totsaldo"] = f"Totalt saldo: {totsaldo} SEK"

            data["account_fetch_status"] = len(customer.accounts) > 0 and ("Konton hittade för kund #" + id) or "Kunden har inga konton"

    # visa all info om kunden
    # visa alla konton för kunden
    # ex: konto 2: 6666 6666 6666 6666

    return render_template("kundbild.html", **data)


# =====================================================================
# Kundsökning
# =====================================================================


@app.route("/kundbild", methods=["GET", "POST"])
@login_required
def kundsokning():
    data = dict(
        # något = "något",
    )
    return render_template("kundbild.html", **data)


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

    webbrowser.open("http://127.0.0.1:5000/")
    app.run("127.0.0.1", port=5000)


if __name__ == "__main__":
    main()
