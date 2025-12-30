import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)  # instantiate 
app.config['SECRET_KEY'] = 'c765149c9618cedc66ff06f71b2fc50f' # protect our sever from attack 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # absolute path of this file's folder
DB_PATH = os.path.join(BASE_DIR, "blogsite.db")
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'  
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], future=True)  # Core
db = SQLAlchemy(app)  # ORM(object-relational mapping)
bcrypt = Bcrypt(app)  # for password authentication (hash real password)
login_manager = LoginManager(app)

from flaskblog import routes  # when everytime I run this app, I need to register these routes, which means those decorators@ codes should be executed, so import script here
from flaskblog.services import task_service, payment_service