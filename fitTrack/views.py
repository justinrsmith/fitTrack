from flask import render_template, request, redirect, flash, url_for
from fitTrack import app
import models as m

def home():
    """Home page"""
    #return "hi"
    return render_template('home.html')

def track():
    """Gather exercise details, insert into DB"""
   
    if request.method == 'POST':
    	print [request.form['exercise']]
    	main = m.main(request.form['exercise'])
    	m.db.session.add(main)
    	m.db.session.commit()

    exercise = m.main.query.all()

    return render_template('track.html',exercise=exercise)