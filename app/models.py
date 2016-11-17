from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db

app.config['SECRET_KEY'] = 'super-secret'

#<<<<<<< HEAD

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:nr812za4@localhost:5432/dataBaseSite' #postgresql://имя:пароль@localhost:порт/база данных


roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

#=======
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5432/dataBaseSite' #postgresql://имя:пароль@localhost:порт/база данных

#>>>>>>> 98091764f9866d4412d9612c77cf313e3c8b4d79

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


#<<<<<<< HEAD

class ListFilm(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(255))
    cast = db.Column(db.String(80))
    genre = db.Column(db.String(15))
    length = db.Column(db.Integer())
    ageRestriction = db.Column(db.Integer())

    def __init__(self, name, description,cast, genre, length, ageRestriction):
        self.name = name
        self.description = description
        self.cast = cast
        self.genre = genre
        self.length = length
        self.ageRestriction = ageRestriction


class Session_cinema(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    film_id = db.Column(db.Integer, db.ForeignKey('Reservation.id'))
    time = db.Column(db.DateTime)
    data = db.Column(db.DateTime)
    hall = db.Column(db.String(100))
    session_price = db.Column(db.Integer())

    def __init__(self, time, data, hall, session_price):
        self.time = time
        self.data = data
        self.hall = hall
        self.session_price = session_price

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
db.create_all()
#=======
class Reservation(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    resID = db.Column(db.String(100), unique=True)
    priceTotal = db.Column(db.Integer)

    def __init__(self, resID, priceTotal):
        self.resID = resID
        self.priceTotal = priceTotal





#>>>>>>> 98091764f9866d4412d9612c77cf313e3c8b4d79
