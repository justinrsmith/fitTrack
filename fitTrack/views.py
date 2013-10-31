from flask import render_template, request, redirect, flash, url_for, jsonify, session, g, abort, make_response
from fitTrack import app
import models as m
import json
from datetime import datetime
import hashlib
from fitTrack.forms import WorkoutChoiceForm, HistoryChoiceForm
from flask.views import MethodView
import os
import unicodedata


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

		"""
		This call and fucntion is so bad I should be ashamed. FIX
		"""
		a = request.form['email']
		a = unicodedata.normalize('NFKD', a).encode('ascii','ignore')
		pw = pw_fetch(a)
		if pw is not None:
			user_password = pw.pop(0)
			user_salt = pw.pop(0)
			user = m.user.query.filter_by(email = a)\
				.filter_by(password = user_password)\
				.filter_by(salt = user_salt).first()
			session['logged_in'] = True
			session['user_id'] = user.id
			flash('You were logged in') 
			return redirect(url_for('track'))
		else:
			error = 'Invalid Email'
			flash('Invalid credentials', error)
			session['logged_in'] = False
		"""
		AWFUL, honestly pathetic
		^^^^^
		"""

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
			print 'not exists'
			newUser = m.user(request.form['email'], pw_hash(request.form['password']),
				pw_salt(),
				request.form['firstName'], request.form['lastName'],
				request.form['age'], request.form['location'])
			m.db.session.add(newUser)
			m.db.session.commit()
			return redirect(url_for('track'))

	return render_template('create.html')


def track():
    """
    Create dropdowns
    User submits their data
    """
    if session['logged_in'] == False:
        abort(401)
    else:
        CATEGORY_LIST = []
        a = m.category.query.filter_by(userID=g.user).all()
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

            exHeader = m.exHeader(g.user, chosen_category, chosen_exercise,
                dt)
            m.db.session.add(exHeader)
            m.db.session.commit()
            exH = m.exHeader.query.filter_by(userID = g.user).order_by(
                m.exHeader.id.desc()).first()
            exH.id2 = exH.id

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
		print 'hi'
		a = ''.join(c for c in request.form.values() if c not in "[']")

		#f = m.exLine.query.filter_by(submitted=a).all()
		f = m.exLine.query.all()
		for x in a:
			print x

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
		r = m.exHeader.query.filter_by(userID=g.user).order_by(
			m.exHeader.submitted.desc()).all()

		CATEGORY_LIST = []
		a = m.category.query.filter_by(userID=g.user).all()
		for x in a:
			CATEGORY_LIST.append({'categoryID': x.id, 'name': x.name})

		form = HistoryChoiceForm(request.form)
		form.category.choices = [('', '--- Select One ---')] + [
			(x['categoryID'], x['name']) for x in CATEGORY_LIST]
		chosen_category = None
		chosen_exercise = None
		context = {
	        'form': form,
	        'chosen_category': chosen_category,
	        'chosen_exercise': chosen_exercise,
    	}

		if request.method == 'POST':
			chosen_category = form.category.data
			chosen_exercise = form.exercise.data

			dt = datetime.now()

			return render_template('me.html',
				recent=r,
				user=u,
				**context
				)

	return render_template('me.html',
		recent=r,
		user=u,
		**context
		)


def control():
	"""
	User can change settings
	"""

	if request.method == 'POST':
		u = m.user.query.filter_by(id=g.user).first()
		if 'updatepw' in request.form:
			print 'updatepw'			
			pwcurrent = pw_fetch(u.email)
			pwhash = pw_hash(request.form['currentpw'])

			if pwhash == pwcurrent[0]:
				user = m.user.query.filter_by(id = g.user)\
					.filter_by(password = pwcurrent[0])\
					.filter_by(salt = pwcurrent[1]).first() 
				newpw = pw_hash(request.form['newpw'])
				user.password = newpw
				m.db.session.add(user)
				m.db.session.commit()
			else:
				flash('Invalid current password')
				redirect('control.html')
		if 'newemail' in request.form:
			print 'newemail'
			pwcurrent = pw_fetch(u.email)
			user = m.user.query.filter_by(id = g.user)\
					.filter_by(password = pwcurrent[0])\
					.filter_by(salt = pwcurrent[1]).first() 
			user.email = request.form['newemail']
			m.db.session.add(user)
			m.db.session.commit()
		else:
			flash('Invalid current password')
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

def pw_fetch(email_in):
	"""
	Fetch pw
	"""

	user = m.user.query.filter_by(email=email_in).first()

	if not user:
		#flash('Account does not exist. Please create an account.')
		return None
	else:
		credList = []
		credList.append(user.password)
		credList.append(user.salt)
		print credList

		return credList