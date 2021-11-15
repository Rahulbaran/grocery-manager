import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from .config import DevConfig, ProdConfig, TestConfig




app = Flask(__name__)
mode = os.environ.get('FLASK_ENV')
if mode == "development":
    app.config.from_object(DevConfig)
elif mode == "production":
    app.config.from_object(ProdConfig)
elif mode == "testing":
    app.config.from_object(TestConfig)

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)


from . import routes









