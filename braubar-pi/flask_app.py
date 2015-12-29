# -*- coding: utf-8 -*-
from flask import Flask, jsonify
from flask import render_template
import json

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
def brewStart():
    return "Not Implemented"


@app.route('/brew/state')
def brewstate():
    return "Not Implemented"


@app.route('/brew/next')
def next():
    # TODO prüfen ob thread gestartet wurde
    return "Not Implemented"


@app.route('/brew/temp')
def temp():
    return "Not Implemented"


@app.route('/brew/chart')
def chart():
    temp_data = {}
    return render_template('chart.html', temp_data=temp_data)
    # return render_template('chart.html', temp_data="hello")


@app.route('/brew/chart/data')
def chart_data():
    temp_current = []
    temp_date = []
    temp_target = []
    temp_change = []
    last_temp = 0.0
    count = 0
    f = open("./log/brewlog_29-12-2015_00-54-13.log")
    for line in f.readlines():
        temp = line[26:-2].split()[3][:-1]
        temp = float(temp)
        if last_temp != temp or last_temp <= temp - 0.1 and temp + 0.1 >= last_temp:
            temp_current.append(temp)
            temp_target.append(line[26:-2].split()[1][:-1])
            temp_date.append(line[1:24])
            temp_change.append(line[26:-2].split()[5][:-1])
        else:
            count += 1
        last_temp = temp
    print("omitted", count, "lines")
    return jsonify({"temp": temp_current, "date": temp_date, "target": temp_target, "change": temp_change});


if __name__ == "__main__":
    # start app in debugmode
    app.debug = True
    app.run(host="192.168.2.9")
