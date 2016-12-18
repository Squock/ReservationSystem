from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from sqlalchemy.orm import relationship
app.config['SECRET_KEY'] = 'super-secret'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    firstName = db.Column(db.String(100))
    secondName = db.Column(db.String(100))
    phoneNumber = db.Column(db.String(100))
    birthDate = db.Column(db.DateTime)
    role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'), default=3)
    password = db.Column(db.String(100))


    def __init__(self, username, email, firstName, secondName, phoneNumber, birthDate, role_id, password):
        self.username = username
        self.email = email
        self.firstName = firstName
        self.secondName = secondName
        self.phoneNumber = phoneNumber
        self.birthDate = birthDate
        self.role_id = role_id
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Role(db.Model):
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')


class Film(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(5000))
    cast = db.Column(db.String(800))
    genre = db.Column(db.String(200))
    producer = db.Column(db.String(200))
    year = db.Column(db.Integer())
    country = db.Column(db.String(100))
    length = db.Column(db.Integer())
    ageRestriction = db.Column(db.Integer())
    foto = db.Column(db.String(200))

    def __init__(self, name, description,cast, genre, producer, year, country, length, ageRestriction, foto):
        self.name = name
        self.description = description
        self.cast = cast
        self.genre = genre
        self.producer = producer
        self.year = year
        self.country = country
        self.length = length
        self.ageRestriction = ageRestriction
        self.foto = foto


class Session_cinema(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    film_id = db.Column(db.Integer, db.ForeignKey('film.id'))
    time = db.Column(db.DateTime)
    date = db.Column(db.DateTime)
    hall = db.Column(db.String(100))
    session_price = db.Column(db.Integer())
    vip_price = db.Column(db.Integer())
    film = relationship('Film')

    def __init__(self, film_id, time, date, hall, session_price, vip_price):
        self.film_id = film_id
        self.time = time
        self.date = date
        self.hall = hall
        self.session_price = session_price
        self.vip_price = vip_price


class Reservation(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    resID = db.Column(db.Integer())
    priceTotal = db.Column(db.Integer())
    random = db.Column(db.String(20))

    def __init__(self, resID, priceTotal, random):
        self.resID = resID
        self.priceTotal = priceTotal
        self.random = random


class ResSeats(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    res_id = db.Column(db.Integer)
    seats = db.Column(db.ARRAY(db.String))
    summa = db.Column(db.Integer())
    seatsMesto = db.Column(db.String(500))
    def __init__(self, res_id, seats, summa, seatsMesto):
        self.res_id = res_id
        self.seats = seats
        self.summa = summa
        self.seatsMesto = seatsMesto


class Slide_photo(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    film_id = db.Column(db.Integer)
    film_name = db.Column(db.String(200))
    pathPhoto = db.Column(db.String(200))

    def __init__(self, film_id, film_name, pathPhoto):
        self.film_id = film_id
        self.film_name = film_name
        self.pathPhoto = pathPhoto


#Вот это на самом конце должно быть
db.create_all()
