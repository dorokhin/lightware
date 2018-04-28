#!/usr/bin/env python
import os
import subprocess
import logging
logging.basicConfig(filename='/run/lightware.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%d.%m.%Y %H:%M:%S ')
from flask_cors import CORS, cross_origin
from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, jsonify, request, make_response, render_template

application = Flask(__name__)
application.debug = True
cors = CORS(application, resources={r"/api/*": {"origins": "*"}})
application.config['SECRET_KEY'] = 'j1h9syenwksu2nHanzPakq63sdfhshdfHjH45dfGFDjd'
toolbar = DebugToolbarExtension(application)

_version = '1.0.0'

LIGHTWARE_BASE_PATH = '/sys/class/gpio'

LIGHTWARE_EXPORT_PATH = LIGHTWARE_BASE_PATH + '/export'
LIGHTWARE_UNEXPORT_PATH = LIGHTWARE_BASE_PATH + '/unexport'

LIGHTWARE_GPIO_PATH = LIGHTWARE_BASE_PATH + '/gpio{0}'
LIGHTWARE_GPIO_DIRECTION_PATH = LIGHTWARE_GPIO_PATH + '/direction'
LIGHTWARE_GPIO_EDGE_PATH = LIGHTWARE_GPIO_PATH + '/edge'
LIGHTWARE_GPIO_VALUE_PATH = LIGHTWARE_GPIO_PATH + '/value'
LIGHTWARE_GPIO_ACTIVE_LOW_PATH = LIGHTWARE_GPIO_PATH + '/active_low'

LIGHTWARE_GPIO_VALUE_LOW = '0'
LIGHTWARE_GPIO_VALUE_HIGH = '1'


class LightWare:
    def __init__(self, num, direction='out', read_only=False):
        self._number = num
        self._direction = direction
        self._read_only = read_only
        if not self._read_only:
            if not self._check_pin_export():
                with open(LIGHTWARE_EXPORT_PATH, 'w') as _f_ex:
                    _f_ex.write('{0}'.format(self._number))

            with open(self._lightware_gpio_direction_path(), 'w') as f:
                f.write(direction)
                f.close()
        try:
            self._f_value = open(self._lightware_gpio_value_path(), 'r+')
        except FileNotFoundError:
            self._f_value = 0

    def _lightware_gpio_direction_path(self):
        return LIGHTWARE_GPIO_DIRECTION_PATH.format(self._number)

    def _lightware_gpio_value_path(self):
        return LIGHTWARE_GPIO_VALUE_PATH.format(self._number)

    def _check_pin_export(self):
        gpio_path = LIGHTWARE_GPIO_PATH.format(self._number)
        return os.path.isdir(gpio_path)

    def on(self):
        self._f_value.write(LIGHTWARE_GPIO_VALUE_HIGH)
        self._f_value.seek(0)
        self._f_value.close()

    def off(self):
        self._f_value.write(LIGHTWARE_GPIO_VALUE_LOW)
        self._f_value.seek(0)
        self._f_value.close()

    def read(self):
        val = self._f_value.read()
        self._f_value.seek(0)
        self._f_value.close()
        return int(val)


switches_state = {
    "switches": {
        "5": {
            "id": 5,
            "name": "Channel 5",
            "state": False,
            "color": "red",
            "active": True
        },
        "6": {
            "id": 6,
            "name": "Channel 6",
            "state": False,
            "color": "purple",
            "active": True
        },
        "13": {
            "id": 13,
            "name": "Channel 13",
            "state": False,
            "color": "green",
            "active": True
        },
        "19": {
            "id": 19,
            "name": "Channel 19",
            "state": False,
            "color": "yellow",
            "active": True
        },
        "26": {
            "id": 26,
            "name": "Channel 26",
            "state": False,
            "color": "orange",
            "active": True
        },
        "12": {
            "id": 12,
            "name": "Channel 12",
            "state": False,
            "color": "violet",
            "active": True
        },
        "16": {
            "id": 16,
            "name": "Channel 16",
            "state": False,
            "color": "pink",
            "active": True
        },
        "20": {
            "id": 20,
            "name": "Channel 20",
            "state": False,
            "color": "brown",
            "active": True
        }
    },
    "api": {
        "version": _version,
        "status": "up",
        "errors": None
    }
}

dimmer_state = {
    "dimmer": {
        "1": {
            "id": 1,
            "name": "Door",
            "value": 0,
            "active": True
        },
        "2": {
            "id": 2,
            "name": "Sofa",
            "value": 0,
            "active": True
        },
        "3": {
            "id": 3,
            "name": "Work zone",
            "value": 0,
            "active": True
        }
    },
    "api": {
        "version": _version,
        "status": "up",
        "errors": None
    }
}


@application.route("/", methods=["GET"])
def index():
    return render_template('index.html')


@application.route("/api")
def api():
    return jsonify({"api": {"version": "1.0.0"}})


@application.route("/api/channel/status", methods=["GET"])
def get_channel_status():
    return jsonify(switches_state)


@application.route("/api/channel/set/state", methods=["POST"])
@cross_origin()
def set_state():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    _params = request.get_json()
    _channel = _params.get("channel", None)
    _state = _params.get("state", None)

    ret = {"channel": _channel, "state": _state}
    switches_state['switches']['{}'.format(_channel)]['state'] = _state

    if _state:
        LightWare(_channel).on()
    else:
        LightWare(_channel).off()

    return jsonify(ret), 200


@application.route("/api/dimmer/status", methods=["GET"])
def get_dimmer_status():
    return jsonify(dimmer_state)


@application.route("/api/dimmer/set/state", methods=["POST"])
def set_dimmer_state():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    _params = request.get_json()
    _dimmer = _params.get("dimmer", None)
    _value = _params.get("value", None)
    if not _value:
        return jsonify({"msg": "Missing value"}), 400
    if _value < 0 or _value > 100:
        return jsonify({"msg": "Out of range"}), 400

    ret = {"dimmer": _dimmer, "value": _value}
    dimmer_state['dimmer']['{}'.format(_dimmer)]['value'] = _value

    try:
        subprocess.call(['dimmer.py', str(_dimmer), str(_value)], cwd='/home/projects/lightware')
        logging.info('set dimmer #{0} value to {1} %'.format(_dimmer, _value))
        return jsonify(ret), 200
    except Exception as e:
        logging.warning('Error: ' + str(e))
        return make_response(jsonify({"msg": "Server error"}), 500)


@application.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"msg": "Resource not found"}), 404)


@application.errorhandler(405)
def handle_bad_request(error):
    return make_response(jsonify({"msg": "Method not allowed"}), 405)


if __name__ == "__main__":
    application.run(host='0.0.0.0')
