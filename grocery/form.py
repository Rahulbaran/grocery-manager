from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import EmailField, BooleanField
from flask_login import current_user
from .models import User





# User Registration Form
class RegistrationForm(FlaskForm):
    name = StringField('Fullname', validators=[Length(min=5, max=100, message='name should be 5 to 100 characters long'), InputRequired()])
    username = StringField('Username', validators=[Length(min=5, max=50, message='username should be 5 to 50 characters long'), InputRequired()])
    email = EmailField('Email Address', validators=[InputRequired(), Length(min=10, max=200, message='email must be at max 200 characters long')])
    password = PasswordField('Password', validators=[Length(min=8, max=100, message='password should be 8 to 100 characters long'), InputRequired()])
    reenter_password = PasswordField('Re-enter Password', validators=[EqualTo('password', message='should match with password')])
    recaptcha = RecaptchaField()
    submit = SubmitField('Register')


    def validate_password(self,password):
        specialChar = '!@#$%^&*()_+-=|\}]{[:;?/>.<,~`\'\"'
        totalSpecialChar = 0
        for char in password.data:
            if char in specialChar:
                totalSpecialChar += 1
        if totalSpecialChar == 0:
            raise ValidationError('password should have atleast one special character')

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('email is already exist')

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('username is already exist')






# User Login Form
class LoginForm(FlaskForm):
    emailOrUsername = StringField('Email or Username', validators=[InputRequired()]) 
    password = PasswordField('Password', validators=[Length(min=8, max=100,message='password should be 8 to 100 characters long'), InputRequired()])
    remember_me = BooleanField(label='Remember Me')
    submit = SubmitField('Login')






# Update General Details Form
class UpdateGeneralDetailsForm(FlaskForm):
    name = StringField('Fullname', validators = [Length(min=5, max=100), InputRequired()])
    shopName = StringField('Shopname', validators = [Length(min=10, max=100)])
    location =StringField('Location', validators = [Length(min=10, max=200)])
    submit = SubmitField('Update')





# Update username and email Form
class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[Length(min=5, max=50, message='username should be 5 to 50 characters long'), InputRequired()])
    email = EmailField('Email Address', validators=[InputRequired(), Length(min=10, max=200, message='email must be at max 200 characters long')]) 
    submit = SubmitField('Update')



    def validate_username(self,username):
        if current_user.username != username.data :
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('username is already exist')


    def validate_email(self,email):
        if current_user.email != email.data:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('email is already exist')