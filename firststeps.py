import time, datetime
import json
import os
import random
from pprint import pprint
from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import luck

app = Flask(__name__)
app.config.from_pyfile('app.cfg')
db = SQLAlchemy(app)
current_week = "666666"

class User(db.Model):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String)
	fullname = db.Column(db.String)
	password = db.Column(db.String)
	luck = db.Column(db.Float)
	photo = db.Column(db.String)

	def __repr__(self):
		return "<User(name='%s', fullname='%s', password='%s', luck='%.2f', photo='%s')>" % (self.name, self.fullname, self.password, self.luck, self.photo)

	def __init__(self, name, fullname="", password="", luck=0, photo=""):
		self.name=name
		self.fullname=fullname
		self.password=password
		self.luck=luck
		self.photo=photo

class JackPot(db.Model):
	__tablename__ = 'JackPot'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String)
	million = db.Column(db.Integer)
	extra = db.Column(db.Integer)

	def __repr__(self):
		return "<JackPot(name='%s', million='%d', extra='%d')>" % (self.name, self.million, self.extra)

class Play(db.Model):
	__tablename__ = "play"

	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.String)
	user_id = db.Column(db.Integer)
	week = db.Column(db.String)
	luck = db.Column(db.Float)

	def __repr__(self):
		return "<Play(date='%s', user_id='%d', luck='%f')>" % (self.date, self.user_id, self.luck)

class LottoStore(db.Model):
	__tablename__ = "store"

	id = db.Column(db.Integer, primary_key=True)
	lat = db.Column(db.Float)
	lng = db.Column(db.Float)
	luck = db.Column(db.Float)

def initJackPot():
	Max = JackPot(name="Max", million=60, extra=25)
	Six49 = JackPot(name="Six49", million=14, extra=1)
	db.session.add(Max)
	db.session.add(Six49)
	db.session.commit()

def initUsers():
	with open('names.json') as data_file:
		data = json.load(data_file)

	for i in data:
		print i
		user = User(name=i["name"], photo=i["photo"])
		db.session.add(user)
		db.session.commit()

def initPlay():
	play = Play(date=time.strftime("%x"))
	db.session.add(play)
	db.session.commit()

def initStore():
	s1 = LottoStore(lat=49.278441, lng=-123.124564)
	s2 = LottoStore(lat=49.278334, lng=-123.124361)
	s3 = LottoStore(lat=49.277575, lng=-123.126956)
	s4 = LottoStore(lat=49.278411, lng=-123.128448)
	db.session(s1)
	db.session(s2)
	db.session(s3)
	db.session(s4)
	db.session.commit()


@app.route('/', methods=["GET", "POST"])
def home_page():
	if request.method == "POST":
		if request.form['id']:
			tmp = request.form['id']
			play = Play.query.filter_by(week=current_week, user_id=tmp).first()
			user = User.query.filter_by(id=tmp).first()
			if not play:
				play = Play(date=datetime.datetime.utcnow(), user_id=int(tmp), week=current_week, luck=luck.GetLuck(user.name))
				print luck
				print play
				db.session.add(play)
				db.session.commit()

		return redirect(url_for('home_page'))
	# play_list = User.query.join(Play, User.idPlay.user_id).filter(Play.week = current_week).add_columns(Users.name, Play.luck).order_by(Play.luck.desc())
	play_list = User.query.join(Play, (User.id == Play.user_id)).filter(Play.week==current_week).add_columns(User.name, Play.luck).order_by(Play.luck.desc()).all()
	plays = Play.query.all();
	return render_template("home.html", users=User.query.order_by(User.name.asc()).all(), jackpots=JackPot.query.all(), play=Play.query.order_by(Play.luck).all(), play_list=play_list)

@app.route('/dashboard', methods=["GET", "POST"])
def dashboard():
	if request.method == "POST":
		if request.form['reset']:
			Play.query.filter_by(week=current_week).delete()
	return render_template("dashboard.html")

# print time.strftime("%x")

if __name__ == '__main__':
	# db.drop_all()
	# db.create_all()
	# initUsers()
	# initJackPot()
	# Model.__t
	app.run( 
        host="0.0.0.0",
        port=int("8888")
  )
