from flask import Flask,render_template,session
from flask import url_for,request,redirect
from pymongo import MongoClient
import random
from flask.ext.sqlalchemy import SQLAlchemy
from hashlib import md5
app=Flask('Gandalf')
app.debug=True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost:3306/zzuli'
mysql = SQLAlchemy(app)


client=MongoClient('zp.tristan.pub',10011)
db=client.douban



#session setting
app.secret_key='123'
@app.route('/')
def index():
	if(session.get('username') is not None and session.get('username') != '!logout'):
		return redirect(url_for('home'))
	else:
		return render_template('login.html')

@app.route('/home')
def home():
	if(session.get('username') is None or session.get('username') == '!logout'):
		return redirect(url_for('index'))
	"""
	random pick 3 movies
	"""
	ml=list()
	idlist=list()
	for i in range(10):
		if(len(ml)>=3):
			break
		cursor=db.mv_test1.find()
		seed=random.randint(0,cursor.count()-1)
		cursor.skip(seed)
		mv=cursor.next()
		if(mv['id'] not in idlist):
			idlist.append(mv['id'])
			ml.append(mv)
	return render_template('home.html',mvlist=ml,username=session.get('username'))

@app.route('/login',methods=['GET','POST'])
def login():
	#session['username']='Tristan'
	temp_user=request.args.get('username')
	temp_pwd=request.args.get('password')
	m=md5()
	m.update(temp_pwd)
	pwd=m.hexdigest()
	user=User.query.filter_by(username=temp_user).first()
	if(user is not None and user.password==pwd):
		session['username']=user.username
		return	redirect(url_for('home'))
	else:
		return 	redirect(url_for('index'))
	#return '<h1>Username: %s<br/><h1>Password:%s ' % (user,pwd)
	#return '<h1>Login in !!</h1>'

@app.route('/logout')
def logout():
	session['username']='!logout'
	return redirect(url_for('home'))
#For test!!!
#For test!!!!!! code review delete
@app.route('/tristan/<user>')
def admin(user):
	session['username']=user
	return redirect(url_for('home'))

class User(mysql.Model):
    id = mysql.Column(mysql.Integer, primary_key=True)
    username = mysql.Column(mysql.String(80), unique=True)
    email = mysql.Column(mysql.String(120), unique=True)
    password=mysql.Column(mysql.String(120))

    def __init__(self, username, email,password):
        self.username = username
        self.email = email
        self.md5=md5()
        self.md5.update(password)
        self.password=self.md5.hexdigest()

    def __repr__(self):
        return '<User %r>' % self.username

if (__name__ == '__main__'):
	app.run()
