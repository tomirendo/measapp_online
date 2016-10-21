#!/usr/local/bin/python3.5
from devices import devices, close_devices
from flask import Flask, render_template, request
from json import dumps

app = Flask(__name__)

DEBUG = True

def return_response(result):
    return dumps({'error' : False , 'result' : result})
def return_error(error_description):
    return dumps({'error' : True, 'error_description' : str(error_description)})


def find_device(name):
    for device in devices:
        if name == device.name:
            return device
    raise Exception("Device Wasn't found")

@app.route("/devices/")
def list_devices():
    return dumps([i.to_dict() for i in devices])

@app.route('/console/')
def console():
    return render_template("terminal.html")

@app.route('/update_property/', methods=['POST'])
def update_property():
    device = request.args.get("device")


if __name__ == "__main__":
    try : 
        app.run()
        close_devices()
    except : 
        close_devices()


