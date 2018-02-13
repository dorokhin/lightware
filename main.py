import os
import subprocess
from flask_cors import CORS
from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, jsonify, request, make_response, render_template

application = Flask(__name__)
application.debug = True
CORS(application)
application.config['SECRET_KEY'] = 'j1h9syenwksu2nHanzPakq63sdfhshdfHjH45dfGFDjd'
toolbar = DebugToolbarExtension(application)

_version = '0.1.0'

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
                print('pin not exported')
                with open(LIGHTWARE_EXPORT_PATH, 'w') as _f_ex:
                    print('trying to export...')
                    _f_ex.write('{0}'.format(self._number))

            with open(self._lightware_gpio_direction_path(), 'w') as f:
                print('write direction')
                f.write(direction)
                f.close()
        try:
            self._f_value = open(self._lightware_gpio_value_path(), 'r+')
        except FileNotFoundError:
            self._f_value = 0
        print('GPIO value path')

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
        print('on')

    def off(self):
        self._f_value.write(LIGHTWARE_GPIO_VALUE_LOW)
        self._f_value.seek(0)
        self._f_value.close()
        print('off')

    def read(self):
        val = self._f_value.read()
        self._f_value.seek(0)
        self._f_value.close()
        return int(val)

switches_state = {
    "switches": {
        "1": {
            "id": 1,
            "name": "Основное освещение",
            "state": False,
            "color": "red",
            "active": False
        },
        "2": {
            "id": 2,
            "name": "Диван",
            "state": False,
            "color": "purple",
            "active": True
        },
        "3": {
            "id": 3,
            "name": "Вход",
            "state": False,
            "color": "yellow",
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
            "name": "Вход",
            "value": 0,
            "active": True
        },
        "2": {
            "id": 2,
            "name": "Диван",
            "value": 0,
            "active": True
        },
        "3": {
            "id": 3,
            "name": "Комп",
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
    return jsonify({"api": {"version": "0.0.1"}})


@application.route("/api/channel/status", methods=["GET"])
def get_channel_status():
    return jsonify(switches_state)


@application.route("/api/channel/set/state", methods=["POST"])
def set_state():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    _params = request.get_json()
    _channel = _params.get("channel", None)
    _state = _params.get("state", None)

    ret = {"channel": _channel, "state": _state}
    print(ret)
    switches_state['switches']['{}'.format(_channel)]['state'] = _state
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
    subprocess.call(["dimmer.py", str(_dimmer), str(_value)])
    return jsonify(ret), 200


@application.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"msg": "Resource not found"}), 404)


if __name__ == "__main__":
    application.run(host='0.0.0.0')
