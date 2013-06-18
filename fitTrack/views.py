from flask import render_template, request, redirect, flash, url_for, session, g, abort
from fitTrack import app
import models as m
import json
from datetime import datetime

def auth(form):

	if 'email' in request.form:
		u = m.User.query.filter_by(email = form['email']).first()

		if u:
			session['user'] = u.id
			print session['user']
			return True

	return False

@app.before_request
def something():

	login_url = url_for('login')
	
	if request.path == login_url:
		return
	elif not session.get('logged_in', False):
		pass
		#return redirect(login_url)

	g.user = session['user_id']

def login():
	"""Handle logging in of users"""

	session['logged_in'] = False
	if request.method == 'POST':
		user = m.User.query.filter_by(email = request.form['email'])\
		.filter_by(password = request.form['password']).first() 
		#print session['logged_in']
		if user is None:
			error = 'Invalid Email'
			flash('Invalid credentials', error)
			session['logged_in'] = False
		else:
			session['logged_in'] = True
			session['user_id'] = user.id
			flash('You were logged in')

			return redirect(url_for('home'))
	
	return render_template('login.html')

def logout():

	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('login'))

def create():
	"""
	User created login
	"""

	#print request.form['newEmail']
	#if request.method == 'POST':
	#	email = request.form['newEmail']
	return render_template('create.html')


def home():
    """Home page"""
    #print session['logged_in']
    print g.user
    if session['logged_in'] == False:
    	abort(404)
    else:
   		
   		#print g.user
   		print 'am i here?'
		return render_template('home.html')


def track():
    """Gather exercise details, insert into DB"""
    
    if session['logged_in'] == False:
    	abort(401)

    if request.method == 'POST':

    	dt = datetime.now()
    	workout = m.Workout(request.form['exercise'], request.form['sets'], request.form[
            'reps'], request.form['weight'], request.form[
            'category'], g.user, dt)
    	m.db.session.add(workout)
    	m.db.session.commit()

    exercise = m.Exercise.query.filter_by(userid = g.user).all()
    workout = m.Workout.query.all()

    return render_template('track.html',
    	workout=workout,
    	exercise=exercise)

def add_exercise():
	"""
	Add user specific/created exercise to DB
	"""

	if request.method == 'POST':
		newExercise = m.Exercise(request.form['category'], 
			request.form['workout'], g.user)
		m.db.session.add(newExercise)
		m.db.session.commit()

	return render_template('add.html')

def me():
	"""
	User summary info
	"""
	print 'me'
	print session['logged_in']
	if session['logged_in'] == False:
		abort(401)
	else:
		workout = m.Workout.query.filter_by(userid = g.user).all()

	return render_template('me.html',
		workout=workout)