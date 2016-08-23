from flask import render_template, redirect, url_for, session, flash, request
from . import auth
from .forms import LoginForm, RegistrationForm
from ..models import User, Role
from flask_login import login_user, logout_user
from .. import db

@auth.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user is not None and user.verify_password(form.password.data):
      login_user(user, form.remember_me.data)
      return redirect(request.args.get('next') or url_for('main.home'))
    flash('Invalid email or password.')
  return render_template('auth/login.html', form=form)

@auth.route('/logout')
def logout():
  logout_user()
  flash('You have been logged out.')
  return redirect(url_for('main.home'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
  form = RegistrationForm()
  if form.validate_on_submit():
    user = User(username=form.username.data,
                email=form.email.data,
                password=form.password.data)
    db.session.add(user)
    db.session.commit()
    flash('You can now login.')
    return redirect(url_for('auth.login'))
  return render_template('auth/register.html',
                         form=form)

