import os, secrets
from PIL import Image
from threading import Thread
from flask import session
from flask_mail import Message
from flask_login import current_user
from twilio.rest import Client
from grocery import mail, create_app



#Function to send the mail asynchronously
def send_mail_async(app,msg):
    with app.app_context():
        mail.send(msg) 




# Function to send email for resetting password
def send_reset_email(user):
    token = user.generate_token()
    msg = Message('[Grocery Manager]:Password Reset', recipients = [user.email])
    link = f"http://127.0.0.1:5000/passwordReset/{token}"
    linkStyle = 'background:hsl(260,100%,50%);padding:.55rem .8rem;color:#fff;border-radius:4px;text-decoration:none;font-size:1rem;box-shadow:0 0 2px rgba(0,0,0,.5);'
    msg.html = f'''
    <h2>
        To reset your password click on the button below
    </h2>
    <a href="{link}" style="{linkStyle}">
        Reset Password
    </a>
    <p style="font-size:1.1rem;">
        If you did not make this request then simply ignore this and no changes will be made in your account.
    </p>
    '''
    Thread(target=send_mail_async, args=(create_app(),msg)).start()
    # mail.send(msg)



# Function to save image in memory
def uploadFunc (pic):
    random_hex = secrets.token_hex(8)
    _,ext = os.path.splitext(pic.filename)
    mod_pic = random_hex + ext
    path = os.path.join(create_app().root_path,'static','user-images',mod_pic)

    size = (720,720)
    img = Image.open(pic)
    img.thumbnail(size)
    img.save(path)

    if current_user.avatar != 'default.png':
        os.remove(os.path.join(create_app().root_path,'static','user-images',current_user.avatar))

    return mod_pic



# Function to send otp for admin
def sendOtp(num):
    account_sid = os.environ.get('ACCOUNT_SID')
    auth_token = os.environ.get('AUTH_TOKEN')
    twilio_number = os.environ.get('TWILIO_PHONE_NUMBER')
    receiver_number = os.environ.get('PERSONAL_MOBILE_NUMBER')
    client = Client(account_sid, auth_token)
    try :
        message = client.messages.create(
            body = f"Your OTP is {num}",
            from_ = twilio_number,
            to = receiver_number
        )
        session['otp'] = num
        return message.sid
    except Exception:
        return None