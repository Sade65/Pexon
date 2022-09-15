import datetime
from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap


app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('index.html', utc_dt=datetime.datetime.utcnow())
