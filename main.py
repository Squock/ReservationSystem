from flask import Flask, render_template, request, escape, session, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import Form, BooleanField, StringField, PasswordField, validators, TextField
from app.models import Role, User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/dataBaseSite'
db = SQLAlchemy(app)

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

db.create_all()

class RegistrationForm(Form):
    firstName = StringField('Имя',[validators.Length(min=2, max=25)])
    secondName = StringField('Фамилия', [validators.Length(min=3, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=35)])
    password = PasswordField('Пароль', [
        validators.DataRequired(),  validators.Length(min=4, max=25),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Повторить пароль')
    accept_tos = BooleanField('Я соглашаюсь с условиями', [validators.DataRequired()])


@app.route("/")
def hello():
    if 'username' in session:
        auth = True
        if 'firstName' in session:
            navbar_firstName = session['firstName']
            navbar_secondName = session['secondName']
            return render_template("index.html", auth=auth, navbar_firstName=navbar_firstName, navbar_secondName=navbar_secondName)
        return render_template("index.html", auth=auth)
    else:
        auth=False
        return render_template("index.html", auth=auth)

@app.route("/registration")
def registration():
    form = RegistrationForm()
    return render_template("registration.html", form=form)


@app.route("/register", methods=["POST", "GET"])
def register():

    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.firstName.data, form.secondName.data, form.email.data, form.password.data)
        role = Role(form.email.data, "user")
        db.session.add(user)
        db.session.add(role)
        db.session.commit()
        return redirect("/authorization")
    return render_template('registration.html', form=form)

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

if __name__ == "__main__":
    app.run("127.0.0.1", 5050)