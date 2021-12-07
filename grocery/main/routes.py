from time import sleep
from flask import Blueprint, render_template, request, make_response
from flask_login import login_required, current_user
from grocery.models import Order




main = Blueprint('main', __name__)




@main.route('/')
@main.route('/home')
def home():
    if current_user.is_authenticated:
        userOrders = Order.query.filter_by(user_id=current_user.id).order_by(Order.order_date.desc()).limit(20).all()
        total = 0
        for order in userOrders:
            total += order.total
        return render_template('home.html', title='Home', userOrders=userOrders, total=total)
    else :
        return render_template('home.html', title='Home')





@main.route('/loadOrders')
@login_required
def loadOrders():
    counter = request.args.get("c")
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.order_date.desc()).offset(counter).limit(20).all()
    if len(orders):
        loadOrders = []
        totalPrice = 0
        for order in orders:
            loadOrder = {
                'customer' : order.customer,
                'date' : order.order_date.strftime('%d %b %Y'),
                'total' : order.total
            }
            totalPrice += order.total
            loadOrders.append(loadOrder)
        sleep(1//2)
        return {'orders': loadOrders, 'totalPrice' : totalPrice}
    else:
        return {'orders' : []}





@main.route('/contactUs')
def contactUs():
    headers = {'Content-Type' : 'text/html'}
    res = make_response(render_template('contact.html', title='Contact Us'),headers)
    res.set_cookie('theme', 'red', max_age=1000, path="/contactUs")
    return res




@main.route('/settings')
@login_required
def settings():
    return render_template('settings.html', title='User Settings')