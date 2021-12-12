import os
from flask import Flask, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_admin import Admin, AdminIndexView
from grocery.config import DevConfig, ProdConfig, TestConfig




bcrypt = Bcrypt()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view='userbp.login'
login_manager.login_message = 'Please login to get the requested page'
login_manager.login_message_category = 'info'
mail = Mail()

# Admin Page Control View
class AdminPageView(AdminIndexView):
    def is_accessible(self):
        if 'admin_logged_in' in session:
            return True
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('userbp.admin_login'))
admin = Admin(template_mode='bootstrap4', name='Admin Section', index_view=AdminPageView())



# Application Factory
def create_app(Dev=DevConfig,Prod=ProdConfig,Test=TestConfig):
    app = Flask(__name__)

    mode = os.environ.get('FLASK_ENV')
    if mode == "development":
        app.config.from_object(Dev)
    elif mode == "production":
        app.config.from_object(Prod)
    elif mode == "testing":
        app.config.from_object(Test)

    bcrypt.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    admin.init_app(app)

    # Blueprints
    from grocery.userbp.routes import userbp
    from grocery.main.routes import main
    from grocery.errorbp.handlers import handlers
    from grocery.productOrders.routes import productOrders

    app.register_blueprint(userbp)
    app.register_blueprint(main)
    app.register_blueprint(handlers)
    app.register_blueprint(productOrders)

    return app




















