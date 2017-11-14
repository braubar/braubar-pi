# -*- coding: utf-8 -*-
import json
import posix_ipc as ipc
import subprocess

from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, send, emit

from service.chartService import ChartService
from service.brewconfig import BrewConfig
from service.ipchelper import prepare_data, TYPE_CONTROL, CONTROL_NEXT
from service.powerstrip import PowerStrip

__author__ = 'oli@fesseler.info'
__version__ = ('0', '0', '1')

app = Flask(__name__)
app.config["JSON_SORT_KEY"] = False
app.config['SECRET_KEY'] = 'secret!braubar!mhh!BIER!'
socketio = SocketIO(app, async_mode='eventlet')
thread = None
cs = None
bc = None
ps = None
bd = None

POWERSTRIP_URL = BrewConfig().get('powerstrip')['url']
BREWDAEMON_FILE = "../braubar/brewdaemon"


@app.route('/')
def index():
    return render_template('index.html',
                           brew_id=brew_id,
                           powerstrip_url=ps.get_url(),
                           powerstrip_ok=ps.check(),
                           sensor_port=bc.get("braubar")["sensor_port"],
                           last_brew_id=cs.get_last_brew_id())


@app.route('/brewboard', methods=["POST"])
def brewboard():
    print(request)
    form = request
    brew_id = request.values["brew_id"]
    # TODO: brewdaemon run
    start_brewdaemon(brew_id)
    recipe_file = open(BrewConfig.RECIPE_FILE)
    recipe = json.load(recipe_file)
    print(recipe)
    bd.run(id)
    return render_template('brew.html',
                           brew_id=brew_id,
                           brew_state=cs.status(brew_id),
                           brew_recipe=recipe)


@socketio.on("connected")
def handle_connected(connected_msg):
    emit("fullchart", cs.brew_chart(brew_id=brew_id))
    print(connected_msg)


@socketio.on("update chart")
def handle_update(update_msg):
    socketio.emit("update chart", json.dumps(cs.status(brew_id=brew_id)))
    print("emitted update chart after message: ", update_msg)

@socketio.on("next")
def next_state(next):
    msg = {"ok": False, "status": None}
    try:
        msg["status"] = cs.status(brew_id)
        print("status:", cs.status(brew_id))
        if write_to_queue(CONTROL_NEXT):
            print("write to queue worked")
            msg["ok"] = True
    except Exception as e:
        print("flask_app error:", e)
    finally:
        socketio.emit("next", json.dumps(msg))


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
    except Exception as e:
        print("error: ", e)

    finally:
        return jsonify(msg)


@app.route('/temp')
def temp():
    return "Not Implemented"


@app.route('/chart/data')
def chart_data():
    a = cs.brew_chart(brew_id=brew_id)
    return a


@app.route('/chart/last_row')
def last_row():
    return jsonify(cs.last_row(brew_id=brew_id))


def write_to_queue(control):
    try:
        msg = {"control": control}
        queue = ipc.MessageQueue(name=BrewConfig.BRAUBAR_QUEUE)
        queue.send(prepare_data(TYPE_CONTROL, msg).encode(encoding=BrewConfig.QUEUE_ENCODING), timeout=5)
    except ipc.ExistentialError as e:
        print("IPC Extential Error happened", e)
        queue.close()
        return False
    except ipc.BusyError as e:
        print("socket busy error: write_to_queue", e)
        queue.close()
        return False
    except Exception as e:
        print("error: ", e)

    return True


def start_brewdaemon(brew_id):
    brewdaemon_args = ["python3", BREWDAEMON_FILE, "--id", brew_id]
    subprocess.Popen(brewdaemon_args)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="BrauBar webserver at your service.")
    parser.add_argument('--host', help="IP-Address to listen on. Default is 0.0.0.0", default="0.0.0.0")
    parser.add_argument('-i', '--id', help="brew_id to identify the current brew process. "
                                           "if no id is given, it shall return all brews")
    parser.add_argument('--powerstrip', help="URL for Powerstrip. Format:e.g. 'http://localhost:8080'",
                        default=POWERSTRIP_URL)
    args = parser.parse_args()

    if POWERSTRIP_URL != args.powerstrip:
        POWERSTRIP_URL = args.powerstrip

    try:
        host = args.host
        brew_id = args.id

        # start app in debugmode
        app.debug = True

        cs = ChartService()
        bc = BrewConfig()
        ps = PowerStrip(url=POWERSTRIP_URL)

        socketio.run(app, host=host)
    finally:
        print("good beer, see ya")
