import os

from flask import json
from flask import render_template, request, session, redirect, flash, url_for
from flask import send_from_directory
from werkzeug.utils import secure_filename

from app.models import User, db, Session_cinema, Film, Reservation, Slide_photo, ResSeats
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
    return render_template("index.html", items=Slide_photo.query.all(), films=Session_cinema.query.all())

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
                        user = User(username, email, firstName, secondName, phoneNumber, date, None, password)
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
                    session['role'] = loginSite.role_id
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
        seats = request.form.getlist('selectedSeats')
        summa = request.form['sum']
        seatsMesto = request.form['selectedSeatsString']
        nameFilm = request.form['nameFilm']
        filmTime = request.form['filmTime']
        filmQuery = Film.query.order_by(Film.id.desc()).filter_by(name=nameFilm).limit(1).first()
        session_film = Session_cinema.query.filter_by(film_id=filmQuery.id).all()
        for se in session_film:
            ses = Session_cinema.query.filter_by(time=filmTime).first()
            s = ResSeats(ses.id, seats, summa, seatsMesto)
            db.session.add(s)
            db.session.commit()
            url = '/reservation?session_id='+str(ses.film_id)
            return redirect(url)
    id = request.args.get('id')
    if id is None:
        return '', 404
    time = request.args.get('time')
    date = request.args.get('date')
    ses1 = Session_cinema.query.filter_by(film_id=id).all()
    for se in ses1:
        sesDate = Session_cinema.query.filter_by(date=date).all()
        for se1 in sesDate:
            ses = Session_cinema.query.filter_by(time=time).first()
            film_name = ses.film.name
            data = [x.seats for x in ResSeats.query.filter_by(res_id=ses.id).all()]
            return render_template('room.html', ses=ses, film_name=film_name, data=json.dumps(data))


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


@app.route('/film/change', methods=['POST', 'GET'])
def change_film():
    id = request.args.get('id')
    if id is None:
        return '', 404
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
        ses = update(Film).where(Film.id == id).values(name=name, description=description,
                                                                                      genre=genre, producer=producer,
                                                                                      year=year,
                                                                                      country=country,length=length,cast=cast,ageRestriction=ageRestriction)
        db.session.execute(ses)
        db.session.commit()
        url = '/page?id=' + id
        return redirect(url)
    film = Film.query.filter_by(id=id).first()
    return render_template('films_change.html', film=film)


@app.route('/film/delete', methods=['POST', 'GET'])
def del_film():
    id = request.args.get('id')
    if id is None:
        return '', 404
    ses1 = Session_cinema.query.filter_by(film_id=id).all()
    for s in ses1:
        db.session.delete(s)
        db.session.commit()
    film = Film.query.filter_by(id=id).first()
    db.session.delete(film)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/page', methods=['POST', 'GET'])
def page_film():
    id = request.args.get('id')
    if id is None:
        return '', 404
    film = Film.query.filter_by(id=id).first()
    ses = Session_cinema.query.filter_by(film_id=id).all()  #[x.time for x in Session_cinema.query.filter_by(film_id=id).all()]
    #ses = Session_cinema.query.filter_by(film_id=id).first()
    if film is None:
        return render_template('index.html')
    else:
        hour = film.length//60
        minute = film.length - 60*hour
        return render_template('films.html', film=film, ses=ses, hour=hour, minute=minute)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        name = request.form['film_name_result']
        c = Film.query.filter_by(name=name).first()
        if c:
            UPLOAD_FOLDER = app.root_path + '\static\img\kino\slide'
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
            if 'file' not in request.files:
                flash('Нету файла')
                return redirect(url_for('upload_file'))
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
                save = Slide_photo(c.id, name, pathPhoto)
                db.session.add(save)
                db.session.commit()
                good = True
                return render_template('upload_slide_poster.html', good=good)
        else:
            flash('Такого фильма нет')
            return redirect(url_for('upload_file'))

    return render_template('upload_slide_poster.html', items=Film.query.all())


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


@app.route('/session/change', methods=['POST', 'GET'])
def session_change():
    id = request.args.get('id')
    time = request.args.get('time')
    date = request.args.get('date')

    if request.method == 'POST':
        film_name = request.form['film_name']
        time123 = request.form['time']
        date = request.form['date']
        hall = request.form['hall']
        session_price = request.form['session_price']
        vip_price = request.form['vip_price']
        time1 = datetime.strptime(time123, "%H:%M")
        filmId = Film.query.filter_by(name=film_name).first()
        ses3 = Session_cinema.query.filter_by(film_id=filmId.id).all()
        for se in ses3:
            sesDate = Session_cinema.query.filter_by(date=se.date).all()
            for se1 in sesDate:
                ses123 = Session_cinema.query.filter_by(time=time).first()
                if ses123:
                    ses = update(Session_cinema).where(Session_cinema.time == ses123.time).values(time=time1, date=date, hall=hall, session_price=session_price, vip_price=vip_price)
                    db.session.execute(ses)
                    db.session.commit()
                    return redirect(url_for('session_list'))
    if id is None:
        return '', 404
    ses1 = Session_cinema.query.filter_by(film_id=id).all()
    for se in ses1:
        sesDate = Session_cinema.query.filter_by(date=date).all()
        for se1 in sesDate:
            ses = Session_cinema.query.filter_by(time=time).first()
            return render_template('session_change.html', ses=ses, ses1=Film.query.all())


@app.route('/session/delete', methods=['POST', 'GET'])
def session_delete():
    id = request.args.get('id')
    time = request.args.get('time')
    date = request.args.get('date')
    if id is None:
        return '', 404
    ses1 = Session_cinema.query.filter_by(film_id=id).all()
    for se in ses1:
        sesDate = Session_cinema.query.filter_by(date=date).all()
        for se1 in sesDate:
            ses = Session_cinema.query.filter_by(time=time).first()
            if ses:
                ses_del = Session_cinema.query.filter_by(id=ses.id).first()
                db.session.delete(ses_del)
                db.session.commit()
                flash('Успешно удалено')
                return redirect(url_for('session_list'))


@app.route('/reservation', methods=['POST', 'GET'])
def reservation():
    ses_id = request.args.get('session_id')
    if ses_id is None:
        return '', 404
    sessio = Session_cinema.query.filter_by(film_id=ses_id).first()
    if sessio is None:
        pass
    randomNumber = random.randrange(1000, 10000)
    res1 = ResSeats.query.order_by(ResSeats.id.desc()).filter_by(res_id=sessio.film_id).limit(1).first()
    resIDsave = Reservation(res1.res_id, res1.summa, randomNumber)
    db.session.add(resIDsave)
    db.session.commit()

    res = ResSeats.query.order_by(ResSeats.id.desc()).filter_by(res_id=sessio.film_id).limit(1).first() #выбрал последнее
    return render_template('reservation.html', sessio=sessio, res=res, randomNumber=randomNumber)


@app.route('/reservation_check', methods=['POST','GET'])
def reservation_check():
    if request.method == 'POST':
        res_id = request.form['res_id']
        reserve = Reservation.query.filter_by(random=res_id).first()
        if reserve is None:
            flash("Ошибка! Строка пуста либо брони с таким номером не существует.")
            return redirect(url_for('reservation_check'))
        else:
            return render_template('reservation_check.html', items=reserve)
    return render_template('reservation_check.html')
