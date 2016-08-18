from flask import Flask, render_template, g, abort
from flask_script import Manager


app = Flask(__name__)
manager = Manager(app)

app.config['DEBUG'] = True
@app.before_request
def before_first_request():
  g.user = 'dave'

@app.route('/')
def home():
  # abort(404)
  return render_template('index.html',
                         name=g.user)

if __name__ == '__main__':
  manager.run()
