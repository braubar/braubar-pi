# -*- coding: utf-8 -*-
#!/bin/python2

__author__ = 'oli@fesseler.info'
__version__ = ('0', '0', '1')


from flask import Flask
app = Flask(__name__)


@app.route("/")
def index():
    return "index"


@app.route("/hello/<name>")
def hello(name):
    """
    Testmethode um zu schauen ob der Server läuft, er antwortet und damit ich diesen wunderschönen Kommentar sehen kann.
    :return:
    """
    return "Hello %s!" % name

if __name__ == "__main__":
    # start app in debugmode
    app.debug = True
    app.run(host="localhost")
