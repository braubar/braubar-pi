# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template

from simplestate import SimpleState
from test import testReadTempSocket

__author__ = 'oli@fesseler.info'
__version__ = ('0', '0', '1')

app = Flask(__name__)




@app.route("/")
def index():
    return "index"


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


@app.route('/brew/start')
def bewStart():
    if SimpleState.instance().state:
        # TODO geht net
        return "läuft schon im status: " + SimpleState.instance().state
    a = SimpleState.instance().next()
    return "brauprozess gestartet"


@app.route('/brew/state')
def brewstate():
    if not SimpleState.instance().state:
        return "no action started"
    return SimpleState.instance().state + ' sec more to wait'


@app.route('/brew/next')
def next():
    # TODO prüfen ob thread gestartet wurde
    return SimpleState.instance().next()

@app.route('/brew/temp')
def temp():
    a = testReadTempSocket()


if __name__ == "__main__":
    # start app in debugmode
    app.debug = True
    app.run(host="192.168.2.9")
