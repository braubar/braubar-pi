# -*- coding: utf-8 -*-
import os
import sys
import json

sys.path.append('./service')

from flask import Flask, jsonify, render_template
from chartService import ChartService

__author__ = 'oli@fesseler.info'
__version__ = ('0', '0', '1')

app = Flask(__name__)


@app.route("/")
def index():
    return "index"


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('starter_template.html', name=name)


@app.route('/brew/start')
def brewStart():
    return "Not Implemented"


@app.route('/brew/state')
def brewstate():
    return "Not Implemented"


@app.route('/brew/next')
def next():
    asd = None
    try:
        os.system("echo 'True' > data/next_state.brew")
        asd = {"ok": True, "state": None}
    except:
        print("next failed")
        asd = {"ok": False, "state": None}
    finally:
        return jsonify(asd)


@app.route('/brew/temp')
def temp():
    return "Not Implemented"


@app.route('/brew/chart')
def chart():
    return render_template('chart.html', brew_id=brew_id)


@app.route('/brew/chart/data_old')
def chart_data_old():
    temp_date, temp_current, temp_target, temp_change = ChartService.brew_chart(brew_id=brew_id)
    return jsonify({"temp": temp_current, "date": temp_date, "target": temp_target, "change": temp_change}) \
 \
 \
@app.route('/brew/chart/data')
def chart_data():
    return ChartService.brew_chart(brew_id=brew_id)


@app.route('/brew/chart/last')
def last_row():
    return jsonify(ChartService.last_row(brew_id=brew_id))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="BrauBar webserver at your service.")
    parser.add_argument('--host', help="IP-Address to listen on. Default is 0.0.0.0", default="0.0.0.0")
    parser.add_argument('-i', '--id', help="brew_id to identify the current brew process. "
                                           "if no id is given, it shall return all brews")
    args = parser.parse_args()
    try:
        host = args.host
        brew_id = args.id
        # start app in debugmode
        app.debug = True
        app.run(host=host)
    finally:
        print("good beer, see ya")
