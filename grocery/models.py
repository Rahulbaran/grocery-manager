from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

from flask_admin.contrib.sqla import ModelView
from grocery import db, login_manager, admin




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

    # Method to generate reset token
    def generate_token(self,expire_sec=600):
        s = Serializer(current_app.config['SECRET_KEY'], expire_sec)
        return s.dumps({'user_id' : self.id}).decode('utf-8')

    # Method to verify the token
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


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









# User View
class UserView (ModelView):
    page_size = 30
    can_delete = False
    can_edit = False
    can_create = False
    column_exclude_list = ['password', 'Avatar']
    column_serachable_list = ['name', 'username', 'email']
    column_filters = ['name', 'shopname', 'location']

# Product View
class ProductView (ModelView):
    can_delete = False
    can_edit = False
    can_create = False
    page_size = 30
    column_searchable_list = ['name','unit','price']
    column_filters = ['unit']

# Order View
class OrderView (ModelView):
    can_delete = False
    can_edit = False
    can_create = False
    column_searchable_list = ['customer', 'order_date']
    page_size = 40
    column_filters = ['customer', 'order_date']

admin.add_view(UserView(User,db.session))
admin.add_view(ProductView(Product,db.session))
admin.add_view(OrderView(Order,db.session))






