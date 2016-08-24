from flask import render_template, redirect, url_for, session, flash, request
from . import auth
from .forms import LoginForm, RegistrationForm, ChangePasswordForm, ResetPasswordRequestForm, ResetPasswordForm, ChangeEmailRequestForm
from ..models import User, Role
from flask_login import login_user, logout_user,current_user, login_required
from .. import db
from ..email import send_mail

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
    token = user.generate_confirmation_token()
    send_mail(user.email, 
             'Confirm Your Account', 
             'auth/email/confirm', 
             user=user, 
             token=token)
    flash('A confirmation email has been sent to you by email.')
    return redirect(url_for('main.home'))
  return render_template('auth/register.html',
                         form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
  if current_user.confirmed:
    return redirect(url_for('main.home'))
  elif current_user.confirm(token):
    flash('You have confirmed your account. Thanks!')
  else:
    flash('The confirmation link is invalid or has expired.')
  return redirect(url_for('main.home'))


@auth.before_app_request
def before_request():
  if current_user.is_authenticated\
    and not current_user.confirmed\
    and request.endpoint[:5] != 'auth.':
    return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
  if current_user.is_anonymous or current_user.confirmed:
    return redirect('main.home')
  return render_template('auth/unconfirmed.html')


@auth.route('/confirm')
@login_required
def resend_confirmation():
  token = current_user.generate_confirmation_token()
  send_mail(current_user.email, 
             'Confirm Your Account', 
             'auth/email/confirm', 
             user=current_user, 
             token=token)
  flash('A new confirmation email has been sent to you by email.')
  return redirect(url_for('main.home'))

@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
  form = ChangePasswordForm()
  if form.validate_on_submit():
    if current_user.verify_password(form.oldPassword.data):
      current_user.password = form.password.data
      db.session.add(current_user)
      db.session.commit()
      flash('Your password has been updated.')
      return redirect(url_for('main.home'))
    else:
      flash('Invalid password')
  return render_template('auth/changepassword.html', form=form)

@auth.route('/reset', methods=['GET', 'POST'])
def reset_password_request():
  if not current_user.is_anonymous:
    return redirect(url_for('main.home'))
  form = ResetPasswordRequestForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user:
      token = user.generate_reset_token()
      send_mail(user.email, 
             'Confirm Your new password', 
             'auth/email/reset_password', 
             user=user, 
             token=token,
             next=request.args.get('next'))
      flash('An email with instructions to reset your password has been '
              'sent to you.')
      return redirect(url_for('auth.login'))
    else:
      flash("Cant't find user with <%r>" % form.email.data)
  return render_template('auth/resetpassword.html', form=form)

@auth.route('/reset/<token>', methods=['GET', 'POST'])
def reset_password(token):
  if not current_user.is_anonymous:
    return redirect(url_for('main.home'))
  form = ResetPasswordForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user is None:
      return redirect(url_for('main.index'))
    if user.reset(token, form.password.data):
      flash('Your password has updated.')
      return redirect(url_for('auth.login'))
    else:
      return redirect(url_for('main.home'))
  return render_template('auth/resetpassword.html', form=form)

@auth.route('/change-email', methods=['GET', 'POST'])
@login_required
def reset_email_request():
  form = ChangeEmailRequestForm()
  if form.validate_on_submit():
    if current_user.verify_password(form.password.data):
      new_email = form.email.data
      token = current_user.generate_email_change_token(new_email)
      send_mail(new_email, 
             'Confirm Your email address', 
             'auth/email/reset_email', 
             user=current_user, 
             token=token
             )
      flash('An email with instructions to reset your email has been '
              'sent to you.')
      return redirect(url_for('main.home'))
  return render_template('auth/changeemail.html', form=form)

@auth.route('/change-email/<token>', methods=['GET', 'POST'])
@login_required
def reset_email(token):
  if current_user.reset_email(token):
    flash('Your email has updated.')
  else:
    flash('Invalid request.')
  return redirect(url_for('main.home'))


