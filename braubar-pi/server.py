# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template

from simplestate import SimpleState
import eventwait

__author__ = 'oli@fesseler.info'
__version__ = ('0', '0', '1')

app = Flask(__name__)

s = SimpleState()


@app.route("/")
def index():
    return "index"


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


@app.route('/brew/start')
def bewStart():
    if SimpleState.state:
        return "läuft schon im status: " + SimpleState.state

    s.runall()

    return "brauprozess gestartet"


@app.route('/brew/state')
def brewstate():
    if not s.state:
        return "no action started"
    return s.state + ' sec more to wait'


@app.route('/brew/next')
def next():
    # TODO prüfen ob thread gestartet wurde
    eventwait.end()
    return "event released"


if __name__ == "__main__":
    # start app in debugmode
    app.debug = True
    app.run(host="localhost")
