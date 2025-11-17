from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text 
from flaskblog.models import sql_user, sql_post

app = Flask(__name__)  # Flask is a class, create an instance 
app.config['SECRET_KEY'] = 'c765149c9618cedc66ff06f71b2fc50f' # protect our sever from attack 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blogsite.db'  # SQLlite, or PostgreSQL, or...
# db = SQLAlchemy(app)  # OMR, map table to python class 
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], future=True)  # Core
def create_table(query):
    with engine.begin() as conn:
        conn.execute(text(query))
create_table(sql_user)
create_table(sql_post) 

from flaskblog import routes