from flask import render_template, request, session, redirect, flash, url_for
from app.models import User, db, Session_cinema, Film, Reservation
from app import app
from datetime import datetime
#Сектерный ключ никому не выдавать
app.secret_key = '_\x1ea\xc2>DK\x13\xd0O\xbe1\x13\x1b\x93h2*\x9a+!?\xcb\x8f'


@app.route("/")
@app.route("/index")
def hello():
    #При открытии страницы проверить авторизован ли пользователь
    if 'username' in session:
        auth = True
        if 'firstName' in session:
            navbar_firstName = session['firstName']
            navbar_secondName = session['secondName']
            return render_template("index.html", auth=auth, navbar_firstName=navbar_firstName, navbar_secondName=navbar_secondName)
        return render_template("index.html", auth=auth)
    else:
        auth = False
        return render_template("index.html", auth=auth)

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
                flash("Неправльно введен электронная почта или пароль")
                return redirect(url_for('login'))
            else:
                if(loginSite.check_password(password)):
                    session['username'] = loginSite.username
                    session['firstName'] = loginSite.firstName
                    session['secondName'] = loginSite.secondName
                    session['id'] = loginSite.id
                    return redirect('/')
                else:
                    flash("Неправльно введен пароль")
                    return redirect(url_for('login'))
        else:
            flash("Неправльно введен электронная почта")
            return redirect(url_for('login'))
    return render_template('authorization.html')


@app.route('/logout')
def logout():
    # удалить из сессии имя пользователя, если оно там есть
    session.pop('username', None)
    return redirect('/')


@app.route('/film', methods=['POST','GET'])
def get_film():
    if request.method == 'POST':
        name = request.form['name1']
        description = request.form['description']
        genre = request.form['genre']
        length = request.form['length']
        cast = request.form['cast']
        ageRestriction = request.form['ageRestriction']
        movie = Film(name, description, genre, cast, length, ageRestriction)
        db.session.add(movie)
        db.session.commit()
        return redirect('/')
    return render_template('listfilm.html')

@app.route('/session', methods=['POST', 'GET'])
def session_cinema():
    if request.method == 'POST':
        time = request.form['time']
        data = request.form['data']
        hall = request.form['hall']
        session_price = request.form['session_price']
        time = datetime.strptime(time, "%H:%M")
        sessions = Session_cinema(time, data, hall, session_price)
        db.session.add(sessions)
        db.session.commit()
        return redirect("/")
    return render_template('session.html')


@app.route('/reservation', methods=['POST', 'GET'])
def reservation():
    if request.method == 'POST':
        resID = request.form['resID']
        priceTotal = request.form['priceTotal']
        reservation_session = Reservation(resID, priceTotal)
        db.session.add(reservation_session)
        db.session.commit()
        return redirect("/")
    ses_id = request.args.get('session_id')
    sessions = Session_cinema.query.filter_by(id = ses_id).first()

    return render_template('reservation.html')


