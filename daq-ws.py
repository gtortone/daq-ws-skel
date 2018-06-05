#!/usr/bin/env python
from threading import Lock
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, Namespace, emit, join_room, leave_room, \
    close_room, rooms, disconnect

from frontend import Frontend
import asyncio
from threading import Thread

async_mode = None

app = Flask(__name__)
socketio = SocketIO(app, async_mode=async_mode)
f = Frontend(socketio) 

@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@socketio.on('disconnect_request', namespace='/daq')
def on_disconnect_request():
    disconnect()

@socketio.on('ping', namespace='/daq')
def on_ping():
    emit('pong')

@socketio.on('connect', namespace='/daq')
def on_connect():
    print("Client connected")

@socketio.on('disconnect', namespace='/daq')
def on_disconnect():
    print('Client disconnected', request.sid)

@socketio.on('start', namespace='/daq')
def on_start():
    print('DAQ started', request.sid)
    f.start()

@socketio.on('stop', namespace='/daq')
def on_stop():
    print('DAQ stopped', request.sid)
    f.stop()

@socketio.on('pause', namespace='/daq')
def on_pause():
    print('DAQ paused', request.sid)
    f.pause()

if __name__ == '__main__':
    # set use_reloader to avoid twice initialization of global vars
    socketio.run(app, debug=True, use_reloader=False)
