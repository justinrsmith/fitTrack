from fitTrack import app
import views as v

url = app.add_url_rule

url('/', 'login', v.login, methods = ['POST', 'GET'])
url('/logout', 'logout', v.logout)
#url('/home', 'home', v.home)
url('/track', 'track', view_func=v.track, methods = ['POST', 'GET'])
url('/login', 'login', v.login)
url('/add', 'add', v.add_exercise, methods = ['POST', 'GET'])
url('/me', 'me', v.me)
url('/create', 'create', v.create, methods = ['POST', 'GET'])
#url('/_add_numbers', 'addNum', v.add_numbers, methods = ['POST', 'GET'])
url('/models/<int:categoryID>/', view_func=v.ModelsAPI.as_view('models_api'), methods=['GET'])