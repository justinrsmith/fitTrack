from flask import render_template, request, redirect, flash, url_for, jsonify, session, g, abort, make_response
from fitTrack import app
import models as m
import json
from datetime import datetime
import hashlib
from fitTrack.forms import WorkoutChoiceForm

from flask.views import MethodView

def auth(form):

	if 'email' in request.form:
		u = m.user.query.filter_by(email = form['email']).first()

		if u:
			session['user'] = u.id
			#print session['user']
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

	if not request.path == url_for('create'):
		g.user = session['user_id']




def login():
	"""Handle logging in of users"""

	session['logged_in'] = False
	
	if request.method == 'POST':

		pw = hashConvert(request.form['password'])
		user = m.user.query.filter_by(email = request.form['email'])\
		.filter_by(password = pw).first() 
		#print session['logged_in']

		if user is None:
			error = 'Invalid Email'
			flash('Invalid credentials', error)
			session['logged_in'] = False
		else:
			session['logged_in'] = True
			session['user_id'] = user.id
			flash('You were logged in')

			return redirect(url_for('track'))
	
	return render_template('login.html')


def logout():

	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('login'))

def create():
	"""
	User created login
	"""

	salt = 'gnarlysaltd00d'

	if request.method == 'POST':
		newUser = m.user(request.form['email'], hashConvert(request.form['password']),
			request.form['firstName'], request.form['lastName'],
			request.form['age'], request.form['location'])
		m.db.session.add(newUser)
		m.db.session.commit()
		print 'post'
	return render_template('create.html')


def home():
    """Home page"""

    if session['logged_in'] == False:
    	abort(404)
    else:
   		print g.user
		return render_template('home.html')




#print CATEGORY_LIST

def track():

    """
    Render a vehicle selection form and handle form submission
    """

    CATEGORY_LIST = []

    a = m.category.query.filter_by(userID=2).all()
    for x in a:
        CATEGORY_LIST.append({'categoryID': x.id, 'name': x.name})

    form = WorkoutChoiceForm(request.form)

    form.category.choices = [('', '--- Select One ---')] + [
        (x['categoryID'], x['name']) for x in CATEGORY_LIST]
    #print form.make.choices
    chosen_category = None
    chosen_exercise = None

    if request.method == 'POST':
        chosen_category = form.category.data
        chosen_exercise = form.exercise.data

        dt = datetime.now()
        #dt = d.strftime("%Y-%m-%d %H:%M:%S")

        exHeader = m.exHeader(g.user, 1, chosen_exercise)
        m.db.session.add(exHeader)
        m.db.session.commit()
        #this is wrong fix just temp
        exH = m.exHeader.query.filter_by(userID = g.user).first()
        
        #m.db.session.add(exH)

        exL = m.exLine(exH.id, request.form['reps'], request.form['sets'],
            request.form['weight'], dt)

        m.db.session.add(exL)
        m.db.session.commit()

    context = {
        'form': form,
        'chosen_category': chosen_category,
        'chosen_exercise': chosen_exercise,
    }
    return render_template('track.html', **context)


class ModelsAPI(MethodView):
    def get(self, categoryID):
        """
        Handle a GET request at /models/<make_id>/
        Return a list of 2-tuples (<model id>, <model name>)
        """
        b = m.exercise.query.all()
        EXERCISE_LIST = []
        for y in b:
            EXERCISE_LIST.append({'exerciseID': y.id, 'categoryID': y.categoryID, 'name': y.name})

        data = [
            (x['exerciseID'], x['name']) for x in EXERCISE_LIST
            if x['categoryID'] == categoryID]
        response = make_response(json.dumps(data))
        response.content_type = 'application/json'
        return response


def add_exercise():
	"""
	Add user specific/created exercise to DB
	"""

	if request.method == 'POST':
		newCategory = m.category(request.form['category'], g.user)
		m.db.session.add(newCategory)
		m.db.session.commit()
		newExercise = m.exercise(request.form['exercise'], g.user, newCategory.id)
		m.db.session.add(newExercise)
		m.db.session.commit()
		
		print newCategory.id

	return render_template('add.html')


def me():
	"""
	User summary info
	"""

	if session['logged_in'] == False:
		abort(401)
	else:
		#user info
		u = m.user.query.filter_by(id=g.user)

		#recent exercises
		x = m.exLine.query.all()

	return render_template('me.html',
		recent=x,
		)

def hashConvert(pwIn):
	"""
	Handle creating/reading salt/hash of pws
	"""

	salt = '1337h4x0rz'
	return hashlib.md5(salt + pwIn).hexdigest()