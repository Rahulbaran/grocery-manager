from flask import request, url_for, render_template, make_response, redirect, flash
from . import app
from .form import RegistrationForm, LoginForm





@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')




@app.route('/contactUs')
def contactUs():
    headers = {'Content-Type' : 'text/html'}
    res = make_response(render_template('contact.html', title='Contact Us'),headers)
    res.set_cookie('theme','red',max_age=1000, path="/contactUs")
    return res




@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Congrats {form.name.data}, You have registered🎊', 'info')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register Here',form=form)




@app.route('/login', methods=["GET","POST"])
def login():
    form = LoginForm()
    return render_template('login.html', title='Login',form=form)