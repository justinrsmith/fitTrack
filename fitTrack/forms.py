from flask.ext.wtf import Form, SelectField


class WorkoutChoiceForm(Form):
    category = SelectField(u'', choices=())
    exercise = SelectField(u'', choices=())

class HistoryChoiceForm(Form):
    category = SelectField(u'', choices=())
    exercise = SelectField(u'', choices=())