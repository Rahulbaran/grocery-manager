import os
from dotenv import load_dotenv

load_dotenv(os.path.abspath('.env'))
baseDir = os.path.realpath(os.path.abspath(__file__))
print(baseDir)



class BaseConfig:
    """
    BaseConfig class contains all the basic 
    configuration required in the application
    """
    DEVELOPMENT = False
    TESTING = False
    FLASK_ENV ='production'

    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RECAPTCHA_PUBLIC_KEY=os.environ.get('RECAPTCHA_PUBLIC_KEY')
    RECAPTCHA_PRIVATE_KEY=os.environ.get('RECAPTCHA_PRIVATE_KEY')




class DevConfig(BaseConfig):
    DEVELOPMENT = True
    FLASK_ENV='development'




class ProdConfig(BaseConfig):
    FLASK_ENV='production'




class TestConfig(BaseConfig):
    DEVELOPMENT = True
    FLASK_ENV='testing'