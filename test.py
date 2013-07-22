from fitTrack import models as m

x = m.exLine.query.all()

for a in x:
	print a.submitted

for b in x:
	print a.line.categoryID