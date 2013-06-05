from flask import render_template, request, redirect, flash, url_for, session
from fitTrack import app
import models as m

def login():
	"""Handle logging in of users"""
	
	#if request.method == 'POST':
	#	print 'hi'

	if request.method == 'POST':
		print request.form['email']
		user = m.user.query.filter_by(email = request.form['email'])#, 
		#	password=request.form['password']))

		#email = user.first().email
		#password = user.first().password
		
		if user.first() is None:
			error = 'Invalid Email'
			flash('Invalid credentials', error)
	#	elif not password:
	#		error = 'Invalid password'
		else:
			session['logged_in'] = True
			flash('You were logged in')

			return redirect(url_for('home'))

	return render_template('login.html')

def home():
    """Home page"""

    return render_template('home.html')


def track():
    """Gather exercise details, insert into DB"""
   
    if request.method == 'POST':
    	workout = m.workout(request.form['exercise'], request.form['sets'], request.form[
            'reps'], request.form['weight'], request.form[
            'category'])
    	m.db.session.add(workout)
    	m.db.session.commit()

    workout = m.workout.query.all()
    exercise = m.exercise.query.all()

    return render_template('track.html',
    	workout=workout,
    	exercise=exercise)