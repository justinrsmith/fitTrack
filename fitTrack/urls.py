from fitTrack import app
import views as v

url = app.add_url_rule

url('/', 'home', v.home)
url('/track', 'track', v.track)