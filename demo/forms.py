from demo.models import User
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length, EqualTo, DataRequired, ValidationError


class RegisterForm(FlaskForm):
    '''
    RegisterForm is a class that inherits from FlaskForm.
    '''

    def validate_username(self, username):
            '''
            This function checks if the username is already in the database.
            Flask searches for validators in the form class by itself.
            '''
            user = User.query.filter_by(name=username.data).first()
            if user:
                raise ValidationError('Username already exists')

    username = StringField('Username', validators=[Length(2, 16), DataRequired()])
    password = StringField('Password', validators=[Length(2, 60), DataRequired()])
    password_confirm = StringField('Confirm Password', validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username')
    password = StringField('Password')
    submit = SubmitField('Login')