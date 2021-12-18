import os



from dotenv import load_dotenv

load_dotenv(os.path.abspath('.env'))
baseDir = os.path.abspath('.')




class BaseConfig:
    """
    BaseConfig class contains all the basic 
    configuration required in the application
    """
    DEBUG = False
    TESTING = False
    FLASK_ENV ='production'

    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY')
    RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY')
    MAX_CONTENT_LENGTH = 16*1024*1024
    UPLOAD_FOLDER = os.path.join(baseDir, 'static', 'user-images')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME')

    FLASK_ADMIN_SWATCH = 'Superhero'



class DevConfig(BaseConfig):
    DEBUG = True
    FLASK_ENV = 'development'
    SQLALCHEMY_DATABASE_URI = os.environ.get('MYSQL_DB_URI') or 'sqlite:///Databases/dev.db'



class ProdConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///Databases/prod.db'



class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    FLASK_ENV = 'testing'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///Databases/test.db'
