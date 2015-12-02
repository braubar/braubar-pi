# -*- coding: utf-8 -*-
# !/bin/python2

__author__ = 'oli@fesseler.info'
__version__ = ('0', '0', '1')

from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/")
def index():
    return "index"


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


if __name__ == "__main__":
    # start app in debugmode
    app.debug = True
    app.run(host="localhost")
