from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import Required, Email, Length

class LoginForm(Form):

    email = StringField('Email', validators=[Email(), Length(1, 64), Required()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')
