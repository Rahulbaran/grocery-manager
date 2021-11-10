import os
from flask import Flask, request, url_for, render_template, make_response
from config import DevConfig, ProdConfig, TestConfig
from flask_bcrypt import Bcrypt
from form import RegistrationForm




app = Flask(__name__)
mode = os.environ.get('FLASK_ENV')
if mode == "development":
    app.config.from_object(DevConfig)
elif mode == "production":
    app.config.from_object(ProdConfig)
else :
    app.config.from_object(TestConfig)

bcrypt = Bcrypt(app)





@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')



@app.route('/contactUs')
def contactUs():
    return render_template('contact.html', title='Contact Us')



@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    return render_template('register.html', title='Register Here',form=form)





if __name__=="__main__":
    app.run(port=5000, load_dotenv=True, debug=True)