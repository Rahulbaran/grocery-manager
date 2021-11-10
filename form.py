from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, PasswordField
from wtforms.fields.html5 import EmailField, IntegerField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError





# User Registration Form
class RegistrationForm(FlaskForm):
    name = StringField('Fullname', validators=[Length(min=5,max=100,message='name should be atleast 5 characters long'), InputRequired()])
    username = StringField('Username', validators=[Length(min=5, max=50, message='username should be atleast 5 characters long'), InputRequired()])
    email = EmailField('Email Address', validators=[InputRequired(), Length(max=200, message='email must be at max 200 characters long')])
    shopname = StringField('Shop Name', validators=[InputRequired(), Length(max=100, message='shopname must be at max 100 characters long')])
    password = PasswordField('Password', validators=[Length(min=8, max=100,message='password should have characters in range of 8 to 100'), InputRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password', message='should match with password')])
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
