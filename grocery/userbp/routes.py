import os, random
from flask import Blueprint, render_template, url_for, request, redirect, flash, session
from flask_login import current_user, login_required, login_user, logout_user
from grocery import db, bcrypt
from grocery.models import User
from grocery.userbp.form import RegistrationForm, AdminLoginForm, LoginForm, PasswordResetForm, OTPForm,\
                              PasswordResetRequestForm, UpdateAccountForm, UpdateGeneralDetailsForm
from grocery.userbp.utils import send_reset_email, uploadFunc, sendOtp



userbp = Blueprint('userbp', __name__)





@userbp.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        flash('You are already logged in','info')
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_pw=bcrypt.generate_password_hash(form.password.data)
        user = User(name=form.name.data, username=form.username.data, email=form.email.data, password=hash_pw)
        db.session.add(user)
        db.session.commit()
        flash(f'Congrats {form.name.data}, You have registered🎊', 'info')
        return redirect(url_for('userbp.login'))
    return render_template('register.html', title='Register Here', form=form)





@userbp.route('/login', methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in','info')
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        emailUser = User.query.filter_by(email=form.emailOrUsername.data).first()
        usernameUser = User.query.filter_by(username=form.emailOrUsername.data).first()
        password = lambda original, pw: bcrypt.check_password_hash(original, pw) 

        if emailUser and password(emailUser.password, form.password.data):
            next = request.args.get('next')
            flash('Welcome back, You have logged in', 'info')
            login_user(emailUser, remember=form.remember_me.data)
            return redirect(next) if next else redirect(url_for('main.home'))
        elif usernameUser and password(usernameUser.password, form.password.data):
            flash('Welcome back, You have logged in', 'info')
            next = request.args.get('next')
            login_user(usernameUser, remember=form.remember_me.data)
            return redirect(next) if next else redirect(url_for('main.home'))
        else : 
            flash('Provided credentials doesn\'t match with our database', 'error')   

    return render_template('login.html', title='Login',form=form)





@userbp.route('/passwordResetRequest',methods=["GET","POST"])
def passwordResetRequest():
    if current_user.is_authenticated:
        flash('Please logout to reset your password', 'info')
        return redirect(url_for('main.home'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user  = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)
            flash('An mail has been sent to reset password','info')
        else:
            flash('Email address does not exist','info')
        return redirect(url_for('main.home'))
    return render_template('passwordResetRequest.html', title='Password Reset Request', form=form)





@userbp.route('/passwordReset/<token>',methods=["GET","POST"])
def passwordReset(token):
    if current_user.is_authenticated:
        flash('Please logout to reset your password', 'info')
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if not user:
        flash('The link is either invalid or expired', 'info')
        return redirect(url_for('main.home'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        hash_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hash_pw
        db.session.commit()
        flash('Your password has been updated','info')
        return redirect(url_for('userbp.login'))
    return render_template('passwordReset.html',title='Reset Password', form=form)





@userbp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have logged out from your account', 'info')
    return redirect(url_for('main.home'))






@userbp.route('/admin_login', methods=["GET","POST"])
def admin_login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        admin_username,admin_password = form.username.data, form.password.data
        if admin_username == os.environ.get('ADMIN_USERNAME') and admin_password == os.environ.get("ADMIN_PASSWORD"):
            otpNumber = random.randint(100000,999999)
            sid = sendOtp(otpNumber)
            if sid:
                return redirect(url_for('userbp.otp'))
            else:
                flash('OTP Couldn\'t get delivered','info')
                return redirect(url_for('main.home'))
        else :
            flash('Either username or password is wrong', 'error')
    return render_template('admin_login.html', title='Admin Login Page', form = form)
    





@userbp.route('/otp', methods=["GET", "POST"])
def otp():
    if session.get('otp'):
        form = OTPForm()
        if form.validate_on_submit() and session['otp'] == int(form.otp.data):
            session['admin_logged_in'] = True
            flash('Welcome admin you have logged in', 'info')
            return redirect('/admin')
        return render_template('otp.html', title='Admin Login OTP', form=form)
    else:
        flash('Admin should login first to access the otp page', 'error')
        return redirect(url_for('userbp.admin_login'))






@userbp.route('/admin_logout')
def admin_logout():
    if "admin_logged_in" in session:
        session.pop('admin_logged_in',default=None)
        session.pop('otp',default=None)
        flash('You have logged out from the admin page','info')
        return redirect(url_for('main.home'))
    else :
        flash('Please login before getting logged out', 'error')
        return redirect(url_for('userbp.admin_login'))





@userbp.route('/updateProfile', methods=["POST","GET"])
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
        flash('Username & Email have been updated','info')
        return redirect(url_for('userbp.updateProfile'))
    return render_template('updateProfile.html', title='Update Profile', accountForm=accountForm, generalForm=generalForm)





@userbp.route('/uploadAvatar',methods=["post"])
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





@userbp.route('/updateGeneralInfo',methods=["POST"])
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