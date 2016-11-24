from flask import render_template, request, session, redirect
from app.models import User, db, Session_cinema, Film
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
        firstName = request.form['firstName']
        secondName = request.form['secondName']
        email = request.form['email']
        password = request.form['password']
        cpassword = request.form['cpassword']
        loginSite = User.query.filter_by(Email=email).first()
        if loginSite is None:
            if password == cpassword:
                user = User(firstName, secondName, email, password)
                db.session.add(user)
                db.session.commit()
                return redirect("/login")
            else:
                ControlPassword = True
                return render_template('registration.html', ControlPassword=ControlPassword)
        else:
            ControlEmail = True
            return render_template('registration.html', ControlEmail=ControlEmail)
    return render_template('registration.html')



###########################################


@app.route("/login", methods=['POST','GET'])
def login():
	if request.method == "POST":
		username = request.form['login']
		password = request.form['password']
		loginBool = True
		loginSite = User.query.filter_by(Email=username).first()
		if loginSite:
			if loginSite is None:
				return render_template('authorization.html', loginBool=loginBool)
			else:
				if loginSite.check_password(password):
					session['username'] = login
					session['firstName'] = loginSite.FirstName
					session['secondName'] = loginSite.SecondName
					return redirect('/')
				else:
					return render_template('authorization.html', loginBool=loginBool)
		else:
			return render_template('authorization.html', loginBool=loginBool)
	
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


