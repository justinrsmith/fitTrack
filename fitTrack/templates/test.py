from fitTrack import models as models

user = m.User.query.filter_by(email='justinrsmith88@gmail.com')

print user.id