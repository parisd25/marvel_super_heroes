import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))
# Give access to the project in ANY OS we find ourselves in
# Allow outside files/folders to be added to the project from the
# Base directory


class Config():
    """
    
        Set Config variables for the flask app.
        Using Enviroment variables where available otherwise
        create the config variables if not done already.
    """

    FLASK_APP = os.environ.get('FLASK_APP')
    FLASK_ENV = os.environ.get('FLASK_ENV')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'You will never guess'
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEPLOY_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    # Turn off Update Messages from the sqlalchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
