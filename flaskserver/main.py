#check to make sure updates are working
from flask import Flask, render_template, flash, request, redirect, url_for
from wtforms import StringField, Form, validators
from flask_wtf import FlaskForm

from sqlalchemy.orm import sessionmaker



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

app = Flask(__name__, static_url_path='')



@app.route('/', methods=['GET', 'POST'])
def laanding_page():

	form = userMForm()

	
	if request.method == 'POST':
		print(request.form.get('username'))
		print(request.form.get('password'))
	return render_template('/homepage.html', form=form)




@app.route('/quick_loggin', methods=['GET', 'POST'])
def secondpage():
	form = QMForm()
	
	
	if request.method == 'POST':
		print(request.form.get('name'))
		logs = quserform(name=str(request.form.get('name')))
		session.add(logs)
		session.commit()
		flash("Successfully created a new book")
		return redirect(url_for('welcome'))

	return render_template('/quick_login.html', form=form)






@app.route('/registration', methods=['GET', 'POST'])
def register():
	form = userMForm()
	if request.method == 'POST':
		print(request.form.get('username'))
		print(request.form.get('password'))

		logs = logindb(username=str(request.form.get('username')), password=str(request.form.get('password')))
		session.add(logs)
		session.commit()
		return redirect(url_for('welcome'))
	return render_template('/register.html', form=form)


@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
	return 'needs work'	


@app.route('/')
def root():
    return app.send_static_file('index.html')
app.secret_key='just a check for now'
app.run(host='0.0.0.0')
