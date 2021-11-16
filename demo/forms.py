from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class RegisterForm(FlaskForm):
    username = StringField('Username')
    password = StringField('Password')
    password_confirm = StringField('Confirm Password')
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username')
    password = StringField('Password')
    submit = SubmitField('Login')