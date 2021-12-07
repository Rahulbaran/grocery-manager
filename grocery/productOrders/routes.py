from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from grocery import db
from grocery.models import Order, Product




productOrders = Blueprint('productOrders', __name__)





@productOrders.route('/products')
@login_required
def products():
    allProducts = Product.query.filter_by(user_id=current_user.id).all()
    return render_template('products.html', title='Manage Products', allProducts=allProducts)





@productOrders.route('/getProducts', methods=["POST"])
@login_required
def getProducts():
    productsData = request.get_json()
    newProducts = productsData.get('products')
    if newProducts:
        totalProducts,alreadyExistProducts = 0,0
        for prod in newProducts:
            product = Product.query.filter_by(user_id=current_user.id,name=prod[0]).first()
            if not product:
                totalProducts += 1
                newProduct = Product(name=prod[0], unit=prod[1], price=prod[2], product_user=current_user)
                db.session.add(newProduct)
            else : 
                alreadyExistProducts += 1
        db.session.commit()
        resProductsData = Product.query.filter_by(user_id=current_user.id).order_by(Product.id.desc()).limit(totalProducts).all()
        resProducts = list()
        for resProduct in resProductsData:
            resProducts.append([resProduct.id,resProduct.name,resProduct.unit,resProduct.price])
        resProducts.reverse()
        return {'newProducts' : resProducts, 'alreadyExistProducts' : alreadyExistProducts}





@productOrders.route('/removeProduct', methods=["POST"])
@login_required
def removeProduct():
    productId = request.get_json().get('id')
    try:
        product = Product.query.get_or_404(productId)
        db.session.delete(product)
        db.session.commit()
        return 'OK'
    except ConnectionError as ConError:
        raise ConError('Something went wrong')





@productOrders.route('/orders')
@login_required
def orders():
    allProducts = Product.query.filter_by(user_id=current_user.id).all()
    allOrders = Order.query.filter_by(user_id=current_user.id).all()
    return render_template('orders.html', title='Manage Orders', allProducts=allProducts, allOrders=allOrders)





@productOrders.route('/getProductDetails', methods=["POST"])
@login_required
def getProductDetails():
    productName =request.get_json().get('name');
    prod = Product.query.filter_by(name=productName, user_id=current_user.id).first()
    if prod :
        return {'unit' : prod.unit, 'price' : prod.price}
    else :
        return {'message' : 'No product available'}





@productOrders.route('/getOrders', methods=["POST"])
@login_required
def getOrders():
    ordersData = request.get_json()
    customer = ordersData.get('customer')
    orders = ordersData.get('orders')
    perfectOrders = 0
    if customer and orders:
        for o in orders:
            if o[1] and o[3]:
                perfectOrders += 1
                order = Order (
                    customer=customer, 
                    product_name=o[0],
                    quantity=o[2], 
                    product_unit=o[1],
                    total=o[3],
                    order_user=current_user
                    )
                db.session.add(order)
        db.session.commit()
    response = Order.query.filter_by(user_id=current_user.id).order_by(Order.id.desc()).limit(perfectOrders).all()
    resOrders = list()
    for res in response:
        resOrders.append([
                res.id,
                res.customer,
                res.product_name,
                res.quantity,
                res.product_unit,
                res.total,
                res.order_date.strftime('%d %b %Y')
            ])
    resOrders.reverse()
    return {'orders' : resOrders}





@productOrders.route('/removeOrder', methods=["POST"])
@login_required
def removeOrder():
    orderId = request.get_json().get('id')
    try:
        order = Order.query.get_or_404(orderId)
        db.session.delete(order)
        db.session.commit()
        return 'OK'
    except ConnectionError as ConError:
        raise ConError('Something went wrong')

