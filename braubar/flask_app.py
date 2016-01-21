# -*- coding: utf-8 -*-
import logging
import os
import datetime

from flask import Flask, jsonify, render_template
from service.chartService import ChartService
import service.brewconfig as config
import time


logfile = config.BrewConfig.LOG_BASE + time.strftime("%d-%m-%Y_%H-%M-%S", time.localtime()) + ".log"
logging.basicConfig(filename=logfile, level=logging.WARN, format='{%(asctime)s: %(message)s}')

__author__ = 'oli@fesseler.info'
__version__ = ('0', '0', '1')

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html', brew_id=brew_id, brew_state=ChartService().status(brew_id))


@app.route('/start')
def brewStart():
    return "Not Implemented"


@app.route('/status')
def status():
    return jsonify(ChartService().status(brew_id))


@app.route('/status/brew')
def brew_state():
    return ChartService.brew_status(brew_id=brew_id)


@app.route('/status/system')
def system_state():
    return ChartService.system_status(brew_id=brew_id)


@app.route('/next')
def next():
    asd = None
    try:
        os.system("echo 'True' > " + config.NEXT_STATE_FILE)
        asd = {"ok": True, "state": None}
    except:
        print("next failed")
        asd = {"ok": False, "state": None}
    finally:
        return jsonify(asd)


@app.route('/temp')
def temp():
    return "Not Implemented"


@app.route('/chart/data')
def chart_data():
    return ChartService().brew_chart(brew_id=brew_id)


@app.route('/chart/last_row')
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
