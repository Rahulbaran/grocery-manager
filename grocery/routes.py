import os, secrets, time
from PIL import Image
from flask import request, url_for, render_template, make_response, redirect, flash
from flask_login import login_user, logout_user, current_user, login_required
from . import app, bcrypt, db
from .form import RegistrationForm, LoginForm, UpdateAccountForm, UpdateGeneralDetailsForm
from .models import User, Product, Order




@app.route('/')
@app.route('/home')
def home():
    if current_user.is_authenticated:
        userOrders = Order.query.filter_by(user_id=current_user.id).order_by(Order.order_date.desc()).limit(20).all()
        total = 0
        for order in userOrders:
            total += order.total
        return render_template('home.html', title='Home', userOrders=userOrders, total=total)
    else :
        return render_template('home.html', title='Home')




@app.route('/loadOrders')
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
        time.sleep(1//2)
        return {'orders': loadOrders, 'totalPrice' : totalPrice}
    else:
        return {'orders' : []}
            




@app.route('/contactUs')
def contactUs():
    headers = {'Content-Type' : 'text/html'}
    res = make_response(render_template('contact.html', title='Contact Us'),headers)
    res.set_cookie('theme', 'red', max_age=1000, path="/contactUs")
    return res




@app.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        flash('You are already logged in','info')
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_pw=bcrypt.generate_password_hash(form.password.data)
        user = User(name=form.name.data, username=form.username.data, email=form.email.data, password=hash_pw)
        db.session.add(user)
        db.session.commit()
        flash(f'Congrats {form.name.data}, You have registered🎊', 'info')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register Here', form=form)





@app.route('/login', methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in','info')
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        emailUser = User.query.filter_by(email=form.emailOrUsername.data).first()
        usernameUser = User.query.filter_by(username=form.emailOrUsername.data).first()
        password = lambda original, pw: bcrypt.check_password_hash(original, pw) 

        if emailUser and password(emailUser.password, form.password.data):
            next = request.args.get('next')
            flash('Welcome back, You have logged in', 'info')
            login_user(emailUser, remember=form.remember_me.data)
            return redirect(next) if next else redirect(url_for('home'))
        elif usernameUser and password(usernameUser.password, form.password.data):
            flash('Welcome back, You have logged in', 'info')
            next = request.args.get('next')
            login_user(usernameUser, remember=form.remember_me.data)
            return redirect(next) if next else redirect(url_for('home'))
        else : 
            flash('Provided credentials doesn\'t match with our database', 'error')   

    return render_template('login.html', title='Login',form=form)





@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have logged out from the site', 'info')
    return redirect(url_for('home'))





@app.route('/products')
@login_required
def products():
    allProducts = Product.query.filter_by(user_id=current_user.id).all()
    return render_template('products.html', title='Manage Products', allProducts=allProducts)





@app.route('/getProducts', methods=["POST"])
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





@app.route('/removeProduct', methods=["POST"])
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





@app.route('/orders')
@login_required
def orders():
    allProducts = Product.query.filter_by(user_id=current_user.id).all()
    allOrders = Order.query.filter_by(user_id=current_user.id).all()
    return render_template('orders.html', title='Manage Orders', allProducts=allProducts, allOrders=allOrders)





@app.route('/getProductDetails', methods=["POST"])
@login_required
def getProductDetails():
    productName =request.get_json().get('name');
    prod = Product.query.filter_by(name=productName, user_id=current_user.id).first()
    if prod :
        return {'unit' : prod.unit, 'price' : prod.price}
    else :
        return {'message' : 'No product available'}





@app.route('/getOrders', methods=["POST"])
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
                order = Order(customer=customer, product_name=o[0],quantity=o[2], product_unit=o[1],total=o[3],order_user=current_user)
                db.session.add(order)
        db.session.commit()
    response = Order.query.filter_by(user_id=current_user.id).order_by(Order.id.desc()).limit(perfectOrders).all()
    resOrders = list()
    for res in response:
        resOrders.append([res.id,res.customer,res.product_name,res.quantity,res.product_unit,res.total,res.order_date.strftime('%d %b %Y')])
    resOrders.reverse()
    return {'orders' : resOrders}





@app.route('/removeOrder', methods=["POST"])
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





@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html', title='User Settings')





@app.route('/updateProfile', methods=["POST","GET"])
@login_required
def updateProfile():
    generalForm = UpdateGeneralDetailsForm()
    accountForm = UpdateAccountForm()
    if request.method == "GET":
        generalForm.name.data = current_user.name
        generalForm.shopName.data = current_user.shopname
        generalForm.location.data = current_user.location
        accountForm.username.data = current_user.username
        accountForm.email.data = current_user.email
    if accountForm.validate_on_submit():
        current_user.username = accountForm.username.data
        current_user.email = accountForm.email.data
        db.session.commit()
        flash('username and email address have been updated','info')
        return redirect(url_for('updateProfile'))
    return render_template('updateProfile.html', title='Update Profile', accountForm=accountForm, generalForm=generalForm)





def uploadFunc (pic):
    random_hex = secrets.token_hex(8)
    _,ext = os.path.splitext(pic.filename)
    mod_pic = random_hex + ext
    path = os.path.join(app.root_path,'static','user-images',mod_pic)

    size = (720,720)
    img = Image.open(pic)
    img.thumbnail(size)
    img.save(path)

    if current_user.avatar != 'default.png':
        os.remove(os.path.join(app.root_path,'static','user-images',current_user.avatar))

    return mod_pic


@app.route('/uploadAvatar',methods=["post"])
@login_required
def uploadAvatar():
    data = request.files
    try:
        img = data['avatar']
        newImage = (uploadFunc(img))
        current_user.avatar = newImage
        db.session.commit();
        return {'pic' : newImage}
    except Exception:
        return None,404





@app.route('/updateGeneralInfo',methods=["POST"])
@login_required
def updateGeneralInfo():
    if request.content_type == "application/json":
        try:
            generalData = request.get_json()
            current_user.name = generalData.get('name')
            current_user.shopname = generalData.get('shop')
            current_user.location = generalData.get('location')
            db.session.commit()
            return {'message' : 'ok'},200
        except ConnectionError as ConError:
            raise ConError('Something went wrong while updating your details')
    else:
        raise TypeError('Provided data is not in json format')
