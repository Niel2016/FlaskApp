from datetime import datetime
from flask import Flask, flash
from flask import session, redirect, url_for
from flask import render_template
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
bootstrap = Bootstrap(app)
manager = Manager(app)
moment = Moment(app)
db = SQLAlchemy(app)

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'HARD TO GUESS'
# @app.before_request
# def before_first_request():
#     g.user = 'Nielss'


class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


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
        oldname = session.get('name')
        if oldname is not None and oldname != form.name.data:
            flash('Looks like you have changed your name.')
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('home'))
    return render_template('index.html',
                           username=session.get('name'),
                           form=form,
                           current_time=datetime.utcnow())

if __name__ == '__main__':
    manager.run()
