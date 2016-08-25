from datetime import datetime
from flask import render_template, redirect, url_for, session
from . import main
from .. import db
from .forms import NameForm, EditProfileForm
from ..models import User, Role
from ..email import send_mail
from flask_login import current_user


@main.route('/', methods=['GET', 'POST'])
def home():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
          user = User(username=form.name.data)
          db.session.add(user)
          db.session.commit()
          session['known'] = False
          send_mail('christianyang@wistronits.com', 'New User', 'mail/new_user', user=user)
        else:
          session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('main.home'))
    return render_template('index.html',
                           username=session.get('name'),
                           form=form,
                           known=session.get('known', False),
                           current_time=datetime.utcnow())

@main.route('/user/<username>')
def user(username):
  user = User.query.filter_by(username=username).first()
  if user is None:
    abort(404)
  return render_template('user.html', user=user)

