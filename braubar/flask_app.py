# -*- coding: utf-8 -*-
import json
import posix_ipc as ipc

from flask import Flask, jsonify, render_template
from service.chartService import ChartService
from service.brewconfig import BrewConfig
from ipchelper import prepare_data, TYPE_CONTROL, CONTROL_NEXT


__author__ = 'oli@fesseler.info'
__version__ = ('0', '0', '1')

app = Flask(__name__)
app.config["JSON_SORT_KEY"] = False


@app.route("/")
def index():
    recipe_file = open(BrewConfig.RECIPE_FILE)
    recipe = json.load(recipe_file)
    return render_template('index.html',
                           brew_id=brew_id,
                           brew_state=ChartService().status(brew_id),
                           brew_recipe=recipe)


@app.route('/start')
def brew_start():
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
def next_state():
    msg = {"ok": False, "status": None}
    try:
        msg["status"] = ChartService().status(brew_id)
        if write_to_queue(CONTROL_NEXT):
            msg["ok"] = True
    finally:
        return jsonify(msg)


@app.route('/temp')
def temp():
    return "Not Implemented"


@app.route('/chart/data')
def chart_data():
    return ChartService().brew_chart(brew_id=brew_id)


@app.route('/chart/last_row')
def last_row():
    return jsonify(ChartService().last_row(brew_id=brew_id))


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
