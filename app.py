# imports
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from models import db, Customer, seed_data
import webbrowser
from flask_migrate import Migrate, upgrade



# app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:my-secret-pw@localhost:3306/bnk'
 

# db
db.app = app
db.init_app(app)



# migrate
migrate = Migrate(app, db)
 


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/customers')
def customers():
    all_customers = Customer.query.all() # Returns a python list of customers


def main():
    


    # flask db migrate -m "description_of_changes"
    # flask db upgrade
    with app.app_context():
        seed_data()
        #upgrade()


    #webbrowser.open("http://127.0.0.1:5000/")
    #app.run("127.0.0.1", port=5000, debug=True)


if __name__ == '__main__':
    main()
