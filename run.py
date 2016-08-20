from flask import Flask
from flask import render_template
from flask import g
from flask_script import Manager
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)
manager = Manager(app)

app.config['DEBUG'] = True


@app.before_request
def before_first_request():
    g.user = 'Niel'


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', msg=e)


@app.errorhandler(505)
def server_internal_error(e):
    return render_template('505.html', s_msg=e)


@app.route('/')
def home():
    return render_template('index.html', name=g.user)

if __name__ == '__main__':
    manager.run()
