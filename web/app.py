from bottle import route, run, template
import socket

@route('/')
def index():
    return str(socket.gethostname())

run(host='0.0.0.0', port=8000)
