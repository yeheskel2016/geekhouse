from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'testingidc'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///geekhouse6.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # this will silence the warning

db = SQLAlchemy(app)
login_manager = LoginManager(app)

from geekhouse import models, routes, forms  # This should come at the end