#!/usr/local/bin/python3.5
from devices import devices
from flask import Flask, render_template
from json import dumps

app = Flask(__name__)

DEBUG = True
@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/devices/")
def list_devices():
    return dumps([i.to_dict() for i in devices])


if __name__ == "__main__":
    app.run()