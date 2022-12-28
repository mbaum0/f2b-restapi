from flask import Flask
from fail2ban.client.csocket import CSocket

app = Flask(__name__)

SOCKET_FILE = '/var/run/fail2ban/fail2ban.sock'


def error(reason):
    """
    A helper function to form an error response.
    :param reason: What happened wrong
    :return: Dict of the response
    """

    return {'error': True, 'reason': reason}


def run_cmd(cmd):
    try:
        client = CSocket(SOCKET_FILE, timeout=20)
        client.settimeout(20)

        ret = client.send(cmd)

        # if an error occured
        if ret[0] != 0:
            return error('invalid response code')

        return {'error': False, 'data': ret[1]}
    except Exception as e:
        return error('exception occured: ' + str(e))


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
    return run_cmd(["stop"])

@app.route('/status')
def status():
    return run_cmd(["status"])

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
    return run_cmd(command)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
