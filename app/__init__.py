from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5432/dataBaseSite' #postgresql://имя:пароль@localhost:порт/база данных
db = SQLAlchemy(app)
from app import views, models
