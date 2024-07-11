from flask import Flask, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('location_update')
def handle_location_update(data):
    emit('update_marker', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app)
