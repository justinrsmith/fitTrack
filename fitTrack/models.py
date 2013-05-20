from fitTrack import app
from flask.ext.sqlalchemy import SQLAlchemy

from sqlalchemy.orm.interfaces import MapperExtension

db = SQLAlchemy(app)

class main(db.Model):
    """The class/table for employee records

    first_name (string)
    last_name (string)"""
    
    id = db.Column(db.Integer(), primary_key=True)
    exercise = db.Column(db.String(25))

    def __init__(self,exercise):
       # self.id = id
        self.exercise = exercise

    def __repr__(self):
    #    """The default way records are represented"""
        return self.exercise