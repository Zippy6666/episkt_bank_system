from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy



"""In Flask, migrating refers to the process of applying changes to your database schema using a tool like Flask-Migrate in
conjunction with SQLAlchemy. When you develop a web application, your database schema might evolve as you add new features,
modify existing ones, or refactor your models."""
from flask_migrate import Migrate, upgrade



from models import db
 


 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@localhost/lennartbladhfuktig'
 
db.app = app
db.init_app(app)
migrate = Migrate(app, db)
 

def seed_data():
    """Don't do this every run or you will get more and more data the more you run it"""
    pass


"""In Flask, the index function is typically associated with the root URL /.
While you can put a lot of functionality into the index function, it's not necessary to confine everything to that function alone.
Flask uses routing, allowing you to define different functions for different URLs.
The index function often serves as the entry point or the landing page of your website."""
@app.route('/')
def index():
    return "Hej"
 
 
if __name__ == '__main__':
    with app.app_context():
        # Database upgrade
        upgrade()
   
    app.run(debug=True)