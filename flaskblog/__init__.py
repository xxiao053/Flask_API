from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_bcrypt import Bcrypt
# from flask_login import LoginManager

app = Flask(__name__)  # Flask is a class, create an instance 
app.config['SECRET_KEY'] = 'c765149c9618cedc66ff06f71b2fc50f' # protect our sever from attack 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blogsite.db'  # SQLlite, or PostgreSQL, or...
# db = SQLAlchemy(app)  # OMR, map table to python class 
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], future=True)  # Core
bcrypt = Bcrypt(app)  # for password authentication 
# login_manager = LoginManager(app)

from flaskblog import routes