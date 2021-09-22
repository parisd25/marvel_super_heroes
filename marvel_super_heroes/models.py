from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime
from marvel.marvel import Marvel
from sqlalchemy.orm import backref


# Adding Flask Security for Passwords
from werkzeug.security import generate_password_hash, check_password_hash

# Import Secrets module (Givenby Python)
import secrets

#Imports for Login Manager
from flask_login import UserMixin, login_manager

#Imports for Flask Login
from flask_login import LoginManager

# Import for Flask-Marshmallow
from flask_marshmallow import Marshmallow
import hashlib


db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String(150), primary_key=True)
    first_name = db.Column(db.String(150), nullable=True, default='')
    last_name = db.Column(db.String(150), nullable=True, default='')
    email = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String, nullable=True, default='')
    g_auth_verify = db.Column(db.Boolean, default=False)
    token = db.Column(db.String, default='', unique=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    #hero = db.relationship('hero', backref='owner', lazy=True)

    def __init__(self, email, first_name='', last_name='', id='', password='', token='', g_auth_verify=False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'User {self.email} has been added to the database.'


class Hero(db.Model):
    id = db.Column(db.String, primary_key= True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(200), nullable= True)
    comic_appeared_in = db.Column(db.Numeric(precision=10, scale=2))
    super_power = db.Column(db.String(150), nullable= True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable=False)


    def get_hash():
        timestamp = datetime.utcnow().strftime('%m/%d/%Y %H:%M:%S')
        marvel_pub_key = '93f46f1ff08973d70263cb4b0756acb0'
        marvel_private_key = '08396b0cb4c569191987b2b16565f64704252596'


        hash_md5 = hashlib.md5()
        hash_md5.update(f'{timestamp}{marvel_private_key}{marvel_pub_key}'.encode('utf-8'))
        hash_params = hash_md5.hexdigest()

        return hash_params

    def __init__(self, name, description, comic_appeared_in, super_power, user_token, id=''):
        self.id = self.set_id()
        self.name = name
        self.description = description
        self.comic_appeared_in = comic_appeared_in
        self.super_power = super_power
        self.user_token = user_token
        

    def __init__(self, user_token):
        self.apiurl = 'https://gateway.marvel.com:443/v1/public/characters?ts={timestamp}&apikey={marvel_pub_key}&hash=get_hash()'








    def __repr__(self):
        return f'The following Hero has been added: {self.name}'

    def set_id(self):
        return secrets.token_urlsafe()

# Creation of API Schema via the Marshmallow Object


class HeroSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'description', 'comic_appeared_in', 'super_power']


hero_schema = HeroSchema()

heroes_schema = HeroSchema(many=True)


