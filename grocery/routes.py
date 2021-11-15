from flask import request, url_for, render_template, make_response, redirect, flash
from flask_login import login_user, logout_user, current_user, login_required
from . import app, bcrypt, db
from .form import RegistrationForm, LoginForm
from .models import User




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
            flash('Welcome back, You have logged in', 'info')
            login_user(emailUser,remember=form.remember_me.data)
            return redirect(url_for('home'))
        elif usernameUser and password(usernameUser.password, form.password.data):
            flash('Welcome back, You have logged in', 'info')
            login_user(usernameUser,remember=form.remember_me.data)
            return redirect(url_for('home'))
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