from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from models import db # db stands for database ofc


"""In Flask, migrating refers to the process of applying changes to your database schema using a tool like Flask-Migrate in
conjunction with SQLAlchemy. When you develop a web application, your database schema might evolve as you add new features,
modify existing ones, or refactor your models."""

"""In the context of databases,
a migration refers to the management and application of changes to the structure of the database schema over time.
It's a way to version-control and apply alterations to the database structure without losing data."""
from flask_migrate import Migrate, upgrade



 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:my-secret-pw@localhost:3306/bnk'
 

db.app = app
db.init_app(app)




migrate = Migrate(app, db)
 



"""In Flask, the index function is typically associated with the root URL /.
While you can put a lot of functionality into the index function, it's not necessary to confine everything to that function alone.
Flask uses routing, allowing you to define different functions for different URLs.
The index function often serves as the entry point or the landing page of your website."""
@app.route('/')
def index():
    return render_template('index.html')
 
 
if __name__ == '__main__':
    with app.app_context():
        # Database upgrade
        # db.create_all()
        upgrade()
   
    #app.run(debug=True)
