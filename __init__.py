from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = 'testingidc'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///geekhouse10.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # this will silence the warning

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

from . import routes
