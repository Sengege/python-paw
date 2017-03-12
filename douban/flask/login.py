from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from hashlib import md5
app = Flask(__name__)
#mysql url format mysql://username:password@hostname/database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost:3306/zzuli'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password=db.Column(db.String(120))

    def __init__(self, username, email,password):
        self.username = username
        self.email = email
        self.md5=md5()
        self.md5.update(password)
        self.password=self.md5.hexdigest()

    def __repr__(self):
        return '<User %r>' % self.username
