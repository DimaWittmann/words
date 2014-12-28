from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
import flask_sijax

app = Flask(__name__)
app.config.from_object('config')

flask_sijax.Sijax(app)

db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

