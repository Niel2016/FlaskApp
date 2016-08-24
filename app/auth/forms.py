from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import Required, Email, Length, Regexp, EqualTo
from ..models import User



class LoginForm(Form):

    email = StringField('Email', validators=[Email(), Length(1, 64), Required()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

class RegistrationForm(Form):

    email = StringField('Email', validators=[Email(), Length(1, 64), Required()])
    username = StringField('Username', validators=[Required(), Length(1, 64),
                           Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                  'Usernames must have only letters, '
                                  'numbers, dots or underscores')])
    password = PasswordField('Password', validators=[Required(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

class ChangePasswordForm(Form):

    oldPassword = PasswordField('Old Password', validators=[Required()])
    password = PasswordField('New Password', validators=[Required(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Change Password')

class ChangeEmailRequestForm(Form):
    
    email = StringField('New email', validators=[Email(), Length(1, 64), Required()])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Update Email Address')

class ResetPasswordRequestForm(Form):

    email = StringField('Email', validators=[Email(), Length(1, 64), Required()])
    submit = SubmitField('Reset Password')

class ResetPasswordForm(Form):

    email = StringField('Email', validators=[Email(), Length(1, 64), Required()])
    password = PasswordField('New Password', validators=[Required(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Reset Password')

