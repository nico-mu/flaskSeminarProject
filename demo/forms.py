from demo.models import User
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
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
    password = PasswordField('Password', validators=[Length(2, 60), DataRequired()])
    password_confirm = PasswordField('Confirm Password', validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Login')
    remember_me = StringField('Remember Me')

class RemoveUserForm(FlaskForm):
    submit = SubmitField('Remove User')

class AddUserForm(FlaskForm):
    submit = SubmitField('Add User')
    name = StringField('Name')
    password = StringField('Password')
    admin = BooleanField('Admin')