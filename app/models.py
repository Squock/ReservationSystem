from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/dataBaseSite' #postgresql://имя:пароль@localhost:порт/база данных
db = SQLAlchemy(app)

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(255))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(100))
    SecondName = db.Column(db.String(100))
    Email = db.Column(db.String(100), unique=True)
    Password = db.Column(db.String(100))

    def __init__(self, FirstName, SecondName, Email, Password):
        self.FirstName = FirstName
        self.SecondName = SecondName
        self.Email = Email
        self.set_password(Password)


    def set_password(self, Password):
        self.Password = generate_password_hash(Password)

    def check_password(self, Password):
        return check_password_hash(self.Password, Password)

    def __repr__(self):
        return '<id {}>'.format(self.id)
