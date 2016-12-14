import os

from flask import render_template, request, session, redirect, flash, url_for
from flask import send_from_directory
from werkzeug.utils import secure_filename

from app.models import User, db, Session_cinema, Film, Reservation
from app import app
from datetime import datetime
from sqlalchemy import update
import random
from flask_gravatar import Gravatar
import re

#Сектерный ключ никому не выдавать
app.secret_key = '_\x1ea\xc2>DK\x13\xd0O\xbe1\x13\x1b\x93h2*\x9a+!?\xcb\x8f'

UPLOAD_FOLDER = app.root_path+'\static\img\kino\posters'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
@app.route("/index")
def index():
    #searchword = request.args.get('key', '')
    return render_template("index.html")

##########################################


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == 'POST':
        username = request.form['username']
        firstName = request.form['firstName']
        secondName = request.form['secondName']
        email = request.form['email']
        date = request.form['date']
        phoneNumber = request.form['phoneNumber']
        password = request.form['password']
        cpassword = request.form['cpassword']
        conditions = request.form['conditions']
        loginSite = User.query.filter_by(username=username).first()
        if loginSite:
            flash("Логин занят")
            return redirect(url_for('register'))
        else:
            if (password == cpassword):
                    if conditions == "on":
                        user = User(username, email, None, firstName, secondName, phoneNumber, date, password)
                        db.session.add(user)
                        db.session.commit()
                        return redirect(url_for("login"))
                    else:
                        flash("Вы не приняли условия!")
                        return redirect(url_for('register'))
            else:
                flash("Пароли не совпадают!")
                return redirect(url_for('register'))

    return render_template('registration.html')

###########################################


