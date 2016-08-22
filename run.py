from datetime import datetime
import os
from flask import Flask, flash
from flask import session, redirect, url_for
from flask import render_template
from flask_script import Manager, Shell
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

#------------------------------------configs---------------------------------
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'HARD TO GUESS'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,
                                                                    'data.sqlite')
#----------------------------------------------------------------------------
bootstrap = Bootstrap(app)
manager = Manager(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


def make_shell_context():
  return dict(db=db, app=app, User=User, Role=Role)
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

#------------------------------------request hooks---------------------------
# @app.before_request
# def before_first_request():
#     g.user = 'Nielss'

#------------------------------------models---------------------------------
class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), unique=True, index=True)
  email = db.Column(db.String(128))
  role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

  def __repr__(self):
    return 'User <%r>' % self.username


class Role(db.Model):
  __tablename__ = 'roles'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(64), unique=True, index=True)
  users = db.relationship('User', backref='role')

  def __repr__(self):
    return 'Role <%r>' % self.name
#------------------------------------forms---------------------------------
class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

#------------------------------------views---------------------------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', msg=e)


@app.errorhandler(500)
def server_internal_error(e):
    return render_template('500.html', s_msg=e)


@app.route('/', methods=['GET', 'POST'])
def home():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
          user = User(username=form.name.data)
          db.session.add(user)
          db.session.commit()
          session['known'] = False
        else:
          session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('home'))
    return render_template('index.html',
                           username=session.get('name'),
                           form=form,
                           known=session.get('known', False),
                           current_time=datetime.utcnow())
#--------------------------------------------------------------------------

if __name__ == '__main__':
    manager.run()

