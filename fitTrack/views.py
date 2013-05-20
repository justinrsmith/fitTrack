from flask import render_template, request, redirect, flash, url_for
from fitTrack import app
import models as m

def home():
    """Home page"""
    return render_template('home.html')

def track():
    """A list of all employees"""
    exercise = m.main.query.all()

    return render_template('track.html',exercise=exercise)