#check to make sure updates are working
from flask import Flask, render_template, flash, request, redirect, url_for
from wtforms import StringField, Form, validators, SelectField
from flask_wtf import FlaskForm
import hashlib
from sqlalchemy.orm import sessionmaker
import requests


from sqlalchemy import create_engine, String, Integer, Column
from sqlalchemy.ext.declarative import declarative_base
import sqlite3

engine = create_engine('sqlite:///user.db:')
base = declarative_base(engine)


class userMForm(FlaskForm):
	username = StringField('username')
	password = StringField('password')




class logindb(base):
	__tablename__ = 'logindb'
	id = Column(Integer, primary_key=True)
	username = Column(String(60))
	password = Column(String(60))


class quserform(base):
	__tablename__= 'quserform'
	id = Column(Integer, primary_key=True)
	name =  Column(String(60))

class QMForm(FlaskForm):
	name = StringField('name')



base.metadata.create_all(engine)
base.metadata.bind = engine
session = sessionmaker(bind=engine)
session = session()

app = Flask(__name__, static_url_path='')


'''class QSelect(FlaskForm):
	qusernames = []
	namelist = session.query(logindb.username).all()
	passlist = session.query(logindb.password).all()
	for item, pitem in zip(namelist, passlist):
	
		if 'not_needed' in pitem:
			qusernames.append(item)
	
	print(qusernames)
	select = SelectField(*qusernames)'''

@app.route('/', methods=['GET', 'POST'])
def landing_page():

	form = userMForm()

	
	if request.method == 'POST':
		print(request.form.get('username'))
		print(request.form.get('password'))
		username = str(request.form.get('username'))
		
		
		q = session.query(logindb.username.like(str(username)), logindb.password).all()
		for item in q:
			if item[0] == True:

				print(item[1])
				print('damnit')
				hashpass = hashlib.md5(str(request.form.get('password'))).hexdigest()
				print(hashpass)

				if hashpass == item[1]:
					print('its a match')
					return redirect('/welcome')
	return render_template('/homepage.html', form=form)


qusernames = []
namelist = session.query(logindb.username).all()
passlist = session.query(logindb.password).all()
for item, pitem in zip(namelist, passlist):

	if 'not_needed' in pitem:
		qusernames.append((item))

@app.route('/quick_loggin', methods=['GET', 'POST'])
def secondpage():
	form = userMForm()
	#sfield = QSelect()
	#data = {'name':'shit', 'one':'shity', 'two':'shat'}
	choice = request.form.get('news2')
	print(request.form.get('username'))
	
	
	if request.method == 'POST':
		if len(request.form.get('username')) > 0:
			print(request.form.get('username'))
		else:
			choice = request.form.get('news2')
			print(choice)

		#logs = logindb(username=str(request.form.get('username')), password='not_needed')

		#session.add(logs)
		#session.commit()
		
	
		
		return redirect(url_for('welcome'))

	return render_template('/quick_login.html', form=form, data=qusernames)






@app.route('/registration', methods=['GET', 'POST'])
def register():
	form = userMForm()
	if request.method == 'POST':
		print(request.form.get('username'))
		print(request.form.get('password'))
		password = str(request.form.get('password'))
		hashed_password = hashlib.md5(password.encode()).hexdigest()
		logs = logindb(username=str(request.form.get('username')), password=str(hashed_password))
		#logs = logindb(username=str(request.form.get('username')), password=str(password))
		session.add(logs)
		session.commit()
		print(hashed_password)
		print('hi')
		return redirect(url_for('landing_page'))
	return render_template('/register.html', form=form)


@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
	return render_template('/welcome.html')


@app.route('/')
def root():
    return app.send_static_file('index.html')
app.secret_key='just a check for now'
app.run(host='0.0.0.0')
