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

    def __init__(self, username, email, cashier, firstName, secondName, phoneNumber, birthDate, password,):
        self.username = username
        self.email = email
        self.cashier = cashier
        self.firstName = firstName
        self.secondName = secondName
        self.phoneNumber = phoneNumber
        self.birthDate = birthDate
        self.set_password(password)

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
    #listfilm_id = db.Column(db.Integer, db.ForeignKey('list_film.id'))
    #reservation_id = db.Column(db.Integer, db.ForeignKey('reservation.id'))
    #tags = db.Table('tags', db.Column('film_id', db.Integer, db.ForeignKey('film.id')),
    #db.Column('reservation_id', db.Integer, db.ForeignKey('reservation.id'))
    #)
    #film_id = db.Column(db.Integer, db.ForeignKey('film.id'))
    film_id = db.Column(db.Integer, db.ForeignKey('film.id'))
    time = db.Column(db.DateTime)
    date = db.Column(db.DateTime)
    hall = db.Column(db.String(100))
    session_price = db.Column(db.Integer())
    vip_price = db.Column(db.Integer())
    #sessions = db.relationship('Session_cinema', backref='film', lazy='dynamic')
    def __init__(self, time, date, hall, session_price, vip_price):
        #self.film_id = film_id
        self.time = time
        self.date = date
        self.hall = hall
        self.session_price = session_price
        self.vip_price = vip_price


class Reservation(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    resID = db.Column(db.Integer(), unique=True)
    priceTotal = db.Column(db.Integer())

    def __init__(self, resID, priceTotal):
        self.resID = resID
        self.priceTotal = priceTotal



#Вот это на самом конце должно быть
db.create_all()
