# -*- coding: utf-8 -*-
import eventlet

eventlet.monkey_patch()

import time
import json
import posix_ipc as ipc

from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO, send, emit
from threading import Thread
from service.chartService import ChartService
from service.brewconfig import BrewConfig
from ipchelper import prepare_data, TYPE_CONTROL, CONTROL_NEXT

__author__ = 'oli@fesseler.info'
__version__ = ('0', '0', '1')

app = Flask(__name__)
app.config["JSON_SORT_KEY"] = False
app.config['SECRET_KEY'] = 'secret!braubar!mhh!BIER!'
socketio = SocketIO(app, async_mode='eventlet')
thread = None
cs = ChartService()


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        time.sleep(3)
        count += 1
        socketio.emit('fullchart',
                      cs.last_row2(brew_id=brew_id))


@app.route('/')
def index():
    global thread
    if thread is None:
        thread = Thread(target=background_thread)
        thread.daemon = True
        thread.start()

    recipe_file = open(BrewConfig.RECIPE_FILE)
    recipe = json.load(recipe_file)
    return render_template('index.html',
                           brew_id=brew_id,
                           brew_state=cs.status(brew_id),
                           brew_recipe=recipe)


@app.route('/start')
def brew_start():
    return "Not Implemented"


@app.route('/status')
def status():
    return jsonify(cs.status(brew_id))


@app.route('/status/brew')
def brew_state():
    return cs.brew_status(brew_id=brew_id)


@app.route('/status/system')
def system_state():
    return cs.system_status(brew_id=brew_id)


@app.route('/next')
def next_state():
    msg = {"ok": False, "status": None}
    try:
        msg["status"] = cs.status(brew_id)
        if write_to_queue(CONTROL_NEXT):
            msg["ok"] = True
    finally:
        return jsonify(msg)


@app.route('/temp')
def temp():
    return "Not Implemented"


@app.route('/chart/data')
def chart_data():
    a = cs.brew_chart(brew_id=brew_id)
    print(a)
    return a


@app.route('/chart/last_row')
def last_row():
    return jsonify(cs.last_row(brew_id=brew_id))


def write_to_queue(control):
    try:
        msg = {"control": control}
        queue = ipc.MessageQueue(name=BrewConfig.BRAUBAR_QUEUE)
        queue.send(prepare_data(TYPE_CONTROL, msg).encode(encoding=BrewConfig.QUEUE_ENCODING), timeout=0)
    except ipc.ExistentialError:
        queue.close()
        return False
    except ipc.BusyError:
        print("socket busy")
        queue.close()
        return False
    return True


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
