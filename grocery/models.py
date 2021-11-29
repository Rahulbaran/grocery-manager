from datetime import datetime
from . import db, login_manager




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# model for new user 
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    avatar = db.Column(db.String(100),nullable=False,default='default.png')
    join_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    shopname = db.Column(db.String(200))
    location = db.Column(db.String(100))
    product = db.relationship('Product', backref="product_user", lazy='dynamic')
    order = db.relationship('Order', backref='order_user', lazy='dynamic')

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
        return f'User({self.name}, {self.email}, {self.shopname})'





# Model for new Product
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


    def __repr__(self):
        return f'Product({self.name} {self.unit} {self.price} {self.user_id})'




# Model for new order
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), nullable=False)
    product_name = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    product_unit = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def __repr__(self):
        return f'Order({self.customer},{self.product_name}, {self.total})'