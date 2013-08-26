from flask import Flask

#import mail

#mail = Mail()

app = Flask(
	__name__,
	template_folder='templates',
	static_folder='static',
	)

#mail.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fit.db'

app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USE_TLS=False,
	MAIL_USERNAME = 'justinrsmith88@gmail.com',
	MAIL_PASSWORD = '********',
	DEFAULT_MAIL_SENDER = 'justinrsmith88@gmail.com'
	)

app.secret_key = 'notsosecret'

#from fitTrack import views
import admin
import urls
