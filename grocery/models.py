from datetime import datetime
from . import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# model for new user 
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    join_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    shopname = db.Column(db.String(200))


    # Methods to use flask_login package
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def is_authenticated(self):
        return True
    def get_id(self):
        return self.id



    def __repr__(self):
        return f'User - [{self.name}, {self.email}, {self.shopname}]'

