# =====================================================================
# imports
# =====================================================================


import webbrowser, os
from enum import Enum
from flask import Flask, render_template, request, redirect, url_for
from models import db, Customer
from flask_migrate import Migrate, upgrade
from flask_login import login_required, LoginManager, UserMixin, login_user


# =====================================================================
# essential stuff
# =====================================================================


# app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:my-secret-pw@localhost:3306/bnk"
app.config["SECRET_KEY"] = os.environ.get('PRIVATE_KEY')


# login manager
login_manager = LoginManager(app)
login_manager.login_view = "login"


# db
db.app = app
db.init_app(app)


# migrate
migrate = Migrate(app, db)


# =====================================================================
# login
# =====================================================================


# user roles
class UserRole(Enum):
    CASHIER = 1
    ADMIN = 2


# user class
class User(UserMixin):
    def __init__(self, id:str, password:str, role:UserRole) -> None:
        self.id = id
        self._password = password
        self._role = role
    
    def authenticate( self, password ) -> bool:
        if password==self._password:
            return True
        else:
            return False


# test user database
users = {
    "bruh420@garbagemail.net":  User("bruh420@garbagemail.net", "123123123", UserRole.CASHIER)
}


# load user
@login_manager.user_loader
def load_user(user_id) -> User:
    return users[user_id]



# login page
@app.route("/login", methods=["GET", "POST"])
def login() -> str:
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # user email registered in database
        if email in users:
            user = users[email]
            authorized = user.authenticate(password) # check if password is correct

            if authorized:
                print(email, user, authorized)
                login_user(user) # login
                return redirect(url_for('index')) # to homepage
    

    return render_template('login.html')


# =====================================================================
# index
# =====================================================================


# first page, needs login
@app.route("/")
@login_required
def index() -> str:
    return render_template("index.html", dollars=69)


# =====================================================================
# misc
# =====================================================================


# customer test
@app.route("/customers")
def customers() -> str:
    all_customers = Customer.query.all()  # returns a python list of customers


# =====================================================================
# main
# =====================================================================


def main() -> None:
    with app.app_context():
        upgrade()

    webbrowser.open("http://127.0.0.1:5000/")
    app.run("127.0.0.1", port=5000)


if __name__ == "__main__":
    main()
