import os
from dotenv import load_dotenv

basedir=os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir,'.env'))

class Config():
    
    SECRET_KEY=os.environ.get('SECRET_KEY') or '1234'

    SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL') or 'sqlite:///'+os.path.join(basedir+'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS=False


    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_SSL = False
    MAIL_USE_TLS = True
    ADMINS = ['heraldjose10@gmail.com']

    POSTS_PER_PAGE = 5

    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
