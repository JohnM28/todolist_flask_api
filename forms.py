from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class Insert(FlaskForm):
    id = IntegerField('id')
    todo_item = StringField('todo_item')
    status = StringField('status')
    submit = SubmitField('insert')


