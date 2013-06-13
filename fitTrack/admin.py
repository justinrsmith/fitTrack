from fitTrack import app
from flask import Flask, request, redirect
from flask.ext.admin import Admin, BaseView, expose
from flask.ext.admin.base import AdminIndexView
from flask.ext.admin.contrib.sqlamodel import ModelView
from flask.ext.admin.model import BaseModelView
from flask.ext.admin.model.form import InlineFormAdmin
from fitTrack import models as m
from wtforms.fields import SelectField

from flask import g

class AdminHome(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html', perms=g.identity.provides)
                
    def is_accessible(self):
        if g.identity.can(permissions.admin_access):
            return True
                        
class exerciseAdmin(ModelView):
    name = 'Exercise'
    can_delete = False
       
    def is_accessible(self):
        return True

class workoutAdmin(ModelView):
    name = 'Workout'

    def is_accessible(self):
        return True            

class userAdmin(ModelView):
	name = 'User'
	
	def is_accessible(self):
		return True
                                                
admin = Admin(app)
admin.add_view(exerciseAdmin(m.Exercise, m.db.session))
admin.add_view(workoutAdmin(m.Workout, m.db.session))
admin.add_view(userAdmin(m.User, m.db.session))