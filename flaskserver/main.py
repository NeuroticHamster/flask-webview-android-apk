#check to make sure updates are working
from flask import Flask, render_template, flash, request, redirect, url_for, session, send_from_directory
from wtforms import StringField, Form, validators, SelectField
from flask_wtf import FlaskForm
import hashlib
from sqlalchemy.orm import sessionmaker
import glob

import os

from sqlalchemy import create_engine, String, Integer, Column
from sqlalchemy.ext.declarative import declarative_base

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
sqlsession = sessionmaker(bind=engine)
sqlsession = sqlsession()

app = Flask(__name__, static_url_path='')


'''class QSelect(FlaskForm):
	qusernames = []
	namelist = sqlsession.query(logindb.username).all()
	passlist = sqlsession.query(logindb.password).all()
	for item, pitem in zip(namelist, passlist):
	
		if 'not_needed' in pitem:
			qusernames.append(item)
	
	print(qusernames)
	select = SelectField(*qusernames)'''

@app.route('/', methods=['GET', 'POST'])
def landing_page():
	sqlsession = sessionmaker(bind=engine)
	sqlsession = sqlsession()

	form = userMForm()

	
	if request.method == 'POST':
		print(request.form.get('username'))
		print(request.form.get('password'))
		username = str(request.form.get('username'))
		
		
		q = sqlsession.query(logindb.username.like(str(username)), logindb.password).all()
		for item in q:
			if item[0] == True:

				print(item[1])
				print('damnit')
				hashpass = hashlib.md5(str(request.form.get('password'))).hexdigest()
				print(hashpass)

				if hashpass == item[1]:
					print('its a match')
					session['username'] = username
					return redirect('/welcome')
	return render_template('/homepage.html', form=form)


class datavalues():
	qusernames = []
	namelist = sqlsession.query(logindb.username).all()
	passlist = sqlsession.query(logindb.password).all()
	for item, pitem in zip(namelist, passlist):

		if 'not_needed' in pitem:
			qusernames.append((item))


def squery(username):
	sqlsession = sessionmaker()
	newses = sqlsession()
	logs = logindb(username=username, password='not_needed')
	newses.add(logs)
	newses.commit()


@app.route('/quick_loggin', methods=['GET', 'POST'])
def secondpage():

	form = userMForm()
	#sfield = QSelect()
	#data = {'name':'shit', 'one':'shity', 'two':'shat'}
	choice = request.form.get('news2')
	print(request.form.get('username'))
	print(choice)
	
	if request.method == 'POST':
		
		username = request.form.get('username')
		choice = request.form.get('news2')
		
		if len(username) > 0:
			print(request.form.get('username'))
			squery(username)
			session['username'] = username
			return redirect(url_for('welcome'))
			

		elif choice != None:
			

			print(choice)
			session['username'] = choice
			return redirect(url_for('welcome'))

	return render_template('/quick_login.html', form=form, data=datavalues.qusernames)






@app.route('/registration', methods=['GET', 'POST'])
def register():
	
	sqlsession = sessionmaker(bind=engine)
	sqlsession = sqlsession()
	form = userMForm()
	if request.method == 'POST':
		print(request.form.get('username'))
		print(request.form.get('password'))
		password = str(request.form.get('password'))
		hashed_password = hashlib.md5(password.encode()).hexdigest()
		logs = logindb(username=str(request.form.get('username')), password=str(hashed_password))
		#logs = logindb(username=str(request.form.get('username')), password=str(password))
		sqlsession.add(logs)
		sqlsession.commit()
		print(hashed_password)
		print('hi')
		return redirect(url_for('landing_page'))
	return render_template('/register.html', form=form)


@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
	import os
	#h = os.listdir('/storage/emulated/0/jams')[0:20]
	h = os.listdir('/home/thedude/Music/')[0:20]
	navselect = request.form.get('navselect')
	print(navselect)

	if str(navselect) == 'schedule':
		return redirect('/schedule')
	if str(navselect) == 'streaming':
		return redirect('/streaming')
	if str(navselect) == 'home_media':
		return redirect('/home_media')
	if str(navselect) == 'personel':
		return redirect('/personel')
	if str(navselect) == 'meditation':
		return redirect('/meditation')
	if str(navselect) == 'logout':
		return redirect('/')
	#h = os.listdir('/storage/emulated/0/jams/')
	
	#h = glob.glob('/home/thedude/Music/*')
	'''new = []
	for item in h:
		new1 = item.split('/jams/')[1]
		new.append(new1)'''
	
	'''vals = requests.get('https://soundcloud.com/search?q=calm')
	newval = urllib2.urlopen('https://soundcloud.com/search?q=calm')
	htmls = newval.read()
	newlist = []
	for item in newval:
		if 'href=' in str(item):
			print(item)'''
	return render_template('/welcome.html', music_list=h)
@app.route('/streaming', methods=['GET', 'POST'])
def streaming():
	return 'streaming'
@app.route('/home_media', methods=['GET', 'POST'])
def home_media():
	return 'home_media'
@app.route('/personel', methods=['GET', 'POST'])
def personel():
	return 'personel'
@app.route('/meditation', methods=['GET', 'POST'])
def meditation():
	return 'meditation'
@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
	return 'schedule'
@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/new/<path:filename>')
def new(filename): 
	return send_from_directory('/home/thedude/Music/', filename)

'''@app.route('/new/<path:filename>')
def testaudio(filename):
	return send_from_directory('/storage/emulated/0/jams/', filename)'''



app.secret_key='just a check for now'
app.run(host='0.0.0.0')
