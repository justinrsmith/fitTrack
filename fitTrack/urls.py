from fitTrack import app
import views as v

url = app.add_url_rule

url('/', 'login', v.login, methods = ['POST', 'GET'])
url('/home', 'home', v.home)
url('/track', 'track', v.track, methods = ['POST', 'GET'])
url('/login', 'login', v.login)
url('/add', 'add', v.add_exercise, methods = ['POST', 'GET'])
url('/me', 'me', v.me)