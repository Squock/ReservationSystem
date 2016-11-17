from flask import render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore
<<<<<<< HEAD
from app.models import Role, User, db, ListFilm
=======
from app.models import Role, User, db, Session_cinema
>>>>>>> 056147cdfcbc76a3e8dabf98d48ca3da51b0c2e3
from app import app
from datetime import datetime
#Сектерный ключ никому не выдавать
app.secret_key = '_\x1ea\xc2>DK\x13\xd0O\xbe1\x13\x1b\x93h2*\x9a+!?\xcb\x8f'



# Setup Flask-Security

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

@app.route("/registration")
def registration():
    return render_template("registration.html")

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == 'POST':
        firstName = request.form['firstName']
        secondName = request.form['secondName']
        email = request.form['email']
        password = request.form['password']
        user = User(firstName, secondName, email, password)
        #role = Role(email, "user") Добавление ролей в БД (Админ, кассир, user)
        db.session.add(user)
        #db.session.add(role)
        db.session.commit()
        return redirect("/authorization")
    return render_template('registration.html')

###########################################

@app.route("/authorization")
def authorization():
    return render_template("authorization.html")

@app.route("/login", methods=['POST'])
def login():
    login = request.form['login']
    password = request.form['password']


    loginSite = User.query.filter_by(Email=login).first()
    if (loginSite):
        if loginSite is None:
            loginBool = True
            return render_template('authorization.html', loginBool=loginBool)
        else:
            if(loginSite.check_password(password)):
                session['username'] = login
                session['firstName'] = loginSite.FirstName
                session['secondName'] = loginSite.SecondName
                return redirect('/')
            else:
                loginBool = True
                return render_template('authorization.html', loginBool=loginBool)
    else:
        loginBool = True
        return render_template('authorization.html', loginBool=loginBool)

@app.route('/logout')
def logout():
    # удалить из сессии имя пользователя, если оно там есть
    session.pop('username', None)
    return redirect('/')

<<<<<<< HEAD
@app.route('/film', methods=['POST','GET'])
def get_film():
    if request.method == 'POST':
        name = request.form['name1']
        description = request.form['description']

        movie = ListFilm(name, description)
        db.session.add(movie)
        db.session.commit()
        return redirect('/')
    return render_template('listfilm.html')




=======
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
>>>>>>> 056147cdfcbc76a3e8dabf98d48ca3da51b0c2e3
