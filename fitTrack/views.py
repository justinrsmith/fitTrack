from flask import render_template, request, redirect, flash, url_for, jsonify, session, g, abort, make_response
from fitTrack import app
import models as m
import json
from datetime import datetime
import hashlib
from fitTrack.forms import WorkoutChoiceForm
from flask.views import MethodView
from flask.ext.mail import Mail
from flask.ext.mail import Message
import os


def auth(form):

	if 'email' in request.form:
		u = m.user.query.filter_by(email = form['email']).first()

		if u:
			session['user'] = u.id
			return True

	return False


@app.before_request
def something():

	login_url = url_for('login')
	
	if request.path == login_url:
		return
	elif not session.get('logged_in', False):
		pass

	if not request.path == url_for('create'):
		g.user = session['user_id']


def login():
	"""Handle logging in of users"""

	session['logged_in'] = False
	
	if request.method == 'POST':

		pw = pw_fetch(request.form['password'])
		print pw[0]
		print pw[1]
		user = m.user.query.filter_by(email = request.form['email'])\
		.filter_by(password = pw[0])\
		.filter_by(salt = pw[1]).first() 

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

	if request.method == 'POST':
		exists = m.user.query.filter_by(email=request.form['email']).first()

		if not exists:
			newUser = m.user(request.form['email'], pw_hash(request.form['password']),
				pw_salt(),
				request.form['firstName'], request.form['lastName'],
				request.form['age'], request.form['location'])
			m.db.session.add(newUser)
			m.db.session.commit()


		#mail = Mail(app)
		#mail.init_app(app)
		
		#msg = Message('Hello',
		#	sender='justinrsmith88@gmail.com',
		#	recipients=['justinrsmith88@gmail.com'])
		#msg.body='body'
		#mail.send(msg)
		#return 'sent'

	return render_template('create.html')


def home():
    """Home page"""

    if session['logged_in'] == False:
    	abort(404)
    else:
   		print g.user
		return render_template('home.html')


def track():
    """
    Create dropdowns
    User submits their data
    """

    CATEGORY_LIST = []
    a = m.category.query.filter_by(userID=2).all()
    for x in a:
        CATEGORY_LIST.append({'categoryID': x.id, 'name': x.name})

    form = WorkoutChoiceForm(request.form)
    form.category.choices = [('', '--- Select One ---')] + [
        (x['categoryID'], x['name']) for x in CATEGORY_LIST]
    chosen_category = None
    chosen_exercise = None

    if request.method == 'POST':
        chosen_category = form.category.data
        chosen_exercise = form.exercise.data

        dt = datetime.now()
        print chosen_category
        exHeader = m.exHeader(g.user, chosen_category, chosen_exercise)
        m.db.session.add(exHeader)
        m.db.session.commit()
        exH = m.exHeader.query.filter_by(userID = g.user).first()
        

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


@app.route('/post', methods=['GET', 'POST'])
def post_request():
	
	if session['logged_in'] == False:
		abort(401)
	else:
		a = ''.join(c for c in request.form.values() if c not in "[']")

		f = m.exLine.query.filter_by(submitted=a).all()

	return render_template('test.html',
		filter=f)


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

		for a in x:
			print a.header.category

	return render_template('me.html',
		recent=x,
		user=u
		)

def control():
	"""
	User can change settings
	"""

	if request.method == 'POST':
		print 'post here'
		u = m.user.query.filter_by(id=g.user).first()
		pwcurrent = pw_fetch(u.email)
		pwhash = pw_hash(request.form['currentpw'])

		if pwhash == pwcurrent[0]:
			user = m.user.query.filter_by(id = g.user)\
				.filter_by(password = pwcurrent[0])\
				.filter_by(salt = pwcurrent[1]).first() 
		else:
			flash("Invalid current password")
			redirect('control.html')

	return render_template('control.html')


def pw_salt():
	"""
	Handle creating salt
	"""

	salt = os.urandom(16).encode('base_64')

	return salt

def pw_hash(pwIn):
	"""
	Handle creating hash
	"""

	hash = hashlib.md5(pwIn).hexdigest()

	return hash

def pw_fetch(emailIn):
	"""
	Fetch pw
	"""

	user = m.user.query.filter_by(email=emailIn).first()
	
	credList = []
	credList.append(user.password)
	credList.append(user.salt)

	return credList

