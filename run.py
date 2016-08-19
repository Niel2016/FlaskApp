from flask import Flask, render_template, g, abort, request
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
	return render_template('404.html',
							msg=e)

@app.route('/')
def home():
  # abort(404)
  return render_template('index.html',
                         name=g.user)

if __name__ == '__main__':
  'This is main function.'
  manager.run()
