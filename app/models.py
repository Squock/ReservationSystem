from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db

app.config['SECRET_KEY'] = 'super-secret'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    cashier = db.Column(db.String(120),default=False)
    firstName = db.Column(db.String(100))
    secondName = db.Column(db.String(100))
    phoneNumber = db.Column(db.String(100))
    birthDate = db.Column(db.DateTime)
    password = db.Column(db.String(100))

    def __init__(self, username, password, email, cashier, firstName, secondName, phoneNumber, birthDate):
        self.username = username
        self.set_password(password)
        self.email = email
        self.cashier = cashier
        self.firstName = firstName
        self.secondName = secondName
        self.phoneNumber = phoneNumber
        self.birthDate = birthDate

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User %r>' % self.username
		
class Film(db.Model):
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
    film_id = db.Column(db.Integer)
    time = db.Column(db.DateTime)
    data = db.Column(db.DateTime)
    hall = db.Column(db.String(100))
    session_price = db.Column(db.Integer())

    def __init__(self, time, data, hall, session_price):
        self.time = time
        self.data = data
        self.hall = hall
        self.session_price = session_price




class Reservation(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    resID = db.Column(db.String(100), unique=True)
    priceTotal = db.Column(db.Integer)

    def __init__(self, resID, priceTotal):
        self.resID = resID
        self.priceTotal = priceTotal



#Вот это на самом конце должно быть
db.create_all()
