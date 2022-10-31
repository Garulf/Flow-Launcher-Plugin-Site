from flask import render_template

from website import app
from website.plugins import get_plugins


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Plugins', plugins=get_plugins())
