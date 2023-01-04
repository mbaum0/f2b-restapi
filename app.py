from flask import Flask, jsonify
from dataclasses import dataclass
from fail2ban.client.csocket import CSocket

app = Flask(__name__)

SOCKET_FILE = '/var/run/fail2ban/fail2ban.sock'


@dataclass
class F2BJailStatus:
    currently_banned: int
    total_banned: int
    ips: list

@dataclass
class F2BStatus:
    num_jails: int
    jails: list

def run_cmd(cmd):
    """
    Runs a supported F2B-Client command. Returns a tuple
    containing: (did_error, result)

    if did_error is True, result is a string errror message, otherwise
    result is the F2B-Client output from the executed command
    """
    try:
        client = CSocket(SOCKET_FILE, timeout=20)
        client.settimeout(20)

        ret = client.send(cmd)

        # if an error occured
        if ret[0] != 0:
            return (True, 'invalid response code')

        return (False, ret[1])
    except Exception as e:
        return (True, 'exception occured: ' + str(e))


def parse_jail_status_output(data):
    curr_banned = data[1][1][0][1]
    total_banned = data[1][1][1][1]
    ips = data[1][1][2][1]
    return F2BJailStatus(curr_banned, total_banned, ips)

def parse_status_output(data):
    num_jails = data[0][1]
    jails = str.split(data[1][1], ', ')
    return F2BStatus(num_jails, jails)


@app.route('/')
def home():
    return {"hello": "world"}

# BASIC


@app.route('/start')
def start():
    return run_cmd(["start"])


@app.route('/reload')
def reload():
    return run_cmd(["reload"])


@app.route('/reload/<jail>')
def reload_jail(jail):
    return run_cmd(["reload", jail])


@app.route('/stop')
def stop():
    return run_cmd(["stop"])[1]


@app.route('/status')
def status():
    failure, data = run_cmd(["status"])
    if failure:
        return jsonify({'failure': True, 'data': data})
    else:
        parsed = parse_status_output(data)
        return jsonify({'failure': False, 'data': parsed})


@app.route('/ping')
def ping():
    return run_cmd(["ping"])


# JAIL CONTROL
@app.route('/start/<jail>')
def start_jail(jail):
    return run_cmd(["start", jail])


@app.route('/stop/<jail>')
def stop_jail(jail):
    return run_cmd(["stop", jail])


@app.route('/status/<jail>')
def status_jail(jail):
    command = ["status", jail]
    failure, data = run_cmd(command)
    if failure:
        return jsonify({'failure': True, 'data': data})
    else:
        parsed = parse_jail_status_output(data)
        return jsonify({'failure': False, 'data': parsed})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
