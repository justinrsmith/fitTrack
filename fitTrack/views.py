from flask import render_template, request, redirect, flash, url_for, session, g, abort
from fitTrack import app
import models as m

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

	if not session.has_key('user'):
		return redirect(url_for('login'))
		#pass
	else:
		g.user = session['user']

#@app.errorhandler(404)
#def page_not_found(e):
#	return render_template('404.html'), 404

def login():
	"""Handle logging in of users"""
	
	if request.method == 'POST':
		user = m.User.query.filter_by(email = request.form['email']).first() 

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

def home():
    """Home page"""
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
    	workout = m.workout(request.form['exercise'], request.form['sets'], request.form[
            'reps'], request.form['weight'], request.form[
            'category'])
    	m.db.session.add(workout)
    	m.db.session.commit()

    workout = m.Workout.query.all()
    exercise = m.Exercise.query.all()

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

	if session['logged_in'] == False:
		abort(401)

	return render_template('me.html')