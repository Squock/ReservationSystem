#!flask/bin/python
from app import app
app.debug = True
app.run("127.0.0.1", 5050)