import os
from flask import Flask, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_admin import Admin, AdminIndexView
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
login_manager.login_view='login'
login_manager.login_message = 'Please login to get the requested page'
login_manager.login_message_category = 'info'
mail = Mail(app)


# Admin Page Control View
class AdminPageView(AdminIndexView):
    def is_accessible(self):
        if 'admin_logged_in' in session:
            return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin_login'))

admin = Admin(app, template_mode='bootstrap4', name='Admin Section', index_view=AdminPageView())




from . import routes









