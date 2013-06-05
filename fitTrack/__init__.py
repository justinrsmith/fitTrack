from flask import Flask

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fit.db'

app.secret_key = 'notsosecret'

#from fitTrack import views
import admin
import urls
