from sqlalchemy.orm import sessionmaker
import time
import json
import os
from pprint import pprint
from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('app.cfg')
db = SQLAlchemy(app)

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
	players = db.Column(db.String)

	def __repr__(self):
		return "<Play(date='%s', player='%s')>" % (self.date, self.players)


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
	play = Play(date=time.strftime("%x"), players="")
	db.session.add(play)
	db.session.commit()

@app.route('/', methods=["GET", "POST"])
def home_page():
	if request.method == "POST":
		print User.query.order_by(User.name.asc()).all()
	return render_template("home.html", users=User.query.order_by(User.name.asc()).all(), jackpots=JackPot.query.all(), play=Play.query.all())

	Comments.query.order_by(Comments.pub_date.desc()).all()

# print time.strftime("%x")

if __name__ == '__main__':
	db.create_all()
	# initUsers()
	# initJackPot()
	# initPlay()
	app.run( 
        host="0.0.0.0",
        port=int("6490")
  )