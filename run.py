from datetime import datetime
from flask import Flask
from flask import render_template
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment

app = Flask(__name__)
bootstrap = Bootstrap(app)
manager = Manager(app)
moment = Moment(app)

app.config['DEBUG'] = True


# @app.before_request
# def before_first_request():
#     g.user = 'Nielss'


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', msg=e)


@app.errorhandler(500)
def server_internal_error(e):
    return render_template('500.html', s_msg=e)


@app.route('/')
def home():
    return render_template('index.html',
                           current_time=datetime.utcnow())

if __name__ == '__main__':
    manager.run()