@app.route("/login", methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form['login']
        password = request.form['password']
        loginSite = User.query.filter_by(username=username).first()
        if (loginSite):
            if loginSite is None:
                flash("Неправильно введен логин")
                return redirect(url_for('login'))
            else:
                if(loginSite.check_password(password)):
                    session['username'] = loginSite.username
                    session['firstName'] = loginSite.firstName
                    session['secondName'] = loginSite.secondName
                    session['id'] = loginSite.id
                    return redirect('/')
                else:
                    flash("Неправильно введен пароль")
                    return redirect(url_for('login'))
        else:
            flash("Неправильно введен логин")
            return redirect(url_for('login'))
    return render_template('authorization.html')


@app.route('/settings', methods=["POST", "GET"])
def settings():
    if 'username' in session:
        if request.method == "POST":
            password = request.form['password']
            new_password = request.form['new_password']
            new_password2 = request.form['new_password2']
            username = session['username']
            c = User.query.filter_by(username=username).first()
            if c:
                if c.check_password(password):
                    if new_password == new_password2:
                        """user = update(User).values(set_password=new_password)
                        db.session.execute(user)
                        db.session.commit()"""
                        flash('Пароли изменены')
                        return redirect(url_for('settings'))
                    else:
                        flash('Новые пароли не совпадают')
                        return redirect(url_for('settings'))
                else:
                    flash('Такого пароля нету')
                    return redirect(url_for('settings'))
            else:
                flash('Такого пароля нету')
                return redirect(url_for('settings'))
        else:
            return render_template('setting.html')
    else:
        return redirect(url_for('hello'))


@app.route('/profile')
def profile():
    username = session['username']
    user = User.query.filter_by(username=username).first()
    gravatar = Gravatar(app,
                        size=128,
                        rating='g',
                        default='mm',
                        force_default=False,
                        force_lower=False,
                        use_ssl=False,
                        base_url=None)
    return render_template('profile.html',user=user, gravatar=gravatar)


@app.route('/logout')
def logout():
    # удалить из сессии имя пользователя, если оно там есть
    session.pop('username', None)
    return redirect('/')


@app.route('/room', methods=['POST', 'GET'])
def view_room():
    if request.method == "POST":
        seats = request.form['selectedSeats']
        print(seats)
        return redirect('/room?id=1')
    id = request.args.get('id')
    if id is None:
        return '', 404
    ses = Session_cinema.query.filter_by(id=id).first()
    return render_template('room.html', ses=ses)




@app.route('/film', methods=['POST', 'GET'])
def add_film():
    if request.method == 'POST':
        name = request.form['name1']
        description = request.form['description']
        genre = request.form['genre']
        producer = request.form['producer']
        year = request.form['year']
        country = request.form['country']
        length = request.form['length']
        cast = request.form['cast']
        ageRestriction = request.form['ageRestriction']
        if 'file' not in request.files:
            flash('Нету файла')
            return redirect(url_for('add_film'))
        file = request.files['file']
        if file.filename == '':
            flash('Файл не выбран')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            foto = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            index = str(foto).find("static")
            pathPhoto = str(foto[index:])
            movie = Film(name, description, cast, genre, producer, year, country, length, ageRestriction, pathPhoto)
            db.session.add(movie)
            db.session.commit()
            return redirect(url_for("session_cinema"))
    return render_template('addfilms.html')


@app.route('/page', methods=['POST','GET'])
def page_film():
    if request.method == 'POST':
        return request(url_for('page_film'))
    if request.method == 'GET':
        id = request.args.get('id')
        film = Film.query.filter_by(id=id).first()
        ses = Session_cinema.query.filter_by(film_id=id).first()
        if film is None:
            return render_template('index.html')
        else:
            hour = film.length//60
            minute = film.length - 60*hour
            return render_template('films.html', film=film, ses=ses, hour=hour, minute=minute)
    return render_template('films.html')


@app.route('/upload', methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        return redirect(url_for('upload_file'))
    return render_template('upload_slide_poster.html',items=Film.query.all())

@app.route('/session', methods=['POST', 'GET'])
def session_cinema():
    if request.method == 'POST':
        film_name = request.form['film_name_result']
        filmId = Film.query.filter_by(name=film_name).first()
        if filmId is None:
            flash("Данного фильма нету")
            return redirect(url_for('session_cinema'))
        else:
            time = request.form['time']
            date = request.form['date']
            hall = request.form['hall']
            session_price = request.form['session_price']
            vip_price = request.form['vip_price']
            time1 = datetime.strptime(time, "%H:%M")
            sessions = Session_cinema(filmId.id, time1, date, hall, session_price, vip_price)
            db.session.add(sessions)
            db.session.commit()
            return redirect(url_for("session_list"))

    return render_template('session.html', items=Film.query.all())


@app.route('/session/list', methods=['POST', 'GET'])
def session_list():
    return render_template('session_list.html', items=Session_cinema.query.all())


@app.route('/reservation', methods=['POST', 'GET'])
def reservation():
    if request.method == 'POST':
        resID = request.form['resID']
        priceTotal = request.form['priceTotal']
        reservation_session = Reservation(resID,priceTotal)
        db.session.add(reservation_session)
        db.session.commit()
        return redirect("/")
    ses_id = request.args.get('session_id')
    session = Session_cinema.query.filter_by(id=ses_id).first()
    if session is None:
        pass
    randomNumber = random.randrange(10000)
    resIDsave = Reservation(None, None, randomNumber)
    db.session.add(resIDsave)
    db.session.commit()
    return render_template('reservation.html', session=session, randomNumber=randomNumber)


@app.route('/reservation_check', methods=['POST','GET'])
def reservation_check():
    if request.method == 'POST':
        res_id = request.form['res_id']
        reserve = Reservation.query.filter_by(resID=res_id).first()
        if reserve is None:
            flash("Ошибка! Строка пуста либо брони с таким номером не существует.")
            return redirect(url_for('reservation_check'))
        else:
            return render_template('reservation_check.html', items=reserve)
    return render_template('reservation_check.html')
