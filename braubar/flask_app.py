# -*- coding: utf-8 -*-
import eventlet
eventlet.monkey_patch()
import json
import logging
import os
import time
import service.brewconfig as config

from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO, send, emit
from threading import Thread
from service.chartService import ChartService

LOG_BASE=config.BrewConfig.LOG_BASE

# logfile = "brewlog_" + time.strftime("%d-%m-%Y_%H-%M-%S", time.localtime()) + ".log"
logfile = config.BrewConfig.LOG_BASE + time.strftime("%d-%m-%Y_%H-%M-%S", time.localtime()) + ".log"
logging.basicConfig(filename=logfile, level=logging.WARN, format='{%(asctime)s: %(message)s}')


__author__ = 'oli@fesseler.info'
__version__ = ('0', '0', '1')

app = Flask(__name__)
app.config["JSON_SORT_KEY"] = False
app.config['SECRET_KEY'] = 'secret!braubar!mhh!BIER!'
socketio = SocketIO(app, async_mode='eventlet')
thread = None

def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        time.sleep(3)
        count += 1
        socketio.emit('fullchart',
                      ChartService().last_row2(brew_id=brew_id))


@app.route('/')
def index():
    global thread
    if thread is None:
        thread = Thread(target=background_thread)
        thread.daemon = True
        thread.start()

    recipe_file = open(config.BrewConfig().RECIPE_FILE)
    recipe = json.load(recipe_file)
    return render_template('index.html',
                           brew_id=brew_id,
                           brew_state=ChartService().status(brew_id),
                           brew_recipe=recipe)


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
        os.system("echo 'True' > " + config.BrewConfig.NEXT_STATE_FILE)
        asd = {"ok": True, "status": ChartService().status(brew_id)}
    except:
        print("next failed")
        asd = {"ok": False, "status": ChartService().status(brew_id)}
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
    # config.BrewConfig.CONFIG_FILE = "/home/oli/dev/braubar-pi/config/config.json"
    # config.BrewConfig.RECIPE_FILE = "/home/oli/dev/braubar-pi/config/recipe.json"

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
        socketio.run(app, host=host)
    finally:
        print("good beer, see ya")
