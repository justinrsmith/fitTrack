from fitTrack import app
from flask.ext.sqlalchemy import SQLAlchemy

from sqlalchemy.orm.interfaces import MapperExtension
from sqlalchemy import and_
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref

db = SQLAlchemy(app)


class user(db.Model):
    """The class/table for user data

    id int
    email string
    password string"""

    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(40))
    password = db.Column(db.String(16))
    salt = db.Column(db.String(64))
    firstName = db.Column(db.String(50))
    lastName = db.Column(db.String(50))
    age = db.Column(db.Integer())
    location = db.Column(db.String(30))

    def __init__(self, email, password, salt, firstName, lastName,
        age, location):

        self.email = email
        self.password = password
        self.salt = salt
        self.firstName = firstName
        self.lastName = lastName
        self.age = age
        self.location = location

    def __repr__(self):

        return id


class category(db.Model):

    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    userID = db.Column(db.Integer)

    def __init__(self, name, userID):
        self.name = name
        self.userID = userID

    def __repr__(self):

        return self.name


class exercise(db.Model):

    __tablename__ = 'exercise'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(10))
    userID = db.Column(db.Integer())
    categoryID = db.Column(db.Integer())

    def __init__(self, name, userID, categoryID):

        self.name = name
        self.userID = userID
        self.categoryID = categoryID

    def __repr__(self):
        return self.name


class exHeader(db.Model):

    __tablename__ = 'exHeader'
    id = db.Column(db.Integer(), primary_key=True)
    userID = db.Column(db.Integer())
    categoryID = db.Column(db.Integer(), db.ForeignKey(category.id))
    exerciseID = db.Column(db.Integer(), db.ForeignKey(exercise.id))
    category = relationship('category')
    exercise = relationship('exercise')
    
    def __init__(self, userID, categoryID, exerciseID):

        self.userID = userID
        self.categoryID = categoryID
        self.exerciseID = exerciseID

    def __repr__(self):

        return str(self.id)


class exLine(db.Model):

    __tablename__ = 'exLine'
    id = db.Column(db.Integer(), primary_key=True)
    exHeaderID = db.Column(db.Integer(), db.ForeignKey(exHeader.id))
    reps = db.Column(db.Integer())
    sets = db.Column(db.Integer())
    weight = db.Column(db.Integer())
    submitted = db.Column(db.Date())
    header = relationship('exHeader')

    def __init__(self, exHeaderID, reps, sets, weight, submitted):

        self.exHeaderID = exHeaderID
        self.reps = reps
        self.sets = sets
        self.weight = weight
        self.submitted = submitted

    def __repr__(self):

        return str(self.exHeaderID)










		