from flask import request, url_for, render_template, make_response, redirect, flash
from flask_login import login_user, logout_user, current_user, login_required
from . import app, bcrypt, db
from .form import RegistrationForm, LoginForm
from .models import User, Product




@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')




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





@app.route('/settings', methods=["POST","GET"])
@login_required
def settings():
    return render_template('settings.html', title='Settings')





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
        for prod in newProducts:
            product = Product(name=prod[0], unit=prod[1], price=prod[2], product_user=current_user)
            db.session.add(product)
        db.session.commit()

        resProductsData = Product.query.filter_by(user_id=current_user.id).order_by(Product.id.desc()).limit(len(newProducts)).all()
        resProducts = list()
        for resProduct in resProductsData:
            resProducts.append([resProduct.id,resProduct.name,resProduct.unit,resProduct.price])
        resProducts.reverse()
        return {'newProducts' : resProducts}





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
    return render_template('orders.html', title='Manage Orders')