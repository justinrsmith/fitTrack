from fitTrack import app
from flask.ext.sqlalchemy import SQLAlchemy

from sqlalchemy.orm.interfaces import MapperExtension
from sqlalchemy import and_
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref

db = SQLAlchemy(app)

class Workout(db.Model):
    """The class/table for excercise data

    id int
    excercise string
    sets int
    reps int
    weight int"""
    
    id = db.Column(db.Integer(), primary_key=True)
    exercise = db.Column(db.String(25))
    sets = db.Column(db.Integer())
    reps = db.Column(db.Integer())
    weight = db.Column(db.Integer())
    category = db.Column(db.String(30))

    def __init__(self, exercise, sets, reps, weight, category):

        self.exercise = exercise
        self.sets = sets
        self.reps = reps
        self.weight = weight
        self.category = category

    def __repr__(self):

        return self.exercise

class User(db.Model):
    """The class/table for user data

    id int
    email string
    password string"""

    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(40))
    password = db.Column(db.String(16))

    def __init__(self, email, password):

        self.email = email
        self.password = password

    def __repr__(self):

        return id

class Exercise(db.Model):

    #__tablenane__ = 'exercise'
    id = db.Column(db.Integer(), primary_key=True)
    category = db.Column(db.String(30))
    workout = db.Column(db.String(30))
    userid = db.Column(db.Integer())

    def __init__(self, category, workout, userid):

        self.category = category
        self.workout = workout
        self.userid = userid
		